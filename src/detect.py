import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
import sys
import time

# Objeto de captura de audio
class AudioStream(object):
    # Constructor de la clase AudioStream
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

    def init_plots(self):
        # x e y para la graficacion
        x = np.arange(0,2*self.chunk, 2)
        y = np.linspace(0, self.rate, self.chunk)

        # figura con dos graficos
        self.fig, (timeG, freqG) = plt.subplots(2, figsize=(15,7))
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)

        # limite de la grafica tiempo
        timeG.set_title("Dominio del Tiempo")
        timeG.set_ylabel=("Amplitud")
        timeG.set_ylim(-10000, 10000)
        timeG.set_xlim(0, 2*self.chunk)
        plt.setp(
            timeG, yticks=[0],
            xticks=[0, self.chunk, 2*self.chunk]
        )

        # limite de la grafica frecuencia
        timeG.set_title("Dominio de la Frecuencia")
        timeG.set_ylabel=("Amplitud")
        timeG.set_xlabel=("Frecuencia")
        timeG.set_xlim(20, self.rate/12)
        timeG.set_xlim(0, 2*self.chunk)
        plt.setp(
            timeG, yticks=[0, 5, 15, 20],
            xticks=[0, 100, 200, 300, 1000, 3000, 4000]
        )

        # Mostrar la ventana
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry = (5, 120, 1910, 1070)
        plt.show(block=False)

    # Graficas en tiempo real
    def start_plot(self):

        print("stream started")
        frame_count = 0
        start_time = time.time()

        while not self.pause:
            # tomar valores desde el microfono
            data = self.stream.read(self.chunk)

            # pasar los valores leidos a tipo int
            data_int = np.frombuffer(data, dtype="h")

            # valores en un arreglo
            data_np = np.array(data_int, dtype="h")

            # agregando los valores a la grafica de tiempo
            self.line.set_ydata(data_np)

            # Calculo de la transformada rapida de fourier
            yf = np.fft.fft(data_int)

            # pasar los valores en frecuencia a la grafica
            self.line_fft.set_ydata(
                np.abs(yf[0:self.chunk])/ (128 * self.chunk)
            )

            # identificar el pico de frecuncia en el vector
            f_vec = self.rate*np.arange(self.chunk/2)/self.chunk
            mic_low_freq = 40
            low_freq_loc = np.argmin(np.abs(f_vec-mic_low_freq))
            fft_data = (np.abs(np.fft.fft(data_int))[0:int(np.floor(self.chunk/2))])/self.chunk

            # pico mas alto en frecuencia
            max_loc = np.argmax(fft_data[low_freq_loc:])+low_freq_loc

            # Detecciomn de nota musical 
            if 980 <= f_vec[max_loc] <= 990:
                