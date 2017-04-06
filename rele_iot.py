# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt


Broker = "iot.eclipse.org"
PortaBroker = 1883
KeepAliveBroker = 60
TopicoSubscribe = "flisoliot2017/lampada"
RELE = 12

def configure():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RELE, GPIO.OUT)


def on_connect(client, userdata, flags, rc):
    print("Conectado ao Broker. Resultado: "+ str(rc))
    client.subscribe(TopicoSubscribe)
    

def on_message(client, userdata, msg):
    print("Mensagem recebida do tópico: " + msg.topic + ". Mensagem: " + str(msg.payload))
    mensagemRecebida = str(msg.payload)
    if(mensagemRecebida):
       print("entrou 1")
       turnLight(mensagemRecebida)
       

def turnLight(mensagemRecebida):
    if (str(mensagemRecebida) == "1"):
        print("entrou 2")
        GPIO.output(RELE, GPIO.LOW)
        #time.sleep(2)
        #GPIO.output(RELE, GPIO.LOW)


try:
        print("Inicializando o MQTT...")
        configure()
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(Broker, PortaBroker, KeepAliveBroker)
        client.loop_forever()
except KeyboardInterrupt:
        print("Encerranddo a aplicação")
        GPIO.cleanup()
