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
from multiprocessing import Process

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
				   

COM_PORT = 'COM15'                     # assign communication port name
BAUD = 115200                         # set baud

#ser = serial.Serial(COM_PORT, BAUD)   # initialize serial port

offset_alpha, offset_beta, offset_gamma = 0, 0, 0

def get_angles_from_uart():
    while ser.in_waiting:          # receive serial data...
        data_raw = ser.readline()  
        data = data_raw.decode(errors = "ignore")   # UTF-T decode
        #print('接收到的原始資料：', data_raw)
        data = data.rstrip()
        print(data)
        alpha, beta, gamma = data.split(' ')
        #f.write(data, end='')
        print ("test")
        return (alpha, beta, gamma)
    print("Some error happened when get angles from uart!")
    return 0, 0, 0

def update_plot(frame_number, z, plot):
    print (frame_number)
    alpha = 1
    beta = 0
    gamma = 0
    while ser.in_waiting:          # receive serial data...
        data_raw = ser.readline()  
        data = data_raw.decode(errors = "ignore")   # UTF-T decode
        #print('接收到的原始資料：', data_raw)
        data = data.rstrip()
        print(data)
        if len(data.split(' ')) == 3:
            alpha, beta, gamma = data.split(' ')
            try:
                alpha = float(alpha)
                beta = float(beta)
                gamma = float(gamma)
            except ValueError:
                pass
                
        #f.write(data, end='')
        print ("test")
    alpha=frame_number
    for j in range(len(x)):
        #print(np.matrix([x[j], y[j], z[j]]) * Rx(i))
        temp = np.matrix([x[j], y[j], z[j]]) * Rz((float(alpha)-float(offset_alpha))*m.pi/180) * Ry((float(gamma)-float(offset_gamma))*m.pi/180) * Rx((float(beta)-float(offset_beta))*m.pi/180)
        #print(data)
        _x[j] = temp[0,0]
        _y[j] = temp[0,1]
        _z[j] = temp[0,2]
    plot[0].remove()
    plot[0] = ax.plot_trisurf(_x, _y, _z, triangles = [[0, 1, 2], [1, 2, 3], [2, 3, 0], [3, 0, 1]], color="Blue")

def update_offset():
    print ("update_offset\n")
    global offset_alpha, offset_beta, offset_gamma
    while ser.in_waiting:          # receive serial data...
        data_raw = ser.readline()  
        data = data_raw.decode(errors = "ignore")   # UTF-T decode
        #print('接收到的原始資料：', data_raw)
        data = data.rstrip()
        print(data)
        if len(data.split(' ')) == 3:
            offset_alpha, offset_beta, offset_gamma = data.split(' ')
            try:
                offset_alpha = float(offset_alpha)
                offset_beta = float(offset_beta)
                offset_gamma = float(offset_gamma)
            except ValueError:
                pass        #f.write(data, end='')
        print ("test")
        print(offset_alpha, offset_beta, offset_gamma)

def detect_hotkey():
    kb.add_hotkey("ctrl+u", update_offset)

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
    
#    thread = threading.Thread(target = detect_hotkey)
#    thread.start()
#    thread.join()

    p = Process(target = detect_hotkey)
    p.start()

    ser = serial.Serial(COM_PORT, BAUD)   # initialize serial port

    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')    

    # create object
    width = 3

    n = width / (2 ** 0.5) * 0.5;

    x = np.array([n, -n,  n, -n]) 
    y = np.array([n,  n, -n, -n]) 
    z = np.array([n, -n, -n, n]) 

    # plot object
    #plot = [ax.plot_surface(x, y, zarray[:,:,0], color='0.75', rstride=1, cstride=1)]
    plot = [ax.plot_trisurf(x, y, z, triangles = [[0, 1, 2], [1, 2, 3], [2, 3, 0], [3, 0, 1]])]


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

    p.join()    

