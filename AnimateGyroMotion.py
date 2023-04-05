'''
https://stackoverflow.com/questions/45712099/updating-z-data-on-a-surface-plot-in-matplotlib-animation


Python 3.8.13 (default, May 20 2022, 16:23:54) [MSC v.1916 64 bit (AMD64)] :: Intel Corporation on win32

'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.animation as animation

import math as m

import serial                       # import serial module, PySerial 3.5 
from datetime import datetime       # import time module

import threading
#from multiprocessing import Process

import keyboard as kb

import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, m.cos(theta),-m.sin(theta)],
                   [ 0, m.sin(theta), m.cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ m.cos(theta), 0, m.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-m.sin(theta), 0, m.cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ m.cos(theta), -m.sin(theta), 0 ],
                   [ m.sin(theta), m.cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])
				   

COM_PORT = 'COM3'                     # assign communication port name
BAUD = 115200                         # set baud

#ser = serial.Serial(COM_PORT, BAUD)   # initialize serial port

offset_alpha, offset_beta, offset_gamma = 0, 0, 0


class GetAnagles:
    def __init__(self, comport, baud):
        self.comport = comport
        self.baud = baud

        try:
            self.ser = serial.Serial(self.comport, self.baud)   # initialize serial port
        except:
            print('Open serial port error\n')
            pass

    def get_angles(self):
        while True:
            self.data_raw = self.ser.readline()  
            self.data = self.data_raw.decode(errors = "ignore")   # UTF-T decode
            self.data = self.data.rstrip()
            print("ser.in_waiting=",end="")
            print(self.self.ser.in_waiting)
            print(self.data)
            if len(data.split(' ')) == 3:
                alpha, beta, gamma = data.split(' ')
                try:
                    self.alpha = float(alpha)
                    self.beta = float(beta)
                    self.gamma = float(gamma)
                except ValueError:
                    print("Get Angles data failed\n")
                    pass

    def update_base_angles(self):
        return self.alpha, self.beta, self.gamma

def update_plot(frame_number, z, plot):
    #print (frame_number)
#    alpha = 1
#    beta = 0
#    gamma = 0
#    alpha, beta, gamma = get_angles_from_serial()
#    while ser.in_waiting:          # receive serial data...
#        data_raw = ser.readline()  
#        data = data_raw.decode(errors = "ignore")   # UTF-T decode
#        data = data.rstrip()
#        print(data)
#        if len(data.split(' ')) == 3:
#            alpha, beta, gamma = data.split(' ')
#            try:
#                alpha = float(alpha)
#                beta = float(beta)
#                gamma = float(gamma)
#            except ValueError:
#                pass
                
        #f.write(data, end='')
#    print ("test")
    #alpha=frame_number
    for j in range(len(x)):
        #print(np.matrix([x[j], y[j], z[j]]) * Rx(i))
        temp = np.matrix([x[j], y[j], z[j]]) * Rz((float(self.alpha)-float(offset_alpha))*m.pi/180) * Ry((float(self.gamma)-float(offset_gamma))*m.pi/180) * Rx((float(self.beta)-float(offset_beta))*m.pi/180)
        #print(data)
        _x[j] = temp[0,0]
        _y[j] = temp[0,1]
        _z[j] = temp[0,2]
    plot[0].remove()
    #plot[0] = ax.plot_trisurf(_x, _y, _z, triangles = [[0, 1, 2], [1, 2, 3], [2, 3, 0], [3, 0, 1]], color="Blue")
    plot[0] = ax.plot_trisurf(_x, _y, _z, linewidth=0.2, antialiased=True, cmap="magma")

def update_offset(angles):
    print ("update_offset\n")
    global offset_alpha, offset_beta, offset_gamma
    offset_alpha, offset_beta, offset_gamma = angles.update_base_angles()
#    while ser.in_waiting:          # receive serial data...
#        data_raw = ser.readline()  
#        data = data_raw.decode(errors = "ignore")   # UTF-T decode
#        data = data.rstrip()
#        print(data)
#        if len(data.split(' ')) == 3:
#            offset_alpha, offset_beta, offset_gamma = data.split(' ')
#            try:
#                offset_alpha = float(offset_alpha)
#                offset_beta = float(offset_beta)
#                offset_gamma = float(offset_gamma)
#            except ValueError:
#                pass        #f.write(data, end='')
#        print ("test")
    print(offset_alpha, offset_beta, offset_gamma)

#def detect_hotkey():
#    kb.add_hotkey("ctrl+u", update_offset)

def on_key_press(event):
    print("you pressed {}".format(event.key))
    update_offset()
#    key_press_handler(event, canvas, toolbar)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

'''
N = 14
nmax=20
x = np.linspace(-4,4,N+1)
x, y = np.meshgrid(x, x)
zarray = np.zeros((N+1, N+1, nmax))

f = lambda x,y,sig : 1/np.sqrt(sig)*np.exp(-(x**2+y**2)/sig**2)

for i in range(nmax):
    zarray[:,:,i] = f(x,y,1.5+np.sin(i*2*np.pi/nmax))
'''

if __name__ == '__main__':
    
    angles = GetAnagles(COM_PORT, BAUD)
    thread = threading.Thread(target = angles.get_angles)
    thread.start()


#    p = Process(target = detect_hotkey)
#    p.start()
#    try:
#        ser = serial.Serial(COM_PORT, BAUD)   # initialize serial port
#    except:
#        print('Open serial port error\n')
#        pass

    root = tkinter.Tk()
    root.wm_title("Gyroscope Motion Animation")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')    

    # create object
    n_radii = 8
    n_angles = 100

    # Make radii and angles spaces (radius r=0 omitted to eliminate duplication).
    radii = np.linspace(0.125, 1.0, n_radii)
    angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)[..., np.newaxis]

    # Convert polar (radii, angles) coords to cartesian (x, y) coords.
    # (0, 0) is manually added at this stage,  so there will be no duplicate
    # points in the (x, y) plane.
    x = np.append(0, (radii*np.cos(angles)).flatten())
    y = np.append(0, (radii*np.sin(angles)).flatten())

    # Compute z to make the pringle surface.
    z = np.sin(-x*y)

    # plot object
    #plot = [ax.plot_surface(x, y, zarray[:,:,0], color='0.75', rstride=1, cstride=1)]
    #plot = [ax.plot_trisurf(x, y, z, triangles = [[0, 1, 2], [1, 2, 3], [2, 3, 0], [3, 0, 1]])]
    plot = [ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True)]


    _x = np.zeros(len(x))
    _y = np.zeros(len(x))
    _z = np.zeros(len(x))

    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_zlim(-2,2)
    animate = animation.FuncAnimation(fig, update_plot, 360, fargs=(z, plot), interval = 100)
#    plt.show()
    
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    canvas.mpl_connect("key_press_event", on_key_press)

    button = tkinter.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tkinter.BOTTOM)
    
    tkinter.mainloop()

#    p.join()    
    thread.join()


