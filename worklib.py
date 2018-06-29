from pims import TiffStack
import numpy as np
from PyQt5 import QtCore,QtWidgets,QtGui
import cv2
import read_roi
import matplotlib.pyplot as plt
from read_roi import read_roi_zip, read_roi_file
"""
useful docs:
pims:   http://soft-matter.github.io/pims/v0.4/
numpy:  https://docs.scipy.org/doc/numpy/reference/
opencv: https://docs.opencv.org/3.3.1/d6/d00/tutorial_py_root.html
matplotlib: https://matplotlib.org/

can't help you with finding pyqt resources, most are private, pyside is illegible.
I recommend using http://gen.lib.rus.ec/ to find some useful books maybe.
"""


"""
In case of headaches when working with the orderedDicts from the read_roi library:
for some roi-set rois:
Formatting:
{name_roi1,name_roi2...name_roiN} where name_roiI is of str()
accessing:
rois[name_roiI][property] where property is of str()

Looking for magic wand rois?
Tough luck, but you can sort down to their relevant category:
relevant = {}
for roi in rois.keys():
    relevant[roi] = filter(lambda roiprop: roiprop=='freehand',rois[roi]['type'])

"""


#The following class should be initialized in any opening of a tiff stack for python work
class TiffStacks(TiffStack): #parent class is credit to pims, gives slicing and iteration, as well as lazyloading and other useful things
    def __init__(self,filename: str,frame=0,rois = None):
        super(TiffStacks,self).__init__(filename)
        self.rois = rois #rois are loaded as orderedDict type, more info in relevant methods
        self.name = filename #name preserved for debugging objects
        self.contrast = 10 #generic multiplier
        self._frame = self[frame] #private copy for methods 
        self.currentframe =  (self[frame]*self.contrast*(255./65535)).astype(np.uint8) #squeezes into a 8bit view (numpy array) 

    def roi_view(self,highlight=(150,0,0)):
        #all rois are loaded as individual ordered lists of items, labelled with an index
        #in our case the read_roi package reads them in with the indices being the messy imagej made ones
        #this makes direct iteration (and avoiding loops in general) difficult :(
        if not self.rois:
            raise FileNotFoundError #if no rois are loaded, raise error
        
        mask = np.stack([np.zeros(self._frame.shape,dtype=self._frame.dtype)]*3,axis=-1)#adds color channels for highlight color
        #in this method we are just writing all the rois overtop of a copy of the image array 
        for roi in self.rois:
            roo = self.rois[roi]
            view[roo['x'],roo['y']] += highlight
        #this isn't the best method to do this as you'll likely create a lot of memory leakage
        #however its the only method right now that should consistently work without any key and index issues
        return mask
    

    
                
            
    




#Controller class is an idea credited to this example: https://gist.github.com/MalloyDelacroix/2c509d6bcad35c7e35b1851dfc32d161
#essentially automates hooking sockets to other windows
class Controller(dict):
    def __init__(self,windowclasses):
        super(Controller,self).__init__()
        '''
        Why make a class to do this?
        python is awful at being run in separate threads and talking to those other threads
        and pyqt isn't quite mature enough in documentation so I did research and figured 
        if I wanted to make this work in a non-hairpulling way, I'd make a class for it.
        If it weren't for my own ineptitude I'd abstract this to a meta-class but maybe thats 
        a good exercise for the reader of this code.

        What does it do?
        allows a developer to create a simple crosstalk between pyqt windows that doesn't break
        the pyqt event-handler or strain python (too badly) through the usage of signals and dicts.

        What do I do after initializing it?
        feed in all your qt window classes you'll be using like in the below init.
        Do note however that I haven't quite come up with a not-so invasive way of setting up signals
        to appear inside the class without passing them upon init, so after initializing in some portion
        of code, flag it with some kinda comment and then write the needed connection in the talking
        classes with the same flag.
        '''
        #self[mainWindow().__class__.__name__] = mainWindow()

    def show_window(self,window:'Window Class', wargs = None): #generalized show fn for the windows#
        if window.__class__.__name__ in self or window:
            pass
        else:
            raise Exception("Named class not found")
        """
        below is an example model where all the relevant windows speak to some main window 
        """
        #self[window.__class__.__name__] = window(wargs)
        #self[window.__class__.__name__].connect_to_main.connect(self['main']._show())
        #self[window.__class__.__name__].show()
        raise NotImplementedError
        
