# NordVPN - Not Working

This is the backend of a [NordVPN WebApp](https://github.com/HuiiBuh/NordVPNGUI). 


### Installation Instructions
I only tested the Program with Python 3.6, so I can´t guarantee that it will work with anoterh python version. I heard that eel had problems with Python 3.7. 

Download and install the official [NordVPN](https://nordvpn.com/de/download/linux/) commandline program. 
Then execute ```sudo apt-get update``` and ```sudo apt-get install nordvpn```.

Install the package which connects the python app with the WebApp<br>
```pip3 install eel```

Download this project and the [NordVPN GUI](https://github.com/HuiiBuh/NordVPNGUI).
```
.
├── root                   
│   ├── NordVPN
│   ├── NordVPNGUI
|...
```

To start the program execute the NordVPN.py file.<br>
```python3.6 NordVPN.py```
