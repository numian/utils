#!/bin/bash


# some ubuntu bug workaround
nmcli nm wifi off
rfkill unblock wlan

# turn on ip forward
sysctl -w net.ipv4.ip_forward=1

# turn on wifi
ifconfig wlan0 192.168.150.1/24 up

# iptables rules
iptables --append FORWARD --in-interface wlan0 -j ACCEPT
iptables --table nat --append POSTROUTING --out-interface wwan0 -j MASQUERADE

# restart services
service dnsmasq restart
service hostapd restart

