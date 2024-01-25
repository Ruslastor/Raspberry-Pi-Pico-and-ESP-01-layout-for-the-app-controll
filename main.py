from espsocketlib import *


adc = machine.ADC(machine.Pin(28))


# Create a PWM object
rgb_red = machine.PWM(machine.Pin(18))
rgb_green = machine.PWM(machine.Pin(17))
rgb_blue = machine.PWM(machine.Pin(16))

# Set the frequency of the PWM signal (Hz)
rgb_red.freq(1000)
rgb_green.freq(1000)
rgb_blue.freq(1000)



esp = ESPSocket(debug=True)

#esp.create_wifi_spot('ESP_TEST_WIFI', '12345566789')

esp.connect_to_wifi('BoatOne','sasibibulah')
esp.begin_tcp_client('192.168.204.33', 12345)

def duty_from_2bhex(hx):
    return int((int(hx,16)/255) * 65535)

while True:
    reading = esp.read()
    esp.send('RO',str(adc.read_u16()))
    
    if not(reading):
        continue
    print(reading)
    command, data = reading
    if command == 'SC':
        print(data, ' ', data[:2], data[2:4], data[4:6])

        rgb_red.duty_u16(duty_from_2bhex(data[:2]))
        rgb_green.duty_u16(duty_from_2bhex(data[2:4]))
        rgb_blue.duty_u16(duty_from_2bhex(data[4:6]))
        
esp.close()

