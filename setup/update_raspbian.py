import sys
import commands

def system(cmd):
    failure, output = commands.getstatusoutput(cmd)
    if failure:
        print('Command {} failed.'.format(cmd))
        print(output)
        sys.exit(1)
    else:
        print(output)

system('df -h')
system('sudo -i apt-get update')
system('sudo -iapt-get install --reinstall libraspberrypi0 \
        libraspberrypi-bin \
        libraspberrypi-dev \
        libraspberrypi-doc \
        raspberrypi-bootloader')
print('System will now reboot...')
system('sudo -i reboot')
