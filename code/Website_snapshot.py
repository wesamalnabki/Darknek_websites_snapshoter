import os
from subprocess import Popen, PIPE
from selenium import webdriver

import socks
import socket

from urllib.parse import urlparse, ParseResult

import signal

ROOT = '/home/wesam/datasets/Snapshot_Result_23_01_2017/'
white_list_dir = '/home/wesam/Codes/ScrapeDeepWeb/white_list.txt'
abspath = lambda *p: os.path.abspath(os.path.join(*p))

def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)


def do_screen_capturing(url, screen_path, width, height):
    print ("Capturing screen..")
    
    service_args = [
    '--proxy=127.0.0.1:9050',
    '--proxy-type=socks5',
    ]    
    driver = webdriver.PhantomJS(service_args=service_args)
    # it save service log file in same directory
    # if you want to have log file stored else where
    # initialize the webdriver.PhantomJS() as
    # driver = webdriver.PhantomJS(service_log_path='/var/log/phantomjs/ghostdriver.log')
    driver.set_script_timeout(30)
    if width and height:
        driver.set_window_size(width, height)
    driver.get(url)
    driver.save_screenshot(screen_path)
    
    # Starting from 2016, the PhantomJS process can NOT be killed with quit() or close. 
    # Then, we must send a SIGTERM signal to stop it. 
    # Otherwise, the server will be down! 
    # Python/Linux quit() does not terminate PhantomJS process
    # https://github.com/seleniumhq/selenium/issues/767
    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()


def do_crop(params):
    print ("Croping captured image..")
    command = [
        'convert',
        params['screen_path'],
        '-crop', '%sx%s+0+0' % (params['width'], params['height']),
        params['crop_path']
    ]
    execute_command(' '.join(command))


def do_thumbnail(params):
    print ("Generating thumbnail from croped captured image..")
    command = [
        'convert',
        params['crop_path'],
        '-filter', 'Lanczos',
        '-thumbnail', '%sx%s' % (params['width'], params['height']),
        params['thumbnail_path']
    ]
    execute_command(' '.join(command))


def get_screen_shot(save_path,**kwargs):
    url = kwargs['url']
    width = int(kwargs.get('width', 1024)) # screen width to capture
    height = int(kwargs.get('height', 768)) # screen height to capture
    filename = kwargs.get('filename', 'screen.png') # file name e.g. screen.png
    path = kwargs.get('path', save_path) # directory path to store screen

    crop = kwargs.get('crop', False) # crop the captured screen
    crop_width = int(kwargs.get('crop_width', width)) # the width of crop screen
    crop_height = int(kwargs.get('crop_height', height)) # the height of crop screen
    crop_replace = kwargs.get('crop_replace', False) # does crop image replace original screen capture?

    thumbnail = kwargs.get('thumbnail', False) # generate thumbnail from screen, requires crop=True
    thumbnail_width = int(kwargs.get('thumbnail_width', width)) # the width of thumbnail
    thumbnail_height = int(kwargs.get('thumbnail_height', height)) # the height of thumbnail
    thumbnail_replace = kwargs.get('thumbnail_replace', False) # does thumbnail image replace crop image?

    #screen_path = abspath(path + '/' +filename[:-4], filename)    
    screen_path = abspath(path , filename)    
    crop_path = thumbnail_path = screen_path

    if thumbnail and not crop:
        raise Exception ('Thumnail generation requires crop image, set crop=True')

    do_screen_capturing(url, screen_path, width, height)

    if crop:
        if not crop_replace:
            crop_path = abspath(path, 'crop_'+ filename)
        params = {
            'width': crop_width, 'height': crop_height,
            'crop_path': crop_path, 'screen_path': screen_path}
        do_crop(params)

        if thumbnail:
            if not thumbnail_replace:
                thumbnail_path = abspath(path, 'thumbnail_'+filename)
            params = {
                'width': thumbnail_width, 'height': thumbnail_height,
                'thumbnail_path': thumbnail_path, 'crop_path': crop_path}
            do_thumbnail(params)
    return screen_path, crop_path, thumbnail_path

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

def return_domain_name (url):
    return '.'.join(str(urlparse(url).netloc).split('.')[0:len(str(urlparse(url).netloc).split('.'))-1])

if __name__ == '__main__':
    '''
        Requirements:
        Install NodeJS
        Using Node's package manager install phantomjs: npm -g install phantomjs
        install selenium (in your virtualenv, if you are using that)
        install imageMagick
        add phantomjs to system path (on windows)
    '''
    
    # Create a folder for the results:
    if not os.path.exists(ROOT):
        os.mkdir(ROOT)
        
    with open(white_list_dir) as reader:
        sites_list = reader.readlines()
    sites_list = [site.strip() for site in sites_list]
        
    #sites_list = ['bo4lbe6xavxbntrv.onion', 'mzmxmkivtasbzhjo.onion']
    
    for url in sites_list:
    
        print ('Processing', url)
        
        save_path = ROOT+'/'+ url
        
        # Create a folder for each domain:
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        else:
            continue
        
        # Adjust the URL by adding http://
        full_url = 'http://www.' + url

        screen_path, crop_path, thumbnail_path = get_screen_shot(
            save_path = save_path,
            url=full_url, filename='{0}.png'.format(url),
            crop=True, crop_replace=False,
            thumbnail=True, thumbnail_replace=False,
            thumbnail_width=200, thumbnail_height=150,
        )