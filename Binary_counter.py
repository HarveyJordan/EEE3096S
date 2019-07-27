
#imports
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
#configre gpio to output/input
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.IN)
GPIO.setup(37, GPIO.IN) #increment down

print("Starting")
i=0
#lookup
pins=[29,31,33]

def upIncrement(arg):
    #check whether number wrap is required else increment 
    global i
    if(i>=7):
        i=0
    else:
        i+=1
    gpioUpdate()

def dwnIncrement(arg):
    #check whether number wrap is required else increment
    global i
    if(i<=0):
        i=7
    else:
        i-=1
    gpioUpdate()

def gpioUpdate():
    for p in pins:
        GPIO.output(p,False); #turn all LEDs off
            
    out = bin(i)[2:] #convert integer to binary
    for j in range(len(out)-1, -1, -1): #iterate through binary number
        GPIO.output(pins[len(out)-j-1], int(out[j])) #set the correct GPIO pin high    

def main():
    #add event detection for button presses
    i=0
    GPIO.add_event_detect(35, GPIO.RISING, callback=upIncrement, bouncetime=300)  # add rising edge detection on pin 35 with debouncing
    GPIO.add_event_detect(37, GPIO.RISING, callback=dwnIncrement, bouncetime=300)  # add rising edge detection on pin 37 with debouncing
    print("Ready")
    
    while(True):
        time.sleep(0.1) #small delay

# Only run the functions if
if __name__ == "__main__":
    # Make sure the GPIO is stopped correctly
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Exiting gracefully")
        # Turn off your GPIOs here
        GPIO.cleanup()
    except:
        print("Some other error occurred")