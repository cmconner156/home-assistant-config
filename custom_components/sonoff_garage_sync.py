import logging
import json

_LOGGER_ = logging.getLogger(__name__)
# The domain of your component. Should be equal to the name of your component.
DOMAIN = 'sonoff_garage_sync'

# List of component names (string) your component depends upon.
DEPENDENCIES = ['mqtt']


CONF_TOPIC_IN = 'topic_in'
CONF_GARAGE_ID = 'garage_id'
CONF_STATE_CLOSED = "state_closed"
CONF_STATE_OPEN = "state_open"
CONF_TELE_STATE_KEY = "tele_state_key"

DEFAULT_TOPIC_IN = 'home-assistant/sonoff_garage_sync_in'
DEFAULT_GARAGE_ID = 'sonoff_garage'
DEFAULT_STATE_CLOSED = "on"
DEFAULT_STATE_OPEN = "off"
DEFAULT_TELE_STATE_KEY = "Switch2"


def setup(hass, config):
    """Set up the Sonoff Garage Sync component."""
    mqtt = hass.components.mqtt
    topic_in = config[DOMAIN].get(CONF_TOPIC_IN, DEFAULT_TOPIC_IN)
    _LOGGER_.debug("topic_in: %s" % topic_in)
    garage_id = config[DOMAIN].get(CONF_GARAGE_ID, DEFAULT_GARAGE_ID)
    _LOGGER_.debug("garage_id: %s" % garage_id)
    state_closed = config[DOMAIN].get(CONF_STATE_CLOSED, DEFAULT_STATE_CLOSED)
    _LOGGER_.debug("state_closed: %s" % state_closed)
    state_open = config[DOMAIN].get(CONF_STATE_OPEN, DEFAULT_STATE_OPEN)
    _LOGGER_.debug("state_open: %s" % state_open)
    tele_state_key = config[DOMAIN].get(CONF_TELE_STATE_KEY, DEFAULT_TELE_STATE_KEY)
    _LOGGER_.debug("tele_state_key: %s" % tele_state_key)
    entity_id = 'sonoff_garage_sync.last_message'

    # Listener to be called when we receive a message.
    def message_received(topic, payload, qos):
        """Handle new MQTT messages."""
        state_json = json.loads(payload)
        _LOGGER_.info("incoming message state: %s" % state_json['tele_state_key'])
        if state_json['tele_state_key'].lower() == state_closed:
          new_state = "closed"
        elif state_json['tele_state_key'].lower() == state_open:
          new_state = "open"
        else:
          new_state = "unknown"

        _LOGGER_.info("setting %s state to %s: " % (garage_id, new_state ))
        hass.states.set(entity_id, payload)

        if new_state != "unknown":
          hass.states.set(garage_id, new_state) 

    # Subscribe our listener to a topic.
    mqtt.subscribe(topic_in, message_received)

    # Set the initial state.
    hass.states.set(entity_id, 'No messages')

    # Return boolean to indicate that initialization was successfully.
    return True

