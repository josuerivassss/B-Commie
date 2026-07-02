import discord
from typing import Optional
from core.kernel import CommieContext, Locale
from core.kernel.emojis import CommieEmojis

class BaseView(discord.ui.View):
    def __init__(self, ctx: CommieContext, locale: Locale, timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        self.message: discord.Message | None = None
        self.t = locale
        self.ctx = ctx

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            await self.message.edit(view=self)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        expected_user_id = self.ctx.author.id
        if self.message and self.message.interaction_metadata:
            expected_user_id = self.message.interaction_metadata.user.id

        if interaction.user.id != expected_user_id:
            await interaction.response.send_message(self.t.get("errors.viewNotForYou" + CommieEmojis.Angry, user=interaction.user.mention), ephemeral=True)
            return False
        return True
    
    async def _finalize(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            await self.message.edit(view=self)
        self.stop()