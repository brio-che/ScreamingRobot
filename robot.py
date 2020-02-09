import sys
import time
import pygame
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library

GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

pygame.mixer.init()
pygame.mixer.music.load("Test2.wav")

TRIG = 23                                  #Associate pin 23 to TRIG
ECHO = 24                                  #Associate pin 24 to ECHO

print("Distance measurement in progress")

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in


def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

getch = _find_getch()

# Setup the library ready for use
import ThunderBorg# Load the library
TB = ThunderBorg.ThunderBorg()         # Create a board object
TB.Init()                              # Setup the board

# Setting motor speeds
power = 0.5

rotatepower = 0.45

def forward():
  TB.SetMotor1(power)
  TB.SetMotor2(-power)

def backward():
  TB.SetMotor1(-power)
  TB.SetMotor2(power)

def left():
  TB.SetMotor1(-rotatepower)
  TB.SetMotor2(-rotatepower)

def right():
  TB.SetMotor1(rotatepower)
  TB.SetMotor2(rotatepower)

def stop():
  TB.MotorsOff()

def test():
  forward()
  time.sleep(2)

  left()
  time.sleep(5)

  stop()

while True:
  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  print("Waiting For Sensor To Settle")
  time.sleep(0.5)                            #Delay of 2 seconds

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                      #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
    pulse_start = time.time()              #Saves the last known time of LOW pulse

  while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
    pulse_end = time.time()                #Saves the last known time of HIGH pulse 

  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            #Round to two decimal points

  if distance > 2 and distance < 25:      #Check whether the distance is within range
    print("Distance:",distance - 0.5,"cm")  #Print distance with 0.5 cm calibration
    pygame.mixer.music.play()
  else:
    print("Out Of Range")                   #display out of range
    
  c = getch()

  if c == 'q':
    break

  print(c)

  if c == 's':
    stop()
  elif c == 'f':
    forward()
  elif c == 'b':
    backward()
  elif c == 'l':
    left()
  elif c == 'r':
    right()
