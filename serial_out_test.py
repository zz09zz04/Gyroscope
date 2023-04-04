import serial                       # import serial module, PySerial 3.5 

COM_PORT = 'COM3'                     # assign communication port name
BAUD = 115200                         # set baud

ser = serial.Serial(COM_PORT, BAUD)   # initialize serial port

while True:
    data_raw = ser.readline()  
    data = data_raw.decode(errors = "ignore")   # UTF-T decode
    data = data.rstrip()    print('ser.in_waiting=',end='')
    print(ser.in_waiting)
    print(data)
