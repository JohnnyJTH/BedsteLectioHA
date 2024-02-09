"""Adds config flow for Blueprint."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    BedsteLectioApiClient,
    BedsteLectioApiClientAuthenticationError,
    BedsteLectioApiClientCommunicationError,
    BedsteLectioApiClientError,
)
from .const import CONF_SCHOOL, DOMAIN, LOGGER


class BedsteLectioFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for BedsteLectio."""

    VERSION = 1

    schools: list[str] = []

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                    school=user_input[CONF_SCHOOL],
                )
            except BedsteLectioApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except BedsteLectioApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except BedsteLectioApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )

        if not self.schools:
            client = BedsteLectioApiClient(
                username="",
                password="",
                school="",
                session=async_create_clientsession(self.hass),
            )
            self.schools = await client.async_get_schools()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                    vol.Required(
                        CONF_SCHOOL,
                        default=(user_input or {}).get(CONF_SCHOOL),
                    ): vol.In(self.schools),
                }
            ),
            errors=_errors,
        )

    async def _test_credentials(
        self, username: str, password: str, school: str
    ) -> None:
        """Validate credentials."""
        client = BedsteLectioApiClient(
            username=username,
            password=password,
            school=school,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_next_room()
