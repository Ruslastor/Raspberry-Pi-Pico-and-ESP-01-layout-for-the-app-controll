<h1>ESP-01 and raspberry pi pico combination project</h1>
<p>The aim of this small project was to establish the Internet connection for Raspberry Pi Pico (like its W version). To implement this I used the ESP-01 module with ESP-8266 microcontroller. The communication is done via UART interface, and AT commands. The espsocketlib implemets a class, that is used to configure the esp device through the UART, and to use it for example lika an SoftAP (wi-fi hotspot) with given SSID and password. Also, it can connect to existing hotspot. All this features are implemented, to obtain a data transfering by the use of TCP protocol.</p>

<img />
