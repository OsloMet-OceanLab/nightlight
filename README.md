# Night Light Service
A service that only turns on the light for one minute every half an hour on the OBSEA ANERIS EMUAS camera.

## Install
### Step 1: Copy or clone repo
a: Copy over to Pi using scp

b: git clone directly on the pi

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
