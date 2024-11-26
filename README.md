# Night Light Service
Night Light Service (NLS) is a service that only turns on the light for one minute every half an hour on the OBSEA ANERIS EMUAS camera.

## Install
### Step 0: Connect device to your computer
Connect your PC with the Raspberry Pi you intend to use, either by cable or network. Make sure you have an IP on the same interface as the device you intend to work on. Say if your connected to the Pi through ethernet and the Pi's IP is `192.168.1.2`, you can scan the network using `arp` or wireshark and choose an IP on the same subnet that is available. 

Let's say we decide to use `192.168.1.6` (because it's unused) and that we are connected through a network interface on our computer called `en8`, then in order to add the IP to our interface we can use the following command:

**Mac:**
```shell
sudo ifconfig en8 alias 192.168.3.6 255.255.255.0
```
**Linux:**
```shell
sudo ip addr add 192.168.3.6/24 dev en8
```
for Linux `addr add` can be substituted with `a a` if you want to write it quicker.

**Windows:** If you are really using Windows I can't help you...

**NOTE:** If you don't know what network interfaces you have available or want to see what IPs are your computer has on different interfaces, you can check this using `sudo ifconfig` for Mac and 
`sudo ip addr` or `sudo ip a` for Linux.


### Step 1: Copy or clone repo
There are two ways of getting the NLS on the desired Raspberry Pi 
#### a: Copy over to Pi using scp
If you don't want to log into git on the host device, there is an option to clone this repo onto your personal computer before copying it over afterwards.

In order to do this first clone the repo to your computer, either with https or ssh:

SSH:
https:
```shell
git clone https://github.com/OsloMet-OceanLab/nightlight.git
```

SSH:
```shell
git clone git@github.com:OsloMet-OceanLab/nightlight.git
```

The difference is that SSH requires a [public key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) while HTTPS requires a [github token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens), please consult the github documentation  [github documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) for more on this.
```shell
scp 
```

#### b: git clone directly on the pi
https:
```shell
git clone https://github.com/OsloMet-OceanLab/nightlight.git
```

SSH:
```shell
git clone git@github.com:OsloMet-OceanLab/nightlight.git
```

### Step 2: Move shit around
sudo mv nightlight/nightlight.service /opt/

sudo mv nightlight/ /opt/

### Step 3: Users, groups and permissions
Set up www-data user

Add user to gpio

### Step 4: Register and start service

sudo systemctl link /opt/nightlight.service

sudo systemctl enable nightlight.service

sudo systemctl daemon-reload

sudo systemctl start nightlight.service

In order to check that the service has started up correctly, the status of the service can be checked using:
sudo systemctl status nightlight.service
