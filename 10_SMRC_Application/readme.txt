Installation der Smart Modelrailway-Cam Applikation (see English Version below)
===================================================================
Voraussetzung: Raspberry Pi 4B mit 
  - PiOS (Legacy) Buster  und Python 3.7 
     !!Nicht PiOS Bullseye verwenden!!!
  - Raspberry Pi Camera V2
  - Coral USB Accelerator (Edge TPU)

Empfohlen: Update von PiOS Buster
- sudo apt update
- sudo apt full-upgrade

Die Installation der SmartModelrailway-Cam besteht aus:

1) Anmeldung als user "pi". 
 
2) Setup der Raspberry Pi Camera V2:
   https://projects-raspberry.com/getting-started-with-raspberry-pi-camera/

3) Zugriff auf den Pi über VNC von einem PC aus:
   https://www.raspberrypi.com/documentation/computers/remote-access.html#virtual-network-computing-vnc
   
4) Für den PC: Download des VNC Viewers:
   https://www.realvnc.com/en/connect/download/viewer/

5) Installation der Edge TPU auf dem Pi:
   Achtung: Erst SW installieren, dann Edge TPU über USB anschließen!
   Siehe den Get Started Giude:
   https://coral.withgoogle.com/docs/accelerator/get-started/
   Es reicht aus, die Edge TPU mit "default operating frequency" zu installieren.
                     
6) Download des GitHub-Repository 
   auf dem Raspberry Pi unter dem user "pi":
   https://github.com/robodhhb/Smart-Modelrailway-Cam 
   mit dem grünen Knopf "code" und dann "Download zip". 

7) Pi: LXTerminal öffnen und zip-Datei mit unzip in einem Ordner Ihrer Wahl entpacken
    und in den Ordner "Smart-Modelrailway-Cam" mit cd wechseln

8) Programme starten:   
   - USB Accelerator an den USB 3 port des Pi anschließen.
   - Starten im LXTerminal mit "python3 SMRC_Main.py"
    
------------------    
Bekannte Probleme:
a)  Falls das Paket "ImageTk" nicht gefunden wird, muss es noch
    installiert werden mit:
    sudo aptitude install python3-pil.imagetk

    
========================English Version====================================
Installation of the application "Smart Modelrailway-Cam"
--------------------------------------------
Prerequisite: Raspberry Pi 4B with:
   - PiOS (Legacy) Buster and Python 3.7
      !!! Do not use PiOS Bullseye !!!
   - Raspberry Pi Camera V2
   - Coral USB Accelerator (Edge TPU)
   
Recommended: Update PiOS Buster
- sudo apt update
- sudo apt full-upgrade

Installation steps:
   
1) Login as user "pi". 
 
2) Setup  Raspberry Pi Camera V2:
   https://projects-raspberry.com/getting-started-with-raspberry-pi-camera/

3) Access the Pi desktop with VNC via a PC:
   https://www.raspberrypi.com/documentation/computers/remote-access.html#virtual-network-computing-vnc

4) Foe a PC: Download des VNC Viewers:
   https://www.realvnc.com/en/connect/download/viewer/

5) Installation of the Edge TPU:
   Caution: First install the software then connect Edge TPU to the USB-Port!
   See: Get started guide:
   https://coral.withgoogle.com/docs/accelerator/get-started/
   It is sufficient to install the Edge TPU with default operating frequency.

6) Download the GitHub-Repository 
   on the Raspberry Pi under the user "pi":
   https://github.com/robodhhb/Smart-Modelrailway-Cam 
   
7)) On Pi: Open LXTerminal and unzip downloaded file in a folder of your choice
    and change directory to "Smart-Modelrailway-Cam"

8) Run the programs:
       - Connect USB Accelearator to the USB3 port
       - Start in LXTerminal:  python3 roboPiCamMain.py
     
--------------       
Known issues:
a)  If the paket "ImageTk" cannot be found, it has to be installed with:
    sudo aptitude install python3-pil.imagetk



 
      
   
