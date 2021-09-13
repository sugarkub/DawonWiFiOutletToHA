import sys

ha_path = "/data/homeassistant"

def add_power_off(mac, name):
    yaml = open(ha_path + "/automation/power_off_" + name + ".yaml", 'w')

    print("alias: power_off_" + name, file=yaml)
    print("description: 'Power off for " + name + "'", file=yaml)
    print("trigger:", file=yaml)
    print("  - below: '15'", file=yaml)
    print("    entity_id: sensor." + mac + "_sensor", file=yaml)
    print("    for: 00:02:00", file=yaml)
    print("    platform: numeric_state", file=yaml)
    print("condition:", file=yaml)
    print("  - condition: state", file=yaml)
    print("    entity_id: switch." + mac + "_switch", file=yaml)
    print("    state: 'on'", file=yaml)
    print("action:", file=yaml)
    print("  - data: {}", file=yaml)
    print("    entity_id: switch." + mac + "_switch", file=yaml)
    print("    service: switch.turn_off", file=yaml)

    yaml.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 power_off.py mac_address device_name")
        exit()

    mac = sys.argv[1]
    name = sys.argv[2]
    add_power_off(mac, name)