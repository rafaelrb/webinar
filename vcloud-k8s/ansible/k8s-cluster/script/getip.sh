#!/bin/bash

DEV=$(ip r | grep  default | awk -F 'dev' '{print $2}' | awk '{print $1}')

ip a | egrep "^.*inet.*[0-9]+\.[0-9]+\..*$DEV" | awk '{print $2}' | awk -F '/' '{print $1}'
