import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
import sys
import time

# Objeto de captura de audio
class AudioStream(object):
    def __init__(self):
        self.chunk = 1024 *2
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 48000 #Fs
        self.pause = False
        
        # Captura de audio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            output=True,
            frames_per_buffer=self.chunk
        )
        self.init_plots()
        self.start_plot()
