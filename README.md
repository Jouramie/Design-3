# How run the system

Just run the `start.py` script. You also need to specify what part you want to run, robot or station.

```commandline
start.py station
```

Also, make sure the requirements are installed. Run the following command at the root of the project: 

```commandline
pip install -r requirements.txt
```

# How to network

The robot host is own wifi network called `equipe6`. Make sure you're connected to it.

The system use socket connection with the port 7420. First of all, make sure the port is open on the base station.

For those who use `ufw` for their firewall, you can add a rule to allow only the mini-pc to connect on the port 7420. Use the following command, assuming the ip address of the robot is `10.42.0.1`.

```commandline
ufw allow proto tcp to any port 7420 from 10.42.0.1
```

If you don't use `ufw`, good luck. 

Then, host the socket on the base station and connect to it with the robot! Make sure the robot connect to the right ip address. You can find the ip address of the base station using the following commands.

###### Arch based linux
```commandline
ip address
```

###### Ubuntu/Fedora
```commandline
ifconfig
```

###### From the robot
```commandline
nmap 10.42.0.0/24
```
