import time
from pimoroni import Button, RGBLED
import machine
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.8)
display.set_font("bitmap6")

led = RGBLED(6, 7, 8)
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
BLUE = display.create_pen(10, 220, 252)
RED = display.create_pen(252, 21, 0)
YELLOW = display.create_pen(252, 223, 2)

paused = False

def convert(seconds):
    minutes = int(seconds / 60)
    seconds = int(seconds % 60)
    return str(minutes)+":"+str('{0:02d}'.format(seconds))


# sets up a handy function we can call to clear the screen
def clear(color):
    display.set_pen(color)
    display.clear()
    display.update()

def work(timer):
    global paused
    seconds = timer
    clear(RED)
    led.set_rgb(252, 21, 0)
    display.set_pen(WHITE)
    display.text("WORK", 86, 90, 240, 3)
    for second in range(timer):
        display.set_pen(WHITE)
        display.text(convert(seconds), 59, 40, 240, 6)
            
        display.update()
        time.sleep(1)
            
        display.set_pen(RED)
        display.rectangle(10, 30,300,50)
        if button_y.read():
            if paused == True:
                paused = False
                led.set_rgb(252, 21, 0)
            else:
                paused = True
                led.set_rgb(0, 0, 0)
        if paused == True:
            pass
        else:
            seconds -= 1

def rest(timer):
    seconds = timer
    clear(BLUE)
    led.set_rgb(10, 220, 252)
    display.set_pen(WHITE)
    display.text("BREAK", 76, 90, 240, 3)
    for second in range(timer):
        display.set_pen(WHITE)
        display.text(convert(seconds), 70, 40, 240, 6)
            
        display.update()
        time.sleep(1)
            
        display.set_pen(BLUE)
        display.rectangle(10, 30,300,50)
        seconds -= 1

# set up
clear(YELLOW)

while True:
    if button_a.read():
        # 5 Minutes
        work(300)
        rest(120)
        machine.reset()
    elif button_b.read():
        # 15 Minutes
        work(900)
        rest(300)
        machine.reset()
    elif button_x.read():
        # 10 Minutes
        work(600)
        rest(300)
        machine.reset()
    elif button_y.read():
        # 25 Minutes
        work(1500)
        rest(300)
        machine.reset()
    else:
        display.set_pen(WHITE)
        led.set_rgb(252, 131, 2)
        fs = 3
        display.text("5 MINS", 10, 20, 240, fs)
        display.text("15 MINS", 10, 95, 240, fs)
        
        display.text("10 MINS", 130, 20, 240, fs)
        display.text("25 MINS", 125, 95, 240, fs)
        display.update()
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
