import network
import machine
import urequests
import time

# put your wifi credentials here
WIFI_SSID = ""
WIFI_PASSWORD = ""

# set your url and token here. The token can be found in the settings, for more information see https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token
HA_URL = "http://[YOUR HA URL HERE]:8123/api/services/input_boolean/"
HA_TOKEN = ""

# you can set your own helper name here
HELPER_NAME = "presence_a" 

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

while not wlan.isconnected():
    pass

sensor = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)

last_motion_state = sensor.value()
print('motion state on start: '+str(last_motion_state))

def send_motion_state(event_type):
    print('sending state: '+event_type)
    headers = {'Authorization': 'Bearer '+HA_TOKEN, 'Content-Type': 'application/json'}
    data = '{"entity_id": "input_boolean.'+HELPER_NAME+'"}' 
    try:
        response = urequests.post(HA_URL+'turn_'+event_type, headers=headers, data=data)
        response.close()
    except Exception as e:
        print('Failed to send: ', e)
        
while True:
    motion_state = sensor.value()
    if motion_state != last_motion_state:
        last_motion_state = motion_state
        if motion_state == 1:
            send_motion_state("on")
        else:
            send_motion_state("off")
    time.sleep(0.1)
