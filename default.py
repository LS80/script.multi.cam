import os
import time
import urllib
import glob

import xbmc, xbmcaddon, xbmcgui, xbmcvfs


ACTION_PREVIOUS_MENU = 10
ACTION_BACKSPACE = 110
ACTION_NAV_BACK = 92
ACTION_STOP = 13

__addon__ = xbmcaddon.Addon()

data_path = xbmc.translatePath(__addon__.getAddonInfo('profile'))
black = os.path.join(__addon__.getAddonInfo('path'), 'resources', 'media', 'black.png')

COORDS = ((0, 0, 640, 360),
          (640, 0, 640, 360),
          (0, 360, 640, 360),
          (640, 360, 640, 360))

def get_urls():
    for i in range(1, 5):
        url = __addon__.getSetting("url{0}".format(i))
        if url:
            yield url

def file_fmt():
    return os.path.join(data_path, "{0}.{{0}}.jpg".format(time.time()))


urls = list(get_urls())

class CamView(xbmcgui.WindowDialog):
    def __init__(self):
        self.addControl(xbmcgui.ControlImage(0, 0, 1280, 720, black))
        
        self.image_controls = []
        
        image_file_fmt = file_fmt()
        for i, (coords, url) in enumerate(zip(COORDS, urls)):
            image_file = image_file_fmt.format(i)
            urllib.urlretrieve(url, image_file)
            control = xbmcgui.ControlImage(*coords, filename=image_file, aspectRatio=2)
            self.image_controls.append(control)
            self.addControl(control)
        
        self.closing = False
        
    def __enter__(self):
        return self
        
    def onAction(self, action):
        if action in (ACTION_PREVIOUS_MENU, ACTION_BACKSPACE, ACTION_NAV_BACK, ACTION_STOP):
            self.stop()
            
    def start(self):
        self.show()
        while(not self.closing):
            image_file_fmt = file_fmt()
            for i, (url, image_control) in enumerate(zip(urls, viewer.image_controls)):
                image_file = image_file_fmt.format(i)
                urllib.urlretrieve(url, image_file)
                image_control.setImage(image_file, useCache=False)
            xbmc.sleep(500)
            
    def stop(self):
        self.closing = True
        self.close()
        
    def __exit__(self, exc_type, exc_value, traceback):
        for f in glob.glob(os.path.join(data_path, "*.jpg")):
            os.remove(f)


with CamView() as viewer:
    viewer.start()

del viewer
