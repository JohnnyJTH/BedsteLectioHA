"""BedsteLectio API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout

from .const import BEDSTELECTIO_API_URL, LOGGER


class BedsteLectioApiClientError(Exception):
    """Exception to indicate a general API error."""


class BedsteLectioApiClientCommunicationError(
    BedsteLectioApiClientError
):
    """Exception to indicate a communication error."""


class BedsteLectioApiClientAuthenticationError(
    BedsteLectioApiClientError
):
    """Exception to indicate an authentication error."""


class BedsteLectioApiClient:
    """Sample API Client."""

    def __init__(
        self,
        username: str,
        password: str,
        school: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._school = school
        self._session = session

    async def async_get_next_room(self) -> any:
        """Get next room from the API."""
        return await self._api_wrapper(
            method="get", url=f"{BEDSTELECTIO_API_URL}/ha/frontpage", headers={
                "username": self._username,
                "password": self._password,
                "school": self._school,
            }
        )

    async def async_get_schools(self) -> list[str]:
        """Get schools from the API."""
        data = await self._api_wrapper(
            method="get",
            url=f"{BEDSTELECTIO_API_URL}/skoler",
        )
        return [school["id"] for school in data]

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status == 500:
                    LOGGER.error(await response.json())
                    raise BedsteLectioApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise BedsteLectioApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise BedsteLectioApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            LOGGER.exception(exception)
            raise BedsteLectioApiClientError(
                "Something really wrong happened!"
            ) from exception
