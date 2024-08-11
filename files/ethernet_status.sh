#!/bin/sh

echo " %{F#fff}$(/usr/sbin/ifconfig ens33 | grep "inet " | awk '{print $2}')"