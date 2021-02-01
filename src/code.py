from azure import azure
import ipaddress
import ssl
import wifi
import socketpool
import time
import alarm

from adafruit_magtag.magtag import MagTag
 
magtag = MagTag()

#Format text 
magtag.add_text(
    text_scale=2,
    text_wrap=25,
    text_maxlen=300,
    text_position=(10, 10),
    text_anchor_point=(0, 0),
)

# Import WiFi and Azure credentials from secrets.py file
try:
    from secrets import secrets
    print("Sucessfully imported secrets!")
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Connect to WiFi
print("Available WiFi networks:")
for network in wifi.radio.start_scanning_networks():
    print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
            network.rssi, network.channel))
wifi.radio.stop_scanning_networks()

print("Connecting to %s"%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

# Connect to Azure
while True:
    try:
        # Create an instance of the Azure class with credentials
        myAzure = azure(secrets["appId"], secrets["clientSecret"], secrets["tenant"], secrets["subscription"])

        # Print the current day cost forecast and refresh display
        magtag.set_text("Azure current day cost forecast: ${}".format(myAzure.cost_forecast()))
        magtag.refresh()

        # Put the board to sleep for 24 hrs 
        time.sleep(2)
        print("Sleeping")
        PAUSE = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 60 * 60 * 24)
        alarm.exit_and_deep_sleep_until_alarms(PAUSE)

    except (ValueError, RuntimeError) as e:
        print("Some error occured, retrying! -", e)
