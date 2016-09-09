#!/usr/bin/env python
# -*- coding: ascii -*-
"""gui.py - the main GUI class that contains all GUI elements"""

from gui_statusbar import Statusbar
from gui_toolbarROI import ToolbarROI
from gui_toolbarButtons import ToolbarButtons
from gui_windowVideo import WindowVideo
from gui_windowSignal import WindowSignal
from defines import __version__

from sys import platform

import cv2
import numpy as np
import Tkinter as Tk
import logging
import settings
import datetime

# Create root widget
root = Tk.Tk()

# Set title in navigation bar
root.wm_title("vbcg " + str(__version__))


class GUI(object):
    """This is the main class of the gui. Here, we use Tkinter for thread management"""

    def start(self, video_thread):
        """Create GUI"""
        print "Entered start()"
        print datetime.datetime.now()

        # Store camera thread
        print "Store camera thread"
        print datetime.datetime.now()
        self.cameraThread = video_thread
        logging.info("Link to thread that delivers video frames was stored in GUI thread")

        # Create Window
        print "Create main window"
        print datetime.datetime.now()
        self.main_window = MainWindow(self, self.cameraThread)
        logging.info('Main window was created')

        # If we are under windows, we need an OpenCV window so that waitKey() works...
        print "Check if under windows"
        print datetime.datetime.now()

        if platform == "win32":
            img = np.zeros((150, 600, 3), np.uint8)
            cv2.putText(img, 'Please do not close this window', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(img, '     (minimizing is okay!)     ', (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.namedWindow("win")
            cv2.imshow("win", img)

        # Start Tkinter thread
        print "Check if in testing"
        print datetime.datetime.now()
        if settings.determine_if_under_testing() is False:
            print "This should not appear when using tests"
            print datetime.datetime.now()
            logging.info('Starting TkInter main loop')
            root.mainloop()

        print "reached end of start()"
        print datetime.datetime.now()


    def get_window(self):
        """Returns the main window"""
        return self.main_window

    def clear(self):
        """Deletes main window and then quits Tkinter mainloop()"""
        self.main_window.clear()
        root.quit()
        root.destroy()


class MainWindow(object):
    """This class contains all GUI elements of the main window"""

    def __init__(self, gui_thread, video_thread):

        self.statusbar = Statusbar(self, root)
        logging.info('Created status bar')

        self.toolbar_roi = ToolbarROI(self, root)
        logging.info('Created toolbar for ROI definition')

        self.video_display = WindowVideo(self, root, gui_thread, video_thread, self.toolbar_roi, self.statusbar)
        logging.info('Created part of the GUI that shows video')

        self.signal_display = WindowSignal(self, root, gui_thread, video_thread, self.statusbar, self.video_display)
        logging.info('Created part of the GUI that shows the signal extracted from the video')

        self.toolbar_buttons = ToolbarButtons(self, root, gui_thread, video_thread, self.signal_display)
        logging.info('Created toolbar with buttons')

    def clear(self):
        """"Delete all GUI elements"""
        self.statusbar.clear()
        self.toolbar_buttons.clear()
        self.toolbar_roi.clear()
        self.video_display.clear()
        self.signal_display.clear()

    # Getter (for unit tests only)

    def get_statusbar(self):
        """Returns statusbar"""
        return self.statusbar

    def get_toolbar_buttons(self):
        """Returns toolbar with buttons"""
        return self.toolbar_buttons

    def get_toolbar_roi(self):
        """Returns ROI toolbar"""
        return self.toolbar_roi

    def get_video_display(self):
        """Returns video display window"""
        return self.video_display

    def get_signal_display(self):
        """"Returns signal display window"""
        return self.signal_display

    @staticmethod
    def get_root():
        """Return Tkinter root widget"""
        return root
