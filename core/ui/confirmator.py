"""
Confirmation View (core/ui/confirmation.py)

Reusable confirmation dialog for discord.py based bots.

This view is designed to:
- Restrict interactions to the command author
- Support localization through a Locale instance
- Provide confirm / cancel actions via callbacks
- Auto-disable on timeout
- Be reusable across commands and cogs

Typical usage:
- Commands send a message (embed or text)
- Commands pass confirm / cancel callbacks
- The view handles UI state and interaction logic
"""

from typing import Callable, Awaitable
import discord
from core.kernel.context import CommieContext
from core.kernel.locale import Locale
from core.ui.base import BaseView

class Confirmator(BaseView):
    def __init__(
        self,
        *,
        ctx: CommieContext,
        locale: Locale,
        on_confirm: Callable[[discord.Interaction], Awaitable[None]] | None = None,
        on_cancel: Callable[[discord.Interaction], Awaitable[None]] | None = None,
        timeout: int = 30
    ):
        super().__init__(ctx=ctx, locale=locale, timeout=timeout)
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self._apply_locale()

    def _apply_locale(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "confirm_cancel":
                    child.label = self.t.get("confirmator.cancel")
                elif child.custom_id == "confirm_confirm":
                    child.label = self.t.get("confirmator.confirm")

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.gray,
        custom_id="confirm_cancel"
    )
    async def cancel(self, interaction: discord.Interaction, _):
        await interaction.response.defer()
        if self.on_cancel:
            await self.on_cancel(interaction)
        await self._finalize()

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.red,
        custom_id="confirm_confirm"
    )
    async def confirm(self, interaction: discord.Interaction, _):
        await interaction.response.defer()
        if self.on_confirm:
            await self.on_confirm(interaction)
        await self._finalize()
