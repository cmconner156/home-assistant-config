import requests
#import json
#import sys
#
logger.info("CHRIS: python: data: %s" % data)
sync_server = data.get('server')
sync_port = data.get('port')
logger.info("Syncing data by connecting to ha-mqtt-bridge-sync on %s:%s" % (sync_server, sync_port))

base_uri = "http://%s:%s" % (sync_server,sync_port)
sync_devices_uri = "%s/updatedevices" % base_uri

try:
  sync_response = requests.get(sync_devices_uri)
  sync_response.raise_for_status()
except requests.exceptions.HTTPError as errh:
  logging.exception("Http Error: %s" % errh)
  logging.exception("Got %s Look into this: %s" % (sync_response.status_code, sync_response.text))
except requests.exceptions.ConnectionError as errc:
  logging.exception("Error Connecting: %s" % errc)
except requests.exceptions.Timeout as errt:
  logging.exception("Timeout Error: %s" % errt)
except requests.exceptions.RequestException as err:
  logging.exception("RequestsException: %s" % err)

sync_json_response = json.loads(sync_response.text)
logger.info("Sync successfull: %s" % sync_json_response[0])

