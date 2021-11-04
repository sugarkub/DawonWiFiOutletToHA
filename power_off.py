import sys

ha_path = "/data/homeassistant"

def add_power_off(mac, name):
    plug_name = mac + "_plug"
    sensor_name = mac + "_energy"

    lines = []
    lines.append("# " + name)
    lines.append("alias: power_off_" + mac)
    lines.append("description: 'Power off for " + name + "'")
    lines.append("trigger:")
    lines.append("  - below: '15'")
    lines.append("    entity_id: sensor." + sensor_name)
    lines.append("    for: 00:10:00")
    lines.append("    platform: numeric_state")
    lines.append("condition:")
    lines.append("  - condition: state")
    lines.append("    entity_id: switch." + plug_name)
    lines.append("    state: 'on'")
    lines.append("action:")
    lines.append("  - data: {}")
    lines.append("    entity_id: switch." + plug_name)
    lines.append("    service: switch.turn_off")

    yaml = open(ha_path + "/automation/power_off_" + mac + ".yaml", 'w')
    yaml.writelines('\n'.join(lines))
    yaml.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 power_off.py mac_address friendly_name")
        exit()

    mac = sys.argv[1].lower()
    friendly_name = sys.argv[2]
    add_power_off(mac, friendly_name)