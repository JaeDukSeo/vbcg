#!/usr/bin/env python
# gui.py - GUI element: frame that displays video

import Tkinter as Tk
import threading
import Image
import ImageTk
import time

# Initialize global variables
root = None

class WindowVideo(Tk.Frame):
    # In this frame the video stream is shown

    def __init__(self, parent, tk_root, thread, cam):

        # Store variables
        global root
        self.root = tk_root

        # Save camera object
        self.cameraInstance = cam

        # Save thread object
        self.threadInstance = thread

        # Create GUI
        self.__create_gui()

        # Start frame display as thread
        self.frameCounter = 0
        self.displayThread = threading.Thread(target=self.__showImage)
        self.displayThread.start()

        # Start FPS computation thread
        self.FPS = 0
        self.frameCounterLastValue = 0
        self.fpsCounterThread = threading.Thread(target=self.__computeFPS)
        self.fpsCounterThread.start()

    def __create_gui(self):
        # Create GUI elements and add them to root widget

        self.video_frame = Tk.Frame(root, width=500, height=400)
        self.video_frame.config(background="gray")
        self.video_frame.pack()
        self.lmain = Tk.Label(self.video_frame)
        self.lmain.pack()

    def __showImage(self):
        # Get frame from camera and display it

        self.isTrueFrame, self.frame = self.cameraInstance.getFrame()
        if self.isTrueFrame:
            self.frameCounter += 1
        self.frameConverted = Image.fromarray(self.frame)
        self.imgTK = ImageTk.PhotoImage(image=self.frameConverted)
        self.lmain.imgtk = self.imgTK
        self.lmain.configure(image=self.imgTK)
        # Repeat thread
        self.lmain.after(1, self.__showImage)

    def __computeFPS(self):
        #if self.get_frameCounter()>0:
        self.FPS = self.get_frameCounter()-self.frameCounterLastValue
        self.frameCounterLastValue = self.get_frameCounter()

        # Repeat thread
        self.video_frame.after(1000, lambda: self.__computeFPS())

    def get_frameCounter(self):
        return self.frameCounter

    def get_FPS(self):
        return str(self.FPS)