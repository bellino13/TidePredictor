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

system('sudo -i apt-get -y install apache2 apache2-doc apache2-utils')
system('sudo -i apt-get -y install libapache2-mod-php5 php5 php-pear php5-xcache')
