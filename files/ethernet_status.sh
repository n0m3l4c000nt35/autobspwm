#!/bin/sh

echo " %{F#fff}$(/usr/sbin/ifconfig interface | grep "inet " | awk '{print $2}')"