import sys
import json
import os.path

ha_path = "/data/homeassistant"

def add_plug(mac, name, model):
    payload_on = json.dumps({"sid":"2","msg":{"o":"e","e":[{"n":"/100/0/31","sv":"true","r":"","ti":"1593516756"}]}}, separators=(',', ':'))
    payload_off = json.dumps({"sid":"2","msg":{"o":"e","e":[{"n":"/100/0/31","sv":"false","r":"","ti":"1593516756"}]}}, separators=(',', ':'))

    did = model + "-" + mac
    plug_name = mac + "_plug"

    yaml = open(ha_path + "/switch/" + plug_name + ".yaml", 'w')

    print("platform: mqtt", file=yaml)
    print("unique_id: \"" + plug_name + "\"", file=yaml)
    print("name: \"" + plug_name + "\"", file=yaml)
    print("command_topic: \"dwd.v1/iot-server/DAWONDNS-" + did + "/execute/json\"", file=yaml)
    print("state_topic: \"dwd.v1/DAWONDNS-" + did + "/iot-server/notify/json\"", file=yaml)
    print("payload_on: '" + payload_on + "'", file=yaml)
    print("payload_off: '" + payload_off + "'", file=yaml)
    print("state_on: 'on'", file=yaml)
    print("state_off: 'off'", file=yaml)
    print("value_template: >-", file=yaml)
    print("  {% if value_json.sid == '2' %}", file=yaml)
    print("    {% if value_json.msg.e[0].sv == 'true' %}", file=yaml)
    print("      on", file=yaml)
    print("    {% else %}", file=yaml)
    print("      off", file=yaml)
    print("    {% endif %}", file=yaml)
    print("  {% else %}", file=yaml)
    print("  {% endif %}", file=yaml)

    yaml.close()

def add_energy_sensor(mac, name, model):
    did = model + "-" + mac
    sensor_name = mac + "_energy"
    yaml = open(ha_path + "/sensor/" + sensor_name + ".yaml", 'w')

    print("platform: mqtt", file=yaml)
    print("unique_id: \"" + sensor_name + "\"", file=yaml)
    print("name: \"" + sensor_name + "\"", file=yaml)
    print("unit_of_measurement: \"W\"", file=yaml)
    print("state_topic: \"dwd.v1/DAWONDNS-" + did + "/iot-server/notify/json\"", file=yaml)
    print("value_template: >-", file=yaml)
    print("  {% if value_json.sid == '2' %}", file=yaml)
    print("    {{ value_json.msg.e[1].sv | float | round(2) }}", file=yaml)
    print("  {% elif value_json.sid == '1' %}", file=yaml)
    print("    {{ value_json.msg.e[3].sv | float | round(2) }}", file=yaml)
    print("  {% else %}", file=yaml)
    print("    {{ states('sensor." + sensor_name + "') }}", file=yaml)
    print("  {% endif %}", file=yaml)

def add_temperature_sensor(mac, name, model):
    did = model + "-" + mac
    sensor_name = mac + "_temperature"
    yaml = open(ha_path + "/sensor/" + sensor_name + ".yaml", 'w')

    print("platform: mqtt", file=yaml)
    print("unique_id: \"" + sensor_name + "\"", file=yaml)
    print("name: \"" + sensor_name + "\"", file=yaml)
    print("unit_of_measurement: \"℃\"", file=yaml)
    print("state_topic: \"dwd.v1/DAWONDNS-" + did + "/iot-server/notify/json\"", file=yaml)
    print("value_template: >-", file=yaml)
    print("  {% set temp = (value_json.msg.e[2].sv | float | round(2)) if value_json.sid == '2' else ((value_json.msg.e[8].sv | float | round(2)) if value_json.sid == '1' else states('sensor." + sensor_name + "')) %}", file=yaml)
    print("  {% if temp > 1 %}", file=yaml)
    print("    {{ temp }}", file=yaml)
    print("  {% else %}", file=yaml)
    print("    {{ states('sensor." + sensor_name + "') }}", file=yaml)
    print("  {% endif %}", file=yaml)
    #print("  {% if value_json.sid == '2' %}", file=yaml)
    #print("    {{ value_json.msg.e[2].sv | float | round(2) }}", file=yaml)
    #print("  {% elif value_json.sid == '1' %}", file=yaml)
    #print("    {{ value_json.msg.e[8].sv | float | round(2) }}", file=yaml)
    #print("  {% else %}", file=yaml)
    #print("    {{ states('sensor." + sensor_name + "') }}", file=yaml)
    #print("  {% endif %}", file=yaml)

def add_energy_integration(mac, name, model):
    sensor_name = mac + "_energy"
    integration_name = mac + "_integration"

    yaml = open(ha_path + "/sensor/" + integration_name + ".yaml", 'w')
    print("platform: integration", file=yaml)
    print("name: \"" + integration_name + "\"", file=yaml)
    print("source: sensor." + sensor_name, file=yaml)
    print("unit_prefix: k", file=yaml)
    print("round: 2", file=yaml)

    yaml.close()

def add_utility_meter(mac, name, model):
    integration = mac + "_integration"
    daily = mac + "_integration_daily"
    monthly = mac + "_integration_monthly"

    yaml = open(ha_path + "/utility_meter/" + integration + ".yaml", 'w')

    print(daily + ":", file=yaml)
    print("  source: sensor." + integration, file=yaml)
    print("  cycle: daily", file=yaml)

    print(monthly + ":", file=yaml)
    print("  source: sensor." + integration, file=yaml)
    print("  cycle: monthly", file=yaml)

    yaml.close()

def add_refresh(mac, name, model):
    # payload for energy and temperature
    payload = json.dumps({"sid":"2","msg":{"o":"r","e":[{"n":"/100/0/31","ti":"1593516756"},{"n":"/100/0/11","ti":"1593516556"},{"n":"/100/0/4","ti":"1593516556"}]}}, separators=(',', ':'))
    did = model + "-" + mac

    path = ha_path + "/automation/dawon_plug_info_refresh.yaml"

    if os.path.isfile(path):
        yaml = open(path, 'a')
        print("  - service: mqtt.publish", file=yaml)
        print("    data_template:", file=yaml)
        print("      topic: \"dwd.v1/iot-server/DAWONDNS-" + did + "/read/json\"", file=yaml)
        print("      payload: '" + payload + "'", file=yaml)

    else:
        yaml = open(path, 'w')
        print("alias: 'dawon_plug_info_refresh'", file=yaml)
        print("trigger:", file=yaml)
        print("  platform: time_pattern", file=yaml)
        print("  seconds: '/30'", file=yaml)
        print("action:", file=yaml)
        print("  - service: mqtt.publish", file=yaml)
        print("    data_template:", file=yaml)
        print("      topic: \"dwd.v1/iot-server/DAWONDNS-" + did + "/read/json\"", file=yaml)
        print("      payload: '" + payload + "'", file=yaml)

    yaml.close()

def add_customize(mac, name):
    path = ha_path + "/customize.yaml"

    mode = 'a'

    if os.path.isfile(path):
        mode = 'a'
    else:
        mode = 'w'

    yaml = open(path, mode)
    print("# " + name, file=yaml)
    print("switch." + mac + "_plug:", file=yaml)
    print("  friendly_name: " + name, file=yaml)
    print("sensor." + mac + "_temperature:", file=yaml)
    print("  friendly_name: " + name + " 내부온도", file=yaml)
    print("sensor." + mac + "_energy:", file=yaml)
    print("  friendly_name: " + name + " 소모전력", file=yaml)
    print("sensor." + mac + "_integration:", file=yaml)
    print("  friendly_name: " + name + " 누적 소모전력", file=yaml)
    print("sensor." + mac + "_integration_daily:", file=yaml)
    print("  friendly_name: " + name + " 일간 소모전력", file=yaml)
    print("sensor." + mac + "_integration_monthly:", file=yaml)
    print("  friendly_name: " + name + " 월간 소모전력", file=yaml)
    print("", file=yaml)


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 3:
        print("Usage python3 dawon_to_ha.py mac_address name friendly_name model_name[optional]")
        exit()

    mac = sys.argv[1].lower()
    name = sys.argv[2]
    model = "B5X"

    if argc == 4:
        model = sys.argv[3]

    print("DAWONDNS-" + model + "-" + mac)

    add_plug(mac, name, model)
    add_energy_sensor(mac, name, model)
    add_energy_integration(mac, name, model)
    add_temperature_sensor(mac, name, model)
    add_utility_meter(mac, name, model)
    add_refresh(mac, name, model)
    add_customize(mac, name)
