import sys

ha_path = "/data/homeassistant"

def add_power_off(mac, name):
    yaml = open(ha_path + "/automation/power_off_" + mac + ".yaml", 'w')
    plug_name = mac + "_plug"
    sensor_name = mac + "_energy"

    print("# " + name, file=yaml)
    print("alias: power_off_" + mac, file=yaml)
    print("description: 'Power off for " + name + "'", file=yaml)
    print("trigger:", file=yaml)
    print("  - below: '15'", file=yaml)
    print("    entity_id: sensor." + sensor_name, file=yaml)
    print("    for: 00:10:00", file=yaml)
    print("    platform: numeric_state", file=yaml)
    print("condition:", file=yaml)
    print("  - condition: state", file=yaml)
    print("    entity_id: switch." + plug_name, file=yaml)
    print("    state: 'on'", file=yaml)
    print("action:", file=yaml)
    print("  - data: {}", file=yaml)
    print("    entity_id: switch." + plug_name, file=yaml)
    print("    service: switch.turn_off", file=yaml)

    yaml.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 power_off.py mac_address friendly_name")
        exit()

    mac = sys.argv[1].lower()
    friendly_name = sys.argv[2]
    add_power_off(mac, friendly_name)