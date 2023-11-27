Installation der Smart Modelrailway-Cam Applikation 2.0(see English Version below)
===================================================================
Voraussetzung: Raspberry Pi 4B or 5 mit 
  - PiOS (Legacy) Bullseye 64bit  oder PiOS Bookworm 64bit 
  - Python 3.9 or later
  - Raspberry Pi Camera V2

Empfohlen: Update von PiOS
- sudo apt update
- sudo apt full-upgrade

Die Installation der SmartModelrailway-Cam besteht aus:

1) Anmeldung als user "pi". 
 
2) Setup der Raspberry Pi Camera V2:
   https://projects-raspberry.com/getting-started-with-raspberry-pi-camera/

3) Zugriff auf den Pi über VNC von einem PC aus: (Achtung momentan nur mit Bullseye möglich)
   Weitere Infos: https://www.raspberrypi.com/documentation/computers/remote-access.html#vnc
   
4) Für den PC: Download des VNC Viewers:
   https://www.realvnc.com/en/connect/download/viewer/

5) Installation der MediaPipe-API:
   Siehe: https://developers.google.com/mediapipe/solutions/setup_python
   MediaPipe Version ab 0.10.8
                     
6) Download des GitHub-Repository 
   auf dem Raspberry Pi unter dem user "pi":
   https://github.com/robodhhb/Smart-Modelrailway-Cam 
   mit dem grünen Knopf "code" und dann "Download zip". 

7) Pi: LXTerminal öffnen und zip-Datei mit unzip in einem Ordner Ihrer Wahl entpacken
    und in den Ordner "40_SMRC_MediaPipe_Version" mit cd wechseln

8) Programme starten:   
   - Starten im LXTerminal mit "python3 SMRC_Main.py"
    
------------------    
Bekannte Probleme:
a)  Falls das Paket "ImageTk" nicht gefunden wird, muss es noch
    installiert werden mit:
    sudo apt install python3-pil.imagetk

b) Da das Programm mit Objekterkennung arbeitet, dürfen nicht 2 oder mehrere
   gleiche Loks in der gleichen Region (Gleis) zur gleichen Zeit fahren.
   (Klassen-)Namen von Loks müssen mit ":" beginnen.

Hinweise, Fragen, Anregungen und Ideen an:
smrc_alert@gmx.de
    
========================English Version====================================
Installation of the application "Smart Modelrailway-Cam"
--------------------------------------------
Prerequisite: Raspberry Pi 4B or 5 mit 
  - PiOS (Legacy) Bullseye 64bit  or PiOS Bookworm 64bit 
  - Python 3.9 or later
  - Raspberry Pi Camera V2
   
Recommended: Update PiOS Buster
- sudo apt update
- sudo apt full-upgrade

Installation steps:
   
1) Login as user "pi". 
 
2) Setup  Raspberry Pi Camera V2:
   https://projects-raspberry.com/getting-started-with-raspberry-pi-camera/

3) Access the Pi desktop with VNC via a PC:
   Additional info: https://www.raspberrypi.com/documentation/computers/remote-access.html#vnc

4) Foe a PC: Download des VNC Viewers:
   https://www.realvnc.com/en/connect/download/viewer/

5) Download the GitHub-Repository 
   on the Raspberry Pi under the user "pi":
   https://github.com/robodhhb/Smart-Modelrailway-Cam 
   
6) On Pi: Open LXTerminal and unzip downloaded file in a folder of your choice
    and change directory to "Smart-Modelrailway-Cam 2.0"

7) Run the programs:
       - Start in LXTerminal:  python3 SMRC_Main.py.py
     
--------------       
Known issues:
a)  If the paket "ImageTk" cannot be found, it has to be installed with:
    sudo apt install python3-pil.imagetk
    
b) Since the program uses object-detection two or more same locomotives
   are not allowed to run on the same track (region) at the same time. 
   Locomotive's (class-)name allways starts with a ":". 


 
      
   

