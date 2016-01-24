from __future__ import print_function
from mycall import call

call('df -h')
call('sudo -i apt-get update')
call('sudo -iapt-get install --reinstall libraspberrypi0 \
        libraspberrypi-bin \
        libraspberrypi-dev \
        libraspberrypi-doc \
        raspberrypi-bootloader')
print('System will now reboot...')
call('sudo -i reboot')
