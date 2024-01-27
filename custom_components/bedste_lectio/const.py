"""Constants for integration_blueprint."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "BedsteLectio"
DOMAIN = "bedste_lectio"
VERSION = "0.0.1"
ATTRIBUTION = "Data provided by https://bedstelectio.dk/"

BEDSTELECTIO_API_URL = "https://api.bedstelectio.dk"
CONF_SCHOOL = "school"
