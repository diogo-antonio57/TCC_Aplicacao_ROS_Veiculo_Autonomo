#!/usr/bin/env python2

import rospy
from std_msgs.msg import Float64, String
import time

class sensors_subscriber:
    def __init__(self):
        self.cont = 0
	self.pot1 = 0
	self.pot2 = 0
	self.btn1 = 0
	self.btn2 = 0
	self.sensor = 0

        self.pot1 = rospy.Subscriber('/throttle_position', Float64, self.get_pot1)  # subscreve no topico throttle_position e ao receber algo chama a funcao self.get_pot1
	self.pot2 = rospy.Subscriber('/engine_speed', Float64, self.get_pot2)  # subscreve no topico engine_speed e ao receber algo chama a funcao self.get_pot2
	self.btn1 = rospy.Subscriber('/sensor1', Float64, self.get_btn1)  # subscreve no topico sensor1 e ao receber algo chama a funcao self.get_btn1
	self.btn2 = rospy.Subscriber('/sensor2', Float64, self.get_btn2)  # subscreve no topico sensor2 e ao receber algo chama a funcao self.get_btn2
	self.sonar = rospy.Subscriber('/sonar', Float64, self.get_sonar)  # subscreve no topico sonar e ao receber algo chama a funcao self.get_sonar
	rospy.loginfo("Subscriber set")  # informa que os subscribers foram setados

        self.status_pub = rospy.Publisher('/led_ultrasonic', Float64, queue_size=5)  # cria a publicacao led_ultrasonic para o arduino
        rospy.loginfo("Publisher set")  # informa que foi setado

    # Funcao do throttle position
    def get_pot1(self, msg):
	self.pot1 = msg.data  # receber a informacao do topico

    # Funcao do engine speed
    def get_pot2(self, msg):
	self.pot2 = msg.data

    # Funcao do sensor1
    def get_btn1(self, msg):
	self.btn1 = int(msg.data)
	if self.btn1 == 1:
	    self.btn1 = "ligado"
	else:
	    self.btn1 = "desligado"

    # Funcao do sensor2
    def get_btn2(self, msg):
	self.btn2 = int(msg.data)  
	if self.btn2 == 1:
	    self.btn2 = "ligado"
	else:
	    self.btn2 = "desligado"

    # Funcao do sonar
    def get_sonar(self, mesage):
	self.sonar = float(mesage.data)
	
	# caso o obstaculo esteja a menos de 8 cm ira informar que ha algo perto
	if self.sonar < 8:
	    self.sonar = "objeto perto"
	    msg = Float64()
	    msg.data = 1.0
	    self.status_pub.publish(msg)
	else:
	    self.sonar = "seguro"
	    msg = Float64()
	    msg.data = 0.0
	    self.status_pub.publish(msg)

	self.show_status()  # chama funcao que informara os dados dos sensores

    # Funcao que imprimi na tela as informacoes
    def show_status(self):
	rospy.loginfo("\n" +
		      "throttle_position: " + str(self.pot1) + "\n" +
		      "engine_speed: " + str(self.pot2) + "\n" +
		      "sensor1: " + str(self.btn1) + "\n" +
		      "sensor2: " + str(self.btn2) + "\n" +
		      "sonar: " + str(self.sonar))

	time.sleep(0.100)
	

    def status_env(self, event):
        msg = Float64()
        msg.data = self.status
        self.status_pub.publish(msg)

if __name__ == '__main__':
    try:
        rospy.init_node('sensors_subscriber')  # cria o no sensor_subscriber
        sensors_subscriber()  # chama a classe
        rospy.spin()  # impede que o no seja encerrado sozinho
    except rospy.ROSInterruptException:
        pass
