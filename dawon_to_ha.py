import sys
import json
import os.path

ha_path = "/data/homeassistant"

def add_plug(mac, name, model):
    payload_on = json.dumps({"sid":"2","msg":{"o":"e","e":[{"n":"/100/0/31","sv":"true","r":"","ti":"1593516756"}]}}, separators=(',', ':'))
    payload_off = json.dumps({"sid":"2","msg":{"o":"e","e":[{"n":"/100/0/31","sv":"false","r":"","ti":"1593516756"}]}}, separators=(',', ':'))

    did = model + "-" + mac
    plug_name = mac + "_plug"

    lines = []
    lines.append("platform: mqtt")
    lines.append("unique_id: \"" + plug_name + "\"")
    lines.append("name: \"" + plug_name + "\"")
    lines.append("command_topic: \"dwd.v1/iot-server/DAWONDNS-" + did + "/execute/json\"")
    lines.append("state_topic: \"dwd.v1/DAWONDNS-" + did + "/iot-server/notify/json\"")
    lines.append("payload_on: '" + payload_on + "'")
    lines.append("payload_off: '" + payload_off + "'")
    lines.append("state_on: 'on'")
    lines.append("state_off: 'off'")
    lines.append("value_template: >-")
    lines.append("  {% if value_json.sid == '2' %}")
    lines.append("    {% if value_json.msg.e[0].sv == 'true' %}")
    lines.append("      on")
    lines.append("    {% else %}")
    lines.append("      off")
    lines.append("    {% endif %}")
    lines.append("  {% else %}")
    lines.append("  {% endif %}")

    yaml = open(ha_path + "/switch/" + plug_name + ".yaml", 'w')
    yaml.writelines('\n'.join(lines))
    yaml.close()

def add_energy_sensor(mac, name, model):
    did = model + "-" + mac
    sensor_name = mac + "_energy"

    lines = []
    lines.append("platform: mqtt")
    lines.append("unique_id: \"" + sensor_name + "\"")
    lines.append("name: \"" + sensor_name + "\"")
    lines.append("unit_of_measurement: \"W\"")
    lines.append("state_topic: \"dwd.v1/DAWONDNS-" + did + "/iot-server/notify/json\"")
    lines.append("value_template: >-")
    lines.append("  {% set measured = (value_json.msg.e[1].sv | float(0) | round(2)) if value_json.sid == '2' else ((value_json.msg.e[3].sv | float(0) | round(2)) if value_json.sid == '1' else states('sensor." + sensor_name + "')) %}")
    lines.append("  {% if measured < 3520 %}")
    lines.append("    {{ measured }}")
    lines.append("  {% else %}")
    lines.append("    {{ states('sensor." + sensor_name + "') }}")
    lines.append("  {% endif %}")

    yaml = open(ha_path + "/sensor/" + sensor_name + ".yaml", 'w')
    yaml.writelines('\n'.join(lines))
    yaml.close()

def add_temperature_sensor(mac, name, model):
    did = model + "-" + mac
    sensor_name = mac + "_temperature"

    lines = []
    lines.append("platform: mqtt")
    lines.append("unique_id: \"" + sensor_name + "\"")
    lines.append("name: \"" + sensor_name + "\"")
    lines.append("unit_of_measurement: \"℃\"")
    lines.append("state_topic: \"dwd.v1/DAWONDNS-" + did + "/iot-server/notify/json\"")
    lines.append("value_template: >-")
    lines.append("  {% set temp = (value_json.msg.e[2].sv | float(0) | round(2)) if value_json.sid == '2' else ((value_json.msg.e[8].sv | float(0) | round(2)) if value_json.sid == '1' else states('sensor." + sensor_name + "')) %}")
    lines.append("  {% if temp > 1 %}")
    lines.append("    {{ temp }}")
    lines.append("  {% else %}")
    lines.append("    {{ states('sensor." + sensor_name + "') }}")
    lines.append("  {% endif %}")

    yaml = open(ha_path + "/sensor/" + sensor_name + ".yaml", 'w')
    yaml.writelines('\n'.join(lines))
    yaml.close()

def add_energy_integration(mac, name, model):
    sensor_name = mac + "_energy"
    integration_name = mac + "_integration"

    lines = []
    lines.append("platform: integration")
    lines.append("name: \"" + integration_name + "\"")
    lines.append("source: sensor." + sensor_name)
    lines.append("unit_prefix: k")
    lines.append("round: 2")

    yaml = open(ha_path + "/sensor/" + integration_name + ".yaml", 'w')
    yaml.writelines('\n'.join(lines))
    yaml.close()

def add_utility_meter(mac, name, model):
    integration = mac + "_integration"
    daily = mac + "_integration_daily"
    monthly = mac + "_integration_monthly"

    lines = []
    lines.append(daily + ":")
    lines.append("  source: sensor." + integration)
    lines.append("  cycle: daily")

    lines.append(monthly + ":")
    lines.append("  source: sensor." + integration)
    lines.append("  cycle: monthly")

    yaml = open(ha_path + "/utility_meter/" + integration + ".yaml", 'w')
    yaml.writelines('\n'.join(lines))
    yaml.close()

def add_refresh(mac, name, model):
    # payload for energy and temperature
    payload = json.dumps({"sid":"2","msg":{"o":"r","e":[{"n":"/100/0/31","ti":"1593516756"},{"n":"/100/0/11","ti":"1593516556"},{"n":"/100/0/4","ti":"1593516556"}]}}, separators=(',', ':'))
    did = model + "-" + mac

    path = ha_path + "/automation/dawon_plug_info_refresh.yaml"

    lines = []

    if os.path.isfile(path):
        yaml = open(path, 'a')
        lines.append("  - service: mqtt.publish")
        lines.append("    data_template:")
        lines.append("      topic: \"dwd.v1/iot-server/DAWONDNS-" + did + "/read/json\"")
        lines.append("      payload: '" + payload + "'")
        lines.append("")

    else:
        yaml = open(path, 'w')
        lines.append("alias: 'dawon_plug_info_refresh'")
        lines.append("trigger:")
        lines.append("  platform: time_pattern")
        lines.append("  seconds: '/30'")
        lines.append("action:")
        lines.append("  - service: mqtt.publish")
        lines.append("    data_template:")
        lines.append("      topic: \"dwd.v1/iot-server/DAWONDNS-" + did + "/read/json\"")
        lines.append("      payload: '" + payload + "'")
        lines.append("")

    yaml.writelines('\n'.join(lines))
    yaml.close()

def add_customize(mac, name):
    path = ha_path + "/customize.yaml"

    mode = 'a'

    if os.path.isfile(path):
        mode = 'a'
    else:
        mode = 'w'

    lines = []
    lines.append("# " + name)
    lines.append("switch." + mac + "_plug:")
    lines.append("  friendly_name: " + name)
    lines.append("  icon: hass:power")
    lines.append("sensor." + mac + "_temperature:")
    lines.append("  friendly_name: " + name + " 내부온도")
    lines.append("  icon: hass:thermometer")
    lines.append("sensor." + mac + "_energy:")
    lines.append("  friendly_name: " + name + " 소모전력")
    lines.append("  icon: hass:speedometer")
    lines.append("sensor." + mac + "_integration:")
    lines.append("  friendly_name: " + name + " 누적 소모전력")
    lines.append("sensor." + mac + "_integration_daily:")
    lines.append("  friendly_name: " + name + " 일간 소모전력")
    lines.append("  icon: hass:calendar-today")
    lines.append("sensor." + mac + "_integration_monthly:")
    lines.append("  friendly_name: " + name + " 월간 소모전력")
    lines.append("  icon: hass:calendar-month")
    lines.append("")

    yaml = open(path, mode)
    yaml.writelines('\n'.join(lines))
    yaml.close()

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
