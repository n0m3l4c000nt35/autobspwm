#!/bin/bash

ip_address=$(/bin/cat ~/.config/bin/target | awk '{print $1}')
machine_name=$(/bin/cat ~/.config/bin/target | awk '{print $2}')

if [ $ip_address ] && [ $machine_name ]; then
  echo " %{F#fff}$ip_address%{u-} - $machine_name"
else
  echo "%{u-}%{F#fff} No target"
fi