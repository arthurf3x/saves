# cogs/identifier.py

import discord

async def identificar_alvo(ctx, argumento):
    argumento = argumento.strip().lower()
    guild = ctx.guild

    if argumento in ["all", "@everyone"]:
        return [m for m in guild.members if m != ctx.me and not m.bot]

    elif argumento == "@here":
        canal = ctx.channel
        return [m for m in canal.members if m.status != discord.Status.offline and m != ctx.me and not m.bot]

    # Menções diretas (tem prioridade)
    if ctx.message.mentions:
        return [m for m in ctx.message.mentions if m != ctx.me and not m.bot]

    # ID
    if argumento.isdigit():
        membro = guild.get_member(int(argumento))
        if membro and membro != ctx.me and not membro.bot:
            return [membro]

    # Nome de usuário ou display name (parcial, insensível a maiúsculas)
    argumento = argumento.lower()
    correspondentes = [
        m for m in guild.members
        if argumento in m.name.lower() or argumento in m.display_name.lower()
    ]
    return [m for m in correspondentes if m != ctx.me and not m.bot]

# Este módulo é utilitário, então não é um cog
