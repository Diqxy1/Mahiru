from pathlib import Path

import discord
from discord.ext import commands, tasks


class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(
            command_prefix=self.prefix,
            case_insensitive=True,
            intents=discord.Intents.all()
        )
        #super().__init__(command_prefix=self.prefix, case_insensitive=True)
    

    def setup(self):
        print("Iniciando configurações...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f"Carregado `{cog}` cog.")

        print('Configurações completas!')
    

    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()
        
        print("Iniciando Bot...")
        super().run(TOKEN, reconnect=True)
    

    async def shutdown(self):
        print("Desconectado do discord...")
        await super().close()
    

    async def close(self):
        print("Desconectando...")
        await self.shutdown()
    

    async def on_connect(self):
        print(f" Conectado no Discord (Ping: {self.latency*1000:,.0f} ms).")
    

    async def on_resumed(self):
        print("Bot Reconectado!")
    

    async def on_disconnect(self):
        print("Bot Desconectado!")
    

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot Online!")
    

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("?")(bot, msg)
    

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)
    

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)