<h1>Raspberry Pi Pico and ESP-01 layout for the app controll project</h1>
<p>This small project aimed to establish the Internet connection for Raspberry Pi Pico (like its W version), to make a device, that can be controlled from an external app on a desktop or mobile.</p>

<p>To implement this I used the ESP-01 module with ESP-8266 microcontroller. The communication is done via the UART interface and AT commands. The <b>espsocketlib.py</b> implements a class, that is used to configure the esp device through the UART and to use it for example like a SoftAP (wi-fi hotspot) with a given SSID and password. Also, it can connect to existing hotspots. All these features are implemented, to obtain data transferring by the use of TCP protocol, with a command and the data to be processed(in the class the command and the data are merged in a single string, which will be transferred).</p>

<h2>The board circuitry</h2>

<table>
  <tr>
    <th>Raspberry Pi Pico</th>
    <th>ESP-01</th>
  </tr>
  <tr>
    <td><img src="images_rpi_esp/rpi_pico.jpg" width="200" alt="RPI Pico"/></td>
    <td><img src="images_rpi_esp/esp01.jpg" width="200" alt="ESP-01"/></td>
  </tr>
</table>

<p>The circuit board was designed to be a layout board, for making projects with such a "hybrid" of RPI Pico and ESP-01. To make it able to detach the raspberry pi and the esp. Connection is established by the goldpins.</p>

<img src="images_rpi_esp/board.jpeg" width="300" alt="Board outlook"/>

<p>The RGB diode, near the ESP, used for indication of the ESP status:</p>
<ul>
  <li>blue - SoftAP mode</li>
  <li>blinking blue - connecting to wi-fi</li>
  <li>green - connected to wi-fi</li>
  <li>red - failed to connect to wi-fi</li>
</ul>
<p>Also, there is there are 2 buck step-down converters. Their outputs are connected to the powerlines on the right side (the 5-volt line is bigger). The first converter's feedback resistance is configured in the way, that it outputs the 3.3V. The second converter is configured to output 5 volts(only if there is an additional external power supply, which has greater than 5 volts voltage). If there is no need for additional power supply</p>

<h2>Project applications</h2>
<p>One of the project applications was to make a full-duplex transferring protocol, on the basis of TCP transfer protocol, to connect the Raspberry Pi Pico to devices, acting like TCP servers, and to control the Raspberry Pi Pico through the desktop or a phone app.</p>
<p>To do the app, I used a Godot4 game engine, which allows to export the same project for different platforms and also has the ability to manipulate on TCP connection manually. To use this kind of connection, I wrote the ESP plugin for the engine.</p>

<p>The circuitry for the example implementation is:</p>
<img src="images_rpi_esp/circuitry.jpeg" alt='The circuitry'/>
<p>The potentiometer was connected to 3V power line, and its output is connected to one of Raspberry Pi Pico ADC pins (GPIO 28). The 2nd RGB LED is connected to last pins (GPIO 18, 17 and 16). The RGB color is set by 3 PWM, regulating the brightness of each color in the diode. In a perfect case, the RGB diode should have had 3 different input resistances for each color, but, concerning it firstly as a prototype, it is a negligible issue.</p>
<p> The Godot program works in the way, that it accepts the signals, coming from the potentiometer, to rotate a 3d object. Also, it in the same time sends the hex value of a color, which is on the color picker. The "ESP circuit plugin" works in the way that it is attached to the main tree and used as a TCP server. When there is any data collected (the number of available bytes is not zero), the module calls a signal, to transfer the accepted string of command and the data. </p>
<p>The usage:</p>
<img src='images_rpi_esp/working.gif' alt="Circuit in work"/>
<p>One of the advantages of using Godot4 for this purpose, is an ability of being exported on any platform (Android, Linux, IOS, MacOS, Web and etc.)</p>
