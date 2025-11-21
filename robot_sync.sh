#!/bin/bash

function sync_rsync() {
	rsync --rsh="sshpass -p robots1234 ssh -l pi" -av --exclude-from=.gitignore project pi@192.168.50.5:/home/pi/master-bakers/bakers-pi-final/
}

function sync_scp() {
	scp -pr project --rsh="sshpass -p robots1234 ssh -l pi" pi@192.168.50.5:/home/pi/master-bakers/bakers-pi-final/
}

function ssh_pi() {
	sshpass -p robots1234 ssh pi@192.168.50.5
}
