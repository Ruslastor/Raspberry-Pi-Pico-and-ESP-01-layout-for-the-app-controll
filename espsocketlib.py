import machine
import utime

class ESPSocket:

    
    MAX_CONNECTION_TIME = 20000
    def __init__(self, uart=0, debug=False, show_transmition=False):
        self.wifi_ssid = ''
        self.wifi_pword = ''
        self.tcp_server_ip = ''
        self.tcp_server_port = 0
        self.debug = debug
        self.show_transmition = show_transmition
        self.last_sent_data = ''
        
        self.rgb_red = machine.Pin(2, machine.Pin.OUT)
        self.rgb_green = machine.Pin(3, machine.Pin.OUT)
        self.rgb_blue = machine.Pin(4, machine.Pin.OUT)
    
        self.uart = machine.UART(uart, baudrate=115200)
        
        self.reset_rgb()
    
    def uart_send(self, message, relax_time=0):
        self.uart.write(message.encode('utf-8'))
        if relax_time > 0:
            utime.sleep_ms(relax_time)
        if self.debug:
            print('From ESP: ', self.uart.read())
    def create_wifi_spot(self,wifi_ssid, wifi_pword):
        self.reset_rgb()
        
        self.wifi_ssid = wifi_ssid
        self.wifi_pword = wifi_pword
        self.uart_send('AT+CWMODE=2\r\n', relax_time=1000)
        self.uart_send('AT+RESTORE\r\n', relax_time=1000)
        self.uart_send(f'AT+CWSAP="{wifi_ssid}","{wifi_pword}",11,3,1\r\n', relax_time=5000)
        
        self.rgb_blue.value(1)
    
    def connect_to_wifi(self, wifi_ssid, wifi_pword):
        self.reset_rgb()
        self.wifi_ssid = wifi_ssid
        self.wifi_pword = wifi_pword
        self.uart_send('AT+CWMODE=1\r\n', relax_time=1)
        self.uart_send('AT+CWJAP="' + self.wifi_ssid + '","' + self.wifi_pword + '"\r\n', relax_time=100)
        used_time = 0
        while not(self.is_ok()):
            self.rgb_blue.value(1)
            utime.sleep_ms(300)
            self.reset_rgb()
            utime.sleep_ms(300)
            used_time += 600
            if used_time >= ESPSocket.MAX_CONNECTION_TIME:
                if self.debug:
                    print('From ESP: Failed to connect')
                self.rgb_red.value(1)
                return False
                
        self.rgb_green.value(1)
        if self.debug:
            print(f'From ESP: Connected after {used_time} miliseconds')
        return True
    def is_ok(self):
        data = self.uart.read()
        if not(data):
            return False
        print(data.decode('utf-8'))
        if 'OK' in data.decode('utf-8'):
            return True
        return False
            
    def get_wifi_adresses(self):
        self.uart_send('AT+CIPSTA?\r\n', relax_time=1)
        
    def begin_tcp_client(self, ip, port):
        self.tcp_server_ip = ip
        self.tcp_server_port = port
        self.uart_send('AT+CIPSTART="TCP","'+ self.tcp_server_ip +'",'+ str(self.tcp_server_port) +'\r\n', relax_time=1000)
        
        
    def send(self, data):
        if data != self.last_sent_data:
            self.uart.write(('AT+CIPSEND='+str(len(data))+'\r\n').encode('utf-8'))
            utime.sleep_ms(150)
            self.uart.write(data.encode('utf-8'))
            utime.sleep_ms(100)
            self.uart.write(b'+++')
            utime.sleep_ms(150)
            self.last_sent_data = data
    def set_reading(self):
        self.uart.write(b'AT+CIPRECVMODE=0')
    def read(self):
        data = self.uart.read()
        if data:
            data = data.decode('utf-8')
            if 'IPD' in data:
                return data.split(':')[-1][:-2]
        return None
    def read_via_command(self):
        data = self.uart.write('AT+CIPRECVDATA=100')
        return self.uart.read().decode('utf-8')
    def reset(self):
        self.uart_send('AT+RST\r\n',relax_time=2000)
    def close(self):
        self.uart_send('AT+CIPCLOSE\r\n', relax_time=2000)
    def reset_rgb(self):
        self.rgb_red.value(0)
        self.rgb_green.value(0)
        self.rgb_blue.value(0)