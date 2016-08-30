#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_gui.py - tests for all GUI elements"""


import unittest
import nose
import video
import gui
import Tkinter as tk

from nose.tools import assert_is_instance


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize GUI and GUI elements """

        # Create video thread
        self.videoThread = video.VideoThread()
        self.videoThread.start()

        # Create GUI
        self.guiThread = gui.GUI()
        self.mainWindow = gui.MainWindow(self.guiThread, self.videoThread)

        # Get TK root widget
        self.root = self.mainWindow.getRoot()

        # Obtain GUI elements
        self.toolbar_roi = self.mainWindow.getToolbarROI()
        self.toolbar_buttons = self.mainWindow.getToolbarButtons()
        self.statusbar = self.mainWindow.getStatusbar()
        self.winSignal = self.mainWindow.getSignalDisplay()
        self.winVideo = self.mainWindow.getVideoDisplay()

    @classmethod
    def tearDownClass(self):
        """Destroy GUI"""

        # Close threads
        self.videoThread.closeCameraThread()
        self.winSignal.closeSignalPlotterThread()

        # Close root widget
        self.root.quit()
        self.root.destroy()

        # Todo: Fix RuntimeError by Tkinter (RuntimeError: main thread is not in main loop)

    def test_gui_getStatusbar(self):
        assert_is_instance(self.mainWindow.getStatusbar(), gui.Statusbar)

    def test_gui_getToolbarButtons(self):
        assert_is_instance(self.mainWindow.getToolbarButtons(), gui.ToolbarButtons)

    def test_gui_ToolbarROI(self):
        assert_is_instance(self.mainWindow.getToolbarROI(), gui.ToolbarROI)

    def test_gui_ToolbarROI_check_values(self):
        """Check if ROI values are well-defined """
        ret_1, ret_2, ret_3, ret_4 = self.toolbar_roi.getROI()
        assert_is_instance(ret_1, int)
        assert_is_instance(ret_2, int)
        assert_is_instance(ret_3, int)
        assert_is_instance(ret_4, int)

    def test_gui_VideoDisplay(self):
        assert_is_instance(self.mainWindow.getVideoDisplay(), gui.WindowVideo)

    def test_gui_VideoDisplay_check_frameCounter(self):
        """Check if number of frames is well-defined"""
        ret_1 = self.winVideo.get_frameCounter()
        assert_is_instance(ret_1, int)

    def test_gui_SignalDisplay(self):
        assert_is_instance(self.mainWindow.getSignalDisplay(), gui.WindowSignal)

    def test_gui_Root(self):
        assert_is_instance(self.mainWindow.getRoot(), tk.Tk)

if __name__ == '__main__':
    nose.main()