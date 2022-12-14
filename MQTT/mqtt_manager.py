################################################################
# import 순서      
# 
# urls.py -> views.py -> mqtt_manager.py 로 차례로 임포팅 되어 실행됨
#
################################################################
from mongoDB.mongoDB_manager import MongoDBManager
import paho.mqtt.client as mqtt

BROKER_IP = "localhost" 
DEVICE_ROOT_TOPIC = "dev/#"

COLLECTION_NAME = "SensorValue"

def printMQTTstate(msg):
    print("MQTT> " + msg)

def on_connect(client, userdata, flags, conn_state):
    printMQTTstate("connected with result code : " + str(conn_state))
    if(conn_state == 0):
        printMQTTstate("succeed to connect to broker")
    else:
        printMQTTstate("failed to connect to broker")

    printMQTTstate("server wait for receiving msg from device...")


def on_message(client, userdata, msg):

    value = float(msg.payload.decode()) 
    _, device_name, msg_info = msg.topic.split('/')
    
    sensor_msg = {
        'Device Name' : device_name,
        'Value' : value
    }

    MongoDBManager().add_data(sensor_msg, COLLECTION_NAME)
    
    if(msg_info == "Data"):
        printMQTTstate("received data msg from " + device_name + ", value : " + str(value))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER_IP)
    client.subscribe(DEVICE_ROOT_TOPIC)           # 반드시 subscribe 함수를 호출해주어야 on_message가 호출됨
    client.loop_start()
except Exception as err:
    printMQTTstate("error occured while connect to broker")
