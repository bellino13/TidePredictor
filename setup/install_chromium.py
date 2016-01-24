from __future__ import print_function
from mycall import call

url = 'https://dl.dropboxusercontent.com/u/87113035'
ver = '45.0.2454.85-0ubuntu0.15.04.1.1181'
browser_all = 'chromium-browser-l10n_{}_all.deb'.format(ver)
browser_armhf = 'chromium-browser_{}_armhf.deb'.format(ver)
codecs = 'chromium-codecs-ffmpeg-extra_{}_armhf.deb'.format(ver)

call('wget {}/{}'.format(url, browser_all))
call('wget {}/{}'.format(url, browser_armhf))
call('wget {}/{}'.format(url, codecs))
call('dpkg -i {}'.format(codecs))
call('dpkg -i {} {}'.format(browser_all, browser_armhf))
call('sudo -i apt-get -y install x11-xserver-utils unclutter')


