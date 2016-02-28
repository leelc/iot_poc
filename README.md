# IOT_POC

This repository contains the implementation and setup details of an IoT application "Obstructing Objects Detector".

The purpose of the application is to detect the presence of objects (including vehicles) causing obstructions in pubicly accessible locations by tracking its presence over a specific period of time. It has several potential applications, such as detecting illegal parking, detecting objects at emergency exits, detecting presence of passengers obstructing door entrance of arriving trains, etc.

Hardware Required (recommended):
  (a) Raspberry Pi 2
  (b) GrovePi
  (c) Wireless adaptor
  (d) Grove ultrasonic sensor
  (e) LED
  (f) Power bank
  
Software Required:
  (a) Python 3.5
  (b) AWS
  (c) Slack
  (c) script provided "ob_det.py"
  
Setup Instructions
  (a) Attach Raspberry Pi and GrovePi together
  (b) Connect the wireless adaptor to the Raspberry Pi
  (c) Connect the ultrasonic sensor and LED to the GrovePi
  (d) Power the device with power bank (or other power source)
  (e) The final setup should look similar to the one at "https://www.dropbox.com/s/z5oex5tfwknqr7y/hardware%20setup.JPG?dl=0"
  
Setup of AWS
  (a) Make sure that you have an AWS account
  (b) Create a new AWS IoT and use the same name in AWS and script
  (c) Copy the relevant certificates generated and copy into the Raspberry Pi
  (d) Create a new DynamoDB for the thing you created

To run the program, type "python3.5 ob_det.py')

The screen output should look like this "https://www.dropbox.com/s/se8735rp3j4z1y6/demo-screen-output.txt?dl=0"


Good Luck!!!

LeeLC
28 Feb 2016

  
  
