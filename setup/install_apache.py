from __future__ import print_function
from mycall import call

call('sudo -i apt-get -y install apache2 apache2-doc apache2-utils apache2-dev')
call('sudo -i apt-get -y install libapache2-mod-wsgi libapache2-mod-php5 php5 php-pear php5-xcache')
