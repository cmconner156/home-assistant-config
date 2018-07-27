import logging
import requests
import json
import sys
import datetime

_LOGGER_ = logging.getLogger(__name__)

DOMAIN = 'ha_mqtt_bridge_sync'
DEPENDENCIES = []

SERVER = 'server'
DEFAULT_SERVER = 'mqttbridgesync'
PORT = 'port'
DEFAULT_PORT = '80'

def setup(hass, config):

  def handle_sync(call):
    sync_server = config[DOMAIN].get(SERVER, DEFAULT_SERVER)
    sync_port = config[DOMAIN].get(PORT, DEFAULT_PORT)
    base_uri = "http://%s:%s" % (sync_server,sync_port)
    sync_devices_uri = "%s/updatedevices" % base_uri
    _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Setting up: sync_devices_uri: %s" % sync_devices_uri)

    _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Sync devices uri: %s" % sync_devices_uri )

    try:
      sync_response = requests.get(sync_devices_uri)
      sync_response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Http Error: ")
#      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Http Error: %s" % errh)
      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Got  Look into this: ")
#      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Got %s Look into this: %s" % (sync_response.status_code, sync_response.text))
    except requests.exceptions.ConnectionError as errc:
      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Error Connecting: ")
#      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Error Connecting: %s" % errc)
    except requests.exceptions.Timeout as errt:
      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Timeout Error: ")
#      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Timeout Error: %s" % errt)
    except requests.exceptions.RequestException as err:
      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: RequestsException: ")
#      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: RequestsException: %s" % err)
    except Exception as e:
      _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Catch All Exception: ")

    _LOGGER_.info("HA-MQTT-BRIDGE-SYNC: Sync successfull:")
    hass.states.set('%s.Last_Sync' % DOMAIN, datetime.datetime.now().timestamp())


  hass.services.register(DOMAIN, 'sync', handle_sync)
  
  return True




