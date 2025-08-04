# cogs/admin/base.py

from discord.ext import commands
from datetime import timedelta

EMOJIS = {
    "nuke": "<a:kaboom_nuke_cod:1369106248586493973>",
    "mute": "<:Muted:1366219484297302059>",
    "unmute": "<:unmuted:1367319653147344967>",
    "kick": "<:icons_kick:1366219467364892682>",
    "ban": "<:banned:1366216116480774214>",
    "unban": "<:unban:1366219503867920384>",
    "info": "<:info1:1367665565719597186>",
    "members": "<:Discord_members:1366479637332361276>",
    "boticon": "<:icon1:1371284668481015868>",
}

def converter_tempo_segundos(tempo: int):
    anos = tempo // (365 * 24 * 60 * 60)
    tempo %= (365 * 24 * 60 * 60)
    meses = tempo // (30 * 24 * 60 * 60)
    tempo %= (30 * 24 * 60 * 60)
    semanas = tempo // (7 * 24 * 60 * 60)
    tempo %= (7 * 24 * 60 * 60)
    dias = tempo // (24 * 60 * 60)
    tempo %= (24 * 60 * 60)
    horas = tempo // (60 * 60)
    tempo %= (60 * 60)
    minutos = tempo // 60
    segundos = tempo % 60
    return anos, meses, semanas, dias, horas, minutos, segundos

def converter_tempo(anos=0, meses=0, semanas=0, dias=0, horas=0, minutos=0, segundos=0):
    dias_totais = dias + (meses * 30) + (anos * 365) + (semanas * 7)
    return timedelta(days=dias_totais, hours=horas, minutes=minutos, seconds=segundos)

async def setup(bot):
    pass

