#!/usr/bin/env python2

import rospy
from std_msgs.msg import Float64, String
import RPi.GPIO as gpio
import time

import sys
import signal

def signal_handler(signal, frame): # ctrl + c -> sai do programa
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

gpio.setmode(gpio.BCM)  # Configura o GPIO do Raspberry

trig = 27 # GPIO 27 - 7 pino do lado esquerdo
echo = 17 # GPIO 17 - 6 pino do lado esquerdo

gpio.setup(trig, gpio.OUT)  # sinal de saida
gpio.setup(echo, gpio.IN)  # sinal de entrada

class SensorSonar:

    def __init__(self):
        self.publisher_sonar = rospy.Publisher('/sonar', Float64, queue_size=10)  # cria um publisher
        self.timer = rospy.Timer(rospy.Duration(0.2), self.sonar_env)  # publica a informacao a cada 0.2 segundos

    # funcao do calculo de distancia
    def sonar_env(self, event):

        gpio.output(trig, False)
        time.sleep(0.1)
        gpio.output(trig, True)
        time.sleep(0.00001)
        gpio.output(trig, False)
        while gpio.input(echo) == 0 :
            pulse_start = time.time()
        while gpio.input(echo) == 1 :
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        msg = Float64()
        msg.data = distance
        self.publisher_sonar.publish(msg)


if __name__ == '__main__':
    try:
        rospy.init_node('sensor_publisher')  # cria o no
        SensorSonar()  # chama a classe SensorSonar
        rospy.spin()  # impede que o no seja encerrado sozinho
    except rospy.ROSInterruptException:
        gpio.cleanup()
        pass
    except (KeyboardInterrupt, SystemExit):
        gpio.cleanup()
    except:
        gpio.cleanup()
