import serial
import threading
import RPi.GPIO as GPIO
import time

port = '/run/zao/ttyZAOV1'
baudrate = 115200

sw1 = 21
sw2 = 20
sw3 = 26 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup([sw1, sw2, sw3], GPIO.OUT, initial=GPIO.LOW)
time.sleep(1)

def read_serial(ser):
    global stop
    while True:
        if ser.in_waiting > 0:
            message = ser.readline().decode('utf-8').rstrip()
            print("Received message:", message)
            #split with :
            color, onoff = message.split(':')
            target = None
            print("color:", color, "onoff:", onoff)
            if color == 'r':
                target = sw1
            elif color == 'y':
                target = sw2
            elif color == 'b':
                target = sw3
            
            if target:
                if onoff == '1':
                    GPIO.output(target, GPIO.HIGH)
                elif onoff == '0':
                    GPIO.output(target, GPIO.LOW)
        

ser = serial.Serial(port, baudrate, timeout=1)

print("Serial port open waiting for data:", ser.name)

thread = threading.Thread(target=read_serial, args=(ser,))
thread.start()
