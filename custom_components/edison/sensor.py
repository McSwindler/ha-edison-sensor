"""Platform for sensor integration."""
from datetime import timedelta
import logging
import re
from siftapi import Sift

from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'edison'
SCAN_INTERVAL = timedelta(seconds=5*60)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the edison platform."""
    add_entities([EdisonSensor(config)])


class EdisonSensor(Entity):

    def __init__(self, config):
        self._state = None
        self._attr = None
        self._email = config['email_address']
        self._password = config['password']
        self._host = config['imap_host']
        self._sift = Sift(config['api_key'], config['api_secret'])
        self._createUser()

    def _setup_account(self):
        if self._create_user():
            response = self._sift.get_email_connections(self._nice_name)
            if not response['result']:
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
        return 'edison_{}'.format(self._nice_name

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
        response=self._sift.get_sifts(self._nice_name)
        self._state=len(response['results'])
