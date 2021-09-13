import sys
import json
import os.path

ha_path = "/data/homeassistant"

def add_switch(mac, model):
    payload_on = json.dumps({"sid":"2","msg":{"o":"e","e":[{"n":"/100/0/31","sv":"true","r":"","ti":"1593516756"}]}}, separators=(',', ':'))
    payload_off = json.dumps({"sid":"2","msg":{"o":"e","e":[{"n":"/100/0/31","sv":"false","r":"","ti":"1593516756"}]}}, separators=(',', ':'))

    did = model + "-" + mac
    switch_name = mac + "_switch"

    yaml = open(ha_path + "/switch/" + switch_name + ".yaml", 'w')

    print("platform: mqtt", file=yaml)
    print("unique_id: \"" + switch_name + "\"", file=yaml)
    print("name: \"" + switch_name + "\"", file=yaml)
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

def add_sensor(mac, model):
    did = model + "-" + mac
    sensor_name = mac + "_sensor"
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


def add_energy(mac, model):
    sensor_name = mac + "_sensor"
    energy_name = mac + "_energy"

    yaml = open(ha_path + "/sensor/" + energy_name + ".yaml", 'w')
    print("platform: integration", file=yaml)
    print("name: \"" + energy_name + "\"", file=yaml)
    print("source: sensor." + sensor_name, file=yaml)
    print("unit_prefix: k", file=yaml)
    print("round: 2", file=yaml)

    yaml.close()

def add_utility_meter(mac, model):
    energy = mac + "_energy"
    daily = mac + "_daily_energy"
    monthly = mac + "_monthly_energy"

    yaml = open(ha_path + "/utility_meter/" + energy + ".yaml", 'w')

    print(daily + ":", file=yaml)
    print("  source: sensor." + energy, file=yaml)
    print("  cycle: daily", file=yaml)

    print(monthly + ":", file=yaml)
    print("  source: sensor." + energy, file=yaml)
    print("  cycle: monthly", file=yaml)

    yaml.close()

def add_refresh(mac, model):
    payload_power = json.dumps({"sid":"2","msg":{"o":"r","e":[{"n":"/100/0/31","ti":"1593516756"},{"n":"/100/0/11","ti":"1593516556"}]}}, separators=(',', ':'))
    did = model + "-" + mac

    path = ha_path + "/automation/dawon_plug_power_refresh.yaml"

    if os.path.isfile(path):
        yaml = open(path, 'a')
        print("  - service: mqtt.publish", file=yaml)
        print("    data_template:", file=yaml)
        print("      topic: \"dwd.v1/iot-server/DAWONDNS-" + did + "/read/json\"", file=yaml)
        print("      payload: '" + payload_power + "'", file=yaml)

    else:
        yaml = open(path, 'w')
        print("alias: 'dawon_plug_power_refresh'", file=yaml)
        print("trigger:", file=yaml)
        print("  platform: time_pattern", file=yaml)
        print("  seconds: '/30'", file=yaml)
        print("action:", file=yaml)
        print("  - service: mqtt.publish", file=yaml)
        print("    data_template:", file=yaml)
        print("      topic: \"dwd.v1/iot-server/DAWONDNS-" + did + "/read/json\"", file=yaml)
        print("      payload: '" + payload_power + "'", file=yaml)

    yaml.close()

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print("Usage python3 refresh.py mac_address name model_name[optional]")
        exit()

    mac = sys.argv[1].lower()
    model = "B5X"

    if argc == 3:
        model = sys.argv[2]

    print("DAWONDNS-" + model + "-" + mac)

    add_switch(mac, model)
    add_sensor(mac, model)
    add_energy(mac, model)
    add_utility_meter(mac, model)
    add_refresh(mac, model)
