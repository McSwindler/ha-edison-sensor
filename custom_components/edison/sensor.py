"""Platform for sensor integration."""
from datetime import timedelta, datetime
import logging
import re
from siftapi import Sift

from homeassistant.const import (
    CONF_API_KEY,
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_HOST)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'edison'
SCAN_INTERVAL = timedelta(seconds=5*60)
CONF_API_SECRET = 'api_secret'


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the edison platform."""
    add_entities([EdisonSensor(config)])


class EdisonSensor(Entity):

    def __init__(self, config):
        self._state = None
        self._attr = None
        self._email = config[CONF_EMAIL]
        self._password = config[CONF_PASSWORD]
        self._host = config[CONF_HOST]
        self._sift = Sift(config[CONF_API_KEY], config[CONF_API_SECRET])
        self._setup_account()

    def _setup_account(self):
        if self._create_user():
            data = {
                'account_type': 'imap',
                'account': self._email,
                'password': self._password,
                'host': self._host
            }
            response = self._sift.add_email_connection(
                self._nice_name, data)
            if response['code'] != 200:
                _LOGGER.error('Cannot create Sift Email Connection, Response: {} - {}'.format(
                    response['code'], response['message']))

    @property
    def _nice_name(self):
        return re.sub(r'\W+', '_', self._email)

    def _create_user(self):
        response = self._sift.add_user(self._nice_name, 'en_US')
        if response['code'] != 200:
            _LOGGER.error(
                'Cannot create Sift User, Response: {} - {}'.format(response['code'], response['message']))
            return False
        return True

    @property
    def name(self):
        return 'Edison {}'.format(self._email)

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return self._attr

    @property
    def icon(self):
        return 'mdi:email'

    def update(self):
        state = self.hass.states.get(self.entity_id)
        if state:
            last_updated = int(state.last_updated.timestamp())
        else:
            last_updated = int(datetime.utcnow().timestamp())
        response = self._sift.get_sifts(
            self._nice_name, last_update_time=last_updated)
        if 'result' in response:
            self._state = len(response['result'])
        self._attr = response
