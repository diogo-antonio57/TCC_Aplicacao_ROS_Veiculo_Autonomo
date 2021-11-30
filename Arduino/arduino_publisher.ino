#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Empty.h>

ros::NodeHandle slave_arduino;  // instancia o node Handle

std_msgs::Float64 msg_btn1;  // instacia as variaveis com o tipo de mensagem
std_msgs::Float64 msg_btn2;

std_msgs::Float64 msg_pot1;
std_msgs::Float64 msg_pot2;

ros::Publisher arduino_btn1("sensor1", &msg_btn1);  // inicia um publicador com o nome do topico de sensor1
ros::Publisher arduino_btn2("sensor2", &msg_btn2);

ros::Publisher arduino_pot1("throttle_position", &msg_pot1);
ros::Publisher arduino_pot2("engine_speed", &msg_pot2);

int pot1 = A0;
int pot2 = A1;
int btn1 = 2;
int btn2 = 4;

int led1 = 3;
int led2 = 5;
int led3 = 6;

// funcao chamada ao receber um subscriber
void sonar_aviso(const std_msgs::Float64& toggle_msg){
  float objeto = toggle_msg.data;  // recebe os dados da mensagem
  if(objeto == 1.0){
    digitalWrite(led3, HIGH);
    }
    else{
      digitalWrite(led3, LOW);
    }
  }

ros::Subscriber<std_msgs::Float64> sub("led_ultrasonic", &sonar_aviso);  // cria um assinante do topico led_ultrasonic e chama a fucao sonar_aviso

void setup() {
  // put your setup code here, to run once:
  
  slave_arduino.initNode();  // inicia o identificador do no ROS

  // anuncia todos os topicos que estao sendo publicados e assina todos os topicos que deseja ouvir
  slave_arduino.advertise(arduino_btn1);
  slave_arduino.advertise(arduino_btn2);
  slave_arduino.advertise(arduino_pot1);
  slave_arduino.advertise(arduino_pot2);
  slave_arduino.subscribe(sub);

  // declara os pinos
  pinMode(2, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

  // le as informacoes dos sensores e guardam nas mensagens que serao postadas
  if (digitalRead(btn1) == LOW){
    msg_btn1.data = 1;
    digitalWrite(led1, HIGH);
  }
  else{
    msg_btn1.data = 0;
    digitalWrite(led1, LOW);
  }
  
  if (digitalRead(btn2) == LOW){
    msg_btn2.data = 1;
    digitalWrite(led2, HIGH);
  }
  else{
    msg_btn2.data = 0;
    digitalWrite(led2, LOW);
  }
  
  slave_arduino.spinOnce();

  float valor_pot = analogRead(pot1);
  msg_pot1.data = valor_pot;
  
  float valor_pot2 = analogRead(pot2);
  msg_pot2.data = valor_pot2;

  // publica as mensagens
  arduino_btn1.publish( &msg_btn1 );
  arduino_btn2.publish( &msg_btn2 );
  
  arduino_pot1.publish(&msg_pot1);
  arduino_pot2.publish(&msg_pot2);

  delay(200);
}
