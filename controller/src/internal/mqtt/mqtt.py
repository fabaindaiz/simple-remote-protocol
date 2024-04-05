import adafruit_connection_manager
from internal.network import NetworkLoader
from adafruit_minimqtt.adafruit_minimqtt import MQTT

KEEP_ALIVE = 5

class MQTTClient():
    def __init__(self, will_set_topic, mqtt_config):
        self._network = NetworkLoader().network
        socket_pool = adafruit_connection_manager.get_radio_socketpool(self._network.interface)
        ssl_context = adafruit_connection_manager.get_radio_ssl_context(self._network.interface)

        self._mqtt_client = MQTT(
            socket_pool=socket_pool,
            ssl_context=ssl_context,
            **mqtt_config)
        
        self._mqtt_client.on_connect = self._on_connect
        self._mqtt_client.on_disconnect = self._on_disconnect

        self._mqtt_client.will_set(will_set_topic, "", 0)
        self.connect()
    
    def _on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT server")

    def _on_disconnect(self, client, userdata, result):
        print("Disconnected from MQTT server")

    def connect(self):
        self._mqtt_client.connect(keep_alive=KEEP_ALIVE)

    def disconnect(self):
        self._mqtt_client.disconnect()

    def publish(self, topic, data):
        self._mqtt_client.publish(topic, data)
    