import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to changer its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify an new mac, use --help for more info")
    return options

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def ger_current_mac(interface):
    ifconfig_result = str(subprocess.check_output(["ifconfig", interface]))

    mac_adress_surch_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_adress_surch_result:
        return mac_adress_surch_result.group(0)
    else:
        print("[-] Could nod read MAC address. ")


options = get_arguments()
current_mac = ger_current_mac(options.interface)
print("Current MAC = " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = ger_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac address was succssefully changed to " + current_mac)
else:
    print("[-] Mac address did not get changed")
