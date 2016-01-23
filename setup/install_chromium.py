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

url = 'https://dl.dropboxusercontent.com/u/87113035'
ver = '45.0.2454.85-0ubuntu0.15.04.1.1181'
browser_all = 'chromium-browser-l10n_{}_all.deb'.format(ver)
browser_armhf = 'chromium-browser_{}_armhf.deb'.format(ver)
codecs = 'chromium-codecs-ffmpeg-extra_{}_armhf.deb'.format(ver)

system('wget {}/{}'.format(url, browser_all))
system('wget {}/{}'.format(url, browser_armhf))
system('wget {}/{}'.format(url, codecs))
system('dpkg -i {}'.format(codecs))
system('dpkg -i {} {}'.format(browser_all, browser_armhf))
system('sudo -i apt-get -y install x11-xserver-utils unclutter')


