#!/usr/bin/env python

import subprocess
import optparse # untuk bisa menggunakan --help atau shortcut
import re

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC Address")
	parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
	#parser.parse_args()
	(options, arguments) = parser.parse_args()

	#interface = options.interface # cara pemanggilan parser
	#new_mac = options.new_mac # cara pemanggilan parser

	if not options.interface:
		parser.error("[-] Please specify an interface, use --help for more info.")
	elif not options.new_mac:
		parser.error("[-] Please specify an new_mac, use --help for more info.")
	return options

def change_mac(interface, new_mac):
	print("[+] Changing mac address for " + interface + " to " + new_mac)

	#subprocess.call("ifconfig " + interface + " down", shell=True)
	#subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
	#subprocess.call("ifconfig " + interface + " up", shell=True)

	# untuk menghandle inputan user ketika menambahkan perintah tambahan
	# ketika ada perintah tambahan maka perintah tambahan tersebut akan masuk(digabung) kedalam
	# perintah yang terlah ditetapkan, bukan menjalankan ke perintah baru.

	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface])
	#print(ifconfig_result)

	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("[-] Could not read MAC address.")

# harus menggunakan python3
# jika ingin menggunakan python2 maka harus pake raw_input

#interface = input("interface > ")
#new_mac = input("new MAC > ")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
	print("[+] MAC address was successfully changed to " + current_mac)
else:
	print("[-] MAC address did not changed")