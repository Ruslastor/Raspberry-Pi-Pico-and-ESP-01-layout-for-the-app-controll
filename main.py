from espsocketlib import *
import random

pot_pin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
pot_on_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)

esp = ESPSocket(debug=True)

esp.create_wifi_spot('ESP_TEST_WIFI', '12345566789')


client_began = False

while True:
    if pot_pin.value():
        print(esp.read())
        esp.send(str(random.randint(101,999)))
    if not(client_began) and pot_on_pin.value():
        esp.begin_tcp_client('0.0.0.0', 8080)
        client_began = True
    if not(pot_on_pin.value()):
        client_began = False
    
esp.close()
