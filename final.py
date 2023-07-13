import RPi.GPIO as GPIO
import time
from time import sleep

# Set the GPIO mode for pin numbering
GPIO.setmode(GPIO.BOARD)

crvena_sustav = 38
crvena = 18
zelena_sustav = 26
zelena = 12
zuta = 16
plava = 10
trig = 22
echo = 37
analog_pin = 8
button_on_off = 40
button_dist = 36
button1 = 32
button2 = 24

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(zuta, GPIO.OUT)
GPIO.setup(zelena, GPIO.OUT)
GPIO.setup(crvena, GPIO.OUT)
GPIO.setup(zelena_sustav, GPIO.OUT)
GPIO.setup(crvena_sustav, GPIO.OUT)
GPIO.setup(plava, GPIO.OUT)

GPIO.setup(button_on_off, GPIO.IN, pull_up_down = GPIO.PUD_UP)
ButtonState = 0

# Define a callback function on_off that toggles the ButtonState global variable when the button_on_off is pressed
def on_off(button_on_off):
    global ButtonState
    ButtonState += 1
    if ButtonState > 1:
        ButtonState = 0
    
GPIO.add_event_detect(button_on_off, GPIO.FALLING, callback=on_off, bouncetime=200)

ButtonState1 = 0
GPIO.setup(button_dist, GPIO.IN, pull_up_down = GPIO.PUD_UP)
 # Define a callback function dist that toggles the ButtonState1 global variable when the button_dist is pressed
def dist(button_dist):
    global ButtonState1
    ButtonState1 += 1
    if ButtonState > 1:
        ButtonState1 = 0

# Register the callback function for the falling edge detection of button_dist using GPIO.add_event_detect
GPIO.add_event_detect(button_dist, GPIO.FALLING, callback=dist, bouncetime=200)
# Perform a delay of 0.2 seconds for stability.
time.sleep(0.2)

# Perform LED checks by briefly turning on and off the LEDs
GPIO.output(zuta, GPIO.HIGH)
GPIO.output(zelena, GPIO.HIGH)
GPIO.output(crvena, GPIO.HIGH)
GPIO.output(zelena_sustav, GPIO.HIGH)
GPIO.output(crvena_sustav, GPIO.HIGH)
GPIO.output(plava, GPIO.HIGH)
time.sleep(3)
GPIO.output(zuta, GPIO.LOW)
GPIO.output(zelena, GPIO.LOW)
GPIO.output(crvena, GPIO.LOW)
GPIO.output(zelena_sustav, GPIO.LOW)
GPIO.output(crvena_sustav, GPIO.LOW)
GPIO.output(plava, GPIO.LOW)

GPIO.setup(button1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(analog_pin, GPIO.IN)

# rc_time function measures the time taken for a capacitor connected to the analog_pin to discharge through a photoresistor
def rc_time (analog_pin):
    count = 0

    GPIO.setup(analog_pin, GPIO.OUT)
    GPIO.output(analog_pin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(analog_pin, GPIO.IN)

    while (GPIO.input(analog_pin) == GPIO.LOW):
        count += 1

    return count

granica = 0

dupliGumb = False
def button1_callback(button1):
    global granica, dupliGumb
    if GPIO.input (button2) == GPIO.LOW:
        dupliGumb = True
        granica -= 500
    elif not dupliGumb:
        granica +=100
    else:
        dupliGumb = False
    
def button2_callback(button2):
    global granica, dupliGumb
    if GPIO.input (button1) == GPIO.LOW:
        dupliGumb = True
        granica += 500
    elif not dupliGumb:
        granica -= 100
    else:
        dupliGumb = False
    if granica < 0:
        granica = 0
       
    
GPIO.add_event_detect(button1, GPIO.RISING, callback = button1_callback, bouncetime = 200)
GPIO.add_event_detect(button2, GPIO.RISING, callback = button2_callback, bouncetime = 200)
upperBorder = 0
lowerBorder = 1000000

udaljenost = 0

try:
    while True:
                
        
        if ButtonState == 1:
            GPIO.output(zelena_sustav, GPIO.HIGH)
            GPIO.output(crvena_sustav, GPIO.LOW)
            time.sleep(0.01)
                        
            if rc_time(analog_pin) > upperBorder:
                upperBorder = rc_time(analog_pin)
                
            if rc_time(analog_pin) < lowerBorder:
                lowerBorder = rc_time(analog_pin)

            
            if granica < rc_time(analog_pin):
                GPIO.output(plava, True)
            else:
                GPIO.output(plava, False)
    

            if ButtonState1 == 0:
                    #senzor udaljenosti rad
                    GPIO.output(trig, GPIO.LOW)
                    time.sleep(2E-6)
                    GPIO.output(trig, GPIO.HIGH)
                    time.sleep(6E-10)
                    GPIO.output(trig, GPIO.LOW)
                    time.sleep(2E-6)
                    
                    while GPIO.input(echo)==0:
                        pass
                    start_time=time.time()
                    while GPIO.input(echo)==1:
                        pass
                    stop_time = time.time()
                    
                    trajanje = stop_time - start_time
                    udaljenost = round(trajanje*17150.2)
                    time.sleep(0.2)
                            
                    if udaljenost <= 15:
                        GPIO.output(crvena, GPIO.HIGH)
                        GPIO.output(zuta, GPIO.LOW)
                        GPIO.output(zelena, GPIO.LOW)
                                    
                    elif udaljenost <= 30:
                        GPIO.output(crvena, GPIO.LOW)
                        GPIO.output(zuta, GPIO.HIGH)
                        GPIO.output(zelena, GPIO.LOW)   
                    
                    elif udaljenost > 30:
                        GPIO.output(crvena, GPIO.LOW)
                        GPIO.output(zuta, GPIO.LOW)
                        GPIO.output(zelena, GPIO.HIGH)
            else:
                GPIO.output(zelena, GPIO.LOW)
                GPIO.output(crvena, GPIO.LOW)
                GPIO.output(zuta, GPIO.LOW)
                udaljenost = 0
                    
            print("Sustav: aktiviran,  Senzor svjetla: ", upperBorder, "Granica osvjtljenja: ", granica, "Udaljenost: ", udaljenost)
            time.sleep(0.5)
        
        else:
            GPIO.output(zelena_sustav, GPIO.LOW)
            GPIO.output(crvena_sustav, GPIO.HIGH)
            GPIO.output(crvena, GPIO.LOW)
            GPIO.output(zuta, GPIO.LOW)
            GPIO.output(zelena, GPIO.LOW)
            granica = 0
            upperBoarder = 0
            print("Sustav: deaktiviran, Senzor svjetla: ", upperBorder, "Granica osvjtljenja: ", granica)
            time.sleep(1)
            
# Exception Handling: Catches the KeyboardInterrupt exception to gracefully exit the program when Ctrl+C is pressed
except KeyboardInterrupt:
    pass
