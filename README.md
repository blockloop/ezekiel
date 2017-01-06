# Ezekiel

> So heap on the wood and kindle the fire. Cook the meat well, mixing in the spices; and let the bones be charred. – Ezekiel 24:10

![](https://cdn.rawgit.com/blockloop/ezekiel/master/ss.png)

This is my attempt at making my Raspberry PI a BBQ companion. With a thermocouple, my Raspberry PI, and my Amazon Echo I created something that I've always wanted. 

>  Me: "Alexa, ask my grill the temperature."
>
> Alexa: 245 degrees

## Credit

I want to give credit to [Rafael Troncoso](https://www.cyberhades.com/2015/04/21/termometro-para-barbacoa-ahumador-horno-con-raspberry-pi/) for the initial hardware and software setup. [His video](https://www.youtube.com/watch?v=tx0H9_cJFyg) on youtube was what initially inspired me to get started.

***Note to the wary and the critical***: I am not a hardware professional. I have soldered maybe twice in my life. I managed to get these parts soldered together because I remembered some things by father tought me. Perhaps they aren't true. Perhaps I am doing it wrong. Nevertheless, I had fun and got the outcome I wanted. The longevity of the solution is still to be determined 😉

## Hardware Requirements

1. Raspberry PI: I used an original Model B from 2012
2. [Thermocouple Type-K Glass Braid Insulated – $9.95](https://www.adafruit.com/products/270)
3. [Thermocouple Amplifier MAX31855 – $14.95](https://www.adafruit.com/products/269)
4. [Female/Male 'Extension' Jumper Wires – $3.95](https://www.adafruit.com/products/826)
5. [Tiny breadboard – $4.00](https://www.adafruit.com/products/65)



![](https://dl.dropbox.com/s/oruxre15f7lsccg/Screenshot%202017-01-01%2012.39.44.png)

## Raspberry Pi Setup

I'm going to assume you're using [Raspian](https://www.raspberrypi.org/downloads/raspbian/). If you're using something else then YMMV. Either SSH or use a keyboard/monitor connected to the PI. In a terminal window perform the following.

```Bash
sudo raspi-config
# choose advanced options > SPI > enable. 
sudo reboot
# after reboot
# install dependencies
sudo apt install build-essential python-dev python-pip python-smbus git
sudo pip install RPi.GPIO
# Install adafruit libs
mkdir -p ~/tmp
cd ~/tmp
git clone https://github.com/adafruit/Adafruit_Python_MAX31855.git
cd Adafruit_Python_MAX31855
sudo python setup.py install
# this will install the Adafruit python libs
```

## Hardware Instructions

The wiring schematics can be found at [adafruit.com](https://learn.adafruit.com/max31855-thermocouple-python-library/hardware). I used the hardware SPI model pasted below for ease. 

![](https://cdn-learn.adafruit.com/assets/assets/000/019/767/large1024/temperature_pi-hardwarespi-max31855_bb.png?1411071293)

I was under the assumption that I could connect the pieces without solder and get a reading, but I was sadly mistaken. I was able to hold the amplifier in a certain position and get a reading, but it was in and out. I was having trouble getting a good connection without solder. If you don't know how to solder then I suggest you do some searching on YouTube. It's really simple. 

* Solder the thermocouple onto the short end of the headers (the six pins)
* Solder the 2 pin terminal block onto the top of the thermocouple with the open holes facing away from the board
* Tighten the terminal block screws all the way and then loosen them a bit for the wires to fit in
* Insert the K-type thermocouple (the braided wire) to the terminal block with the yellow on the left and the red on the right. 

## Installing Ezekiel

Connect to the PI again and perform the following.

```bash
mkdir -p /var/www
sudo chown -r $(WHOAMI) /var/www
cd /var/www
git clone https://github.com/blockloop/ezekiel.git
cd ezekiel
python probe_reader/test.py
# you sould see the following output if the probe reads properly
#  Probe: 72
#  External: 81
```

If you don't see real temperatures then you may have a problem with connections. Check your solder, the thermocouple wire connections, make sure the screws on the terminal are tight, etc. 

```bash
sudo cp lib/systemd/system/* /lib/systemd/system/
sudo systemctl enable /lib/systemd/system/probe_updatedb.py
sudo systemctl enable /lib/systemd/system/probe_updatedb.timer
sudo systemctl enable /lib/systemd/system/probe_http.py
```





## Future Goals

1. Add a display
2. Add a simple UI with a graphs and historical information