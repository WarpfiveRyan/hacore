"""Adds config flow for SabNzbd."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import DOMAIN
from .helpers import get_client

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): TextSelector(
            TextSelectorConfig(
                type=TextSelectorType.URL,
            )
        ),
        vol.Required(CONF_API_KEY): TextSelector(
            TextSelectorConfig(
                type=TextSelectorType.PASSWORD,
            )
        ),
    }
)


class SABnzbdConfigFlow(ConfigFlow, domain=DOMAIN):
    """Sabnzbd config flow."""

    VERSION = 1

    async def _async_validate_input(self, user_input):
        """Validate the user input allows us to connect."""
        errors = {}
        sab_api = await get_client(self.hass, user_input)
        if not sab_api:
            errors["base"] = "cannot_connect"

        return errors

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""

        errors = {}
        if user_input is not None:
            errors = await self._async_validate_input(user_input)

            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_API_KEY][:12], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=USER_SCHEMA,
            errors=errors,
        )
