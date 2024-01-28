"""Sensor platforms for BedsteLectio."""
from __future__ import annotations
from datetime import datetime
from dateutil import parser

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN
from .coordinator import BedsteLectioDataUpdateCoordinator
from .entity import BedsteLectioEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="bedste_lectio_next_room",
        name="BedsteLectio Next Room",
        icon="mdi:map-marker",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        BedsteLectioSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


def get_next_room(entries: list[dict[str, str]]) -> dict[str, str]:
    """Get the next room from the list of rooms."""
    if len(entries) == 0:
        return {
            "room": "N/A",
            "activity": "N/A",
            "teacher": "N/A",
            "start": "N/A",
        }

    rooms = []
    for entry in entries:
        date = parser.parse(entry["tidspunkt"].split(" til")[0], fuzzy=True)
        if date < datetime.now():
            continue

        rooms.append({
            "room": entry.get("lokale", "N/A"),
            "activity": entry.get("navn") or entry.get("hold", "N/A"),
            "teacher": entry.get("lærer", "N/A"),
            "start": date,
        })

    return rooms[0] # The first entry is closest to now that hasn't passed


class BedsteLectioSensor(BedsteLectioEntity, SensorEntity):
    """BedsteLectio Sensor class."""

    def __init__(
        self,
        coordinator: BedsteLectioDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        entries = self.coordinator.data.get("skema")
        room = get_next_room(entries)
        return room.get("room", "N/A")

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return the state attributes of the entity."""
        entries = self.coordinator.data.get("skema")
        data = get_next_room(entries)
        data.update({
            "last_update": datetime.now(),
        })
        return data
