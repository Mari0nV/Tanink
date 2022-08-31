# Tanink

Writing software for Raspberry PI zero W and e-Paper screen IT8951 10.3.

## Setup

- Connect the Raspberry PI to a screen, keyboard and mouse (using a HUB if needed).
- Turn it on and connect it to your wifi.
- Get the IP address of your raspberry PI by opening a console and typing ifconfig.
- On your PC, connect to the Raspberry PI through SSH.
```
ssh pi@192.168.XX.XX
```
- Clone the Tanink package and install it
- ```sudo python3 tanink/main.py``` to launch the software on the E-ink screen.

In VSCode:
- Install SSH FS extension
- Create new configuration with SSH info (put "/home/pi/Projects" in root)
- Click on Add as workspace folder

To test outside E-ink screen:
replace ```AutoEPDDisplay``` by ```VirtualEPDDisplay``` in main.py
