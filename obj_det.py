#!/usr/bin/env python

# This python is written by LeeLC
# The purpose is to detect the presence of object at specific location for a presribed period of time.
# The results are then send to AWS IoT

import time
import datetime
import ssl
import json
import paho.mqtt.client as mqtt
import grovepi

# TODO: Name of our Raspberry Pi, also known as our "Thing Name"
deviceName = "g39_pi"
# TODO: Public certificate of our Raspberry Pi, as provided by AWS IoT.
deviceCertificate = "132a0c3d8b-certificate.pem.crt"
# TODO: Private key of our Raspberry Pi, as provided by AWS IoT.
devicePrivateKey = "132a0c3d8b-private.pem.key"
# Root certificate to authenticate AWS IoT when we connect to their server.
awsCert = "aws-iot-rootCA.crt"
isConnected = False

# Set the device id of the object detector
device = 1234

# Connect Grove LED to digital port D2, Ultrasonic Ranger to D4.
led = 2
ultrasonic_ranger = 4

# To set the threshold range - if lesser then object is detected
Dist_Thres = 50


# This is the main logic of the program.  We connect to AWS IoT via MQTT, send sensor data periodically to AWS IoT,
# and handle any actuation commands received from AWS IoT.
def main():
    global isConnected
    # Create an MQTT client for connecting to AWS IoT via MQTT.
    client = mqtt.Client(deviceName + "_sr")  # Client ID must be unique because AWS will disconnect any duplicates.
    client.on_connect = on_connect  # When connected, call on_connect.
    client.on_message = on_message  # When message received, call on_message.
    client.on_log = on_log          # When logging debug messages, call on_log.

    # Set the certificates and private key for connecting to AWS IoT.  TLS 1.2 is mandatory for AWS IoT and is supported
    # only in Python 3.4 and later, compiled with OpenSSL 1.0.1 and later.
    client.tls_set(awsCert, deviceCertificate, devicePrivateKey, ssl.CERT_REQUIRED, ssl.PROTOCOL_TLSv1_2)

    # Connect to AWS IoT server.  Use AWS command line "aws iot describe-endpoint" to get the address.
    print("Connecting to AWS IoT...")
    client.connect("A1TY9955CX3QUA.iot.ap-northeast-1.amazonaws.com",8883, 60)

    # Start a background thread to process the MQTT network commands concurrently, including auto-reconnection.
    client.loop_start()

    # Configure the Grove LED port for output.
    grovepi.pinMode(led, "OUTPUT")
    time.sleep(1)

    detected=0

    # Loop forever.
    while True:
        try:
            # If we are not connected yet to AWS IoT, wait 1 second and try again.
            if not isConnected:
                time.sleep(1)
                continue

            # Scanning mode - 
            while (grovepi.ultrasonicRead(ultrasonic_ranger)>Dist_Thres):
                print("[Status] scanning... no detection @ "+datetime.datetime.now().isoformat())
                time.sleep(3)

            # Verification mode - 
            detected=1
            for i in range(1,10):
                if (grovepi.ultrasonicRead(ultrasonic_ranger)<Dist_Thres):
                    print("[Status] possible object presence @ "+datetime.datetime.now().isoformat())
                    grovepi.digitalWrite(led,1)
                    grovepi.digitalWrite(led,0)
                else:
                    detected=0
                    break

            if (detected==1):
                # Read Grove sensor values. Prepare our sensor data in JSON format.
                print("[Status] object detected!!!")
                grovepi.digitalWrite(led,1)
                payload = {
                    "state": {
                        "reported": {
                            "device": device,
                            "timestamp": datetime.datetime.now().isoformat(),
                            "distance": grovepi.ultrasonicRead(ultrasonic_ranger)
                        }
                    }
                }
                print("Sending sensor data to AWS IoT...\n" +
                      json.dumps(payload, indent=4, separators=(',', ': ')))

                # Publish our sensor data to AWS IoT via the MQTT topic, also known as updating our "Thing Shadow".
                client.publish("$aws/things/" + deviceName + "/shadow/update", json.dumps(payload))
                print("Sent to AWS IoT")

                while (grovepi.ultrasonicRead(ultrasonic_ranger)<Dist_Thres):
                    print("[Status] object still present ...")
                grovepi.digitalWrite(led,0)
                print("[Status] object is not longer detected!")

        except KeyboardInterrupt:
            break
        except IOError:
            print("Error")


# This is called when we are connected to AWS IoT via MQTT.
# We subscribe for notifications of desired state updates.
def on_connect(client, userdata, flags, rc):
    global isConnected
    isConnected = True
    print("Connected to AWS IoT")
    # Subscribe to our MQTT topic so that we will receive notifications of updates.
    topic = "$aws/things/" + deviceName + "/shadow/update/accepted"
    print("Subscribing to MQTT topic " + topic)
    client.subscribe(topic)


# This is called when we receive a subscription notification from AWS IoT.
def on_message(client, userdata, msg):
    # Convert the JSON payload to a Python dictionary.
    # The payload is in binary format so we need to decode as UTF-8.
    payload2 = json.loads(msg.payload.decode("utf-8"))
#    print("Received message, topic: " + msg.topic + ", payload:\n" +
#          json.dumps(payload2, indent=4, separators=(',', ': ')))


# Print out log messages for tracing.
def on_log(client, userdata, level, buf):
    print("Log: " + buf)


# Start the main program.
main()

