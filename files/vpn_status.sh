#!/bin/sh

IFACE=$(/usr/sbin/ifconfig | grep tun0 | awk '{print $1}' | tr -d ':')

if [ "$IFACE" = "tun0" ]; then
    echo " %{F#fff}$(/usr/sbin/ifconfig tun0 | grep "inet " | awk '{print $2}')"
else
  echo " %{F#fff}Disconnected"
fi