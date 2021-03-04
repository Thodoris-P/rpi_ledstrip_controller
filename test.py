import pigpio
from time import sleep

red = 22
blue = 27
green = 23

pi = pigpio.pi()
while True:
    for duty in range(255):
        pi.set_PWM_dutycycle(blue, duty)
        sleep(0.05)
    for duty in range(255, 0, -1):
        pi.set_PWM_dutycycle(blue, duty)
        sleep(0.05)
        #pi.set_PWM_dutycycle(red, 200)
        #pi.set_PWM_dutycycle(green, 0)

pi.stop
