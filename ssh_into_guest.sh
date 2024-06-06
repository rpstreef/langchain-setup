#!/bin/bash

# We deploy to the 'default' machine, if you have more machines, replace the machine name here.
machine_name="langflow"

# Using VirtualBox CLI to get the bridged network IP address
guest_machine_ip=$(VBoxManage guestproperty get "$machine_name" "/VirtualBox/GuestInfo/Net/1/V4/IP" | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')

# Default vagrant username
username="vagrant"

# SSH private key location
private_key="./.vagrant/machines/$machine_name/virtualbox/private_key"

ssh -i "$private_key" "$username@$guest_machine_ip"