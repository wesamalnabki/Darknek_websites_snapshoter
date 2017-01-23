# Darknek_websites_snapshoter
A python project to take a snapshot from darknet TOR (*.onion) websites as png file (full, page, thumb)
This project was token from a thread on Stackoverflow (http://stackoverflow.com/questions/1197172/how-can-i-take-a-screenshot-image-of-a-website-using-python)
I adapted it to work over a list of darknet website and be able to access via a proxt.
I have the code in .py and .ipynb.

## To use it, you should: 
    '''
        Requirements:
        Install NodeJS
        Using Node's package manager install phantomjs: npm -g install phantomjs
        install selenium
        install imageMagick 
        add phantomjs to system path (on windows)
    '''
    
 ## Important note:
 
 In order to use the code, you should install TOR browser on your system. 
 For Debien 8:
 
 You need to add the following entry in /etc/apt/sources.list or a new file in /etc/apt/sources.list.d/:

deb http://deb.torproject.org/torproject.org jessie main
deb-src http://deb.torproject.org/torproject.org jessie main


Then add the gpg key used to sign the packages by running the following commands at your command prompt:

gpg --keyserver keys.gnupg.net --recv A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89
gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -
You can install it with the following commands:

$ apt-get update
$ apt-get install tor deb.torproject.org-keyring

To Start/ Stop the service:
sudo service tor stop
sudo service tor start

To remove TOR:
apt-get remove tor
sudo apt-get remove --auto-remove tor
sudo apt-get purge tor
sudo apt-get purge --auto-remove tor

Note: Sometime TOR stuck opening the port 9050:
sudo netstat -plnt | fgrep 9050

to kill it, use:
sudo killall tor

    
    
