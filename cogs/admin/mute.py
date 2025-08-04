import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timezone

from .base import EMOJIS, converter_tempo
from cogs.identifier import identificar_alvo


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ultimo_mutado = {}

    @commands.command()
    async def mute(self, ctx, *, args):
        dono = ctx.guild.owner
        if ctx.author != dono and not ctx.author.guild_permissions.administrator:
            return await ctx.reply("❌ Você não tem permissão para isso.")

        partes = args.split()
        if len(partes) < 1:
            return await ctx.reply("❌ Especifique um usuário.")

        tempo = None
        unidades = {
            "s": ("segundos", 2419200),
            "m": ("minutos", 40320),
            "h": ("horas", 672),
            "d": ("dias", 28),
            "w": ("semanas", 4),
            "M": ("meses", 1),
            "y": ("anos", 0)  # anos não permitidos
        }

        try:
            for i, parte in enumerate(partes):
                sufixo = parte[-1]
                if sufixo in unidades:
                    valor = int(parte[:-1])
                    unidade, limite = unidades[sufixo]

                    if limite == 0 or valor > limite:
                        return await ctx.reply("⚠️ O tempo máximo de mute permitido é de 28 dias (4 semanas).")

                    kwargs = {unidade: valor}
                    tempo = converter_tempo(**kwargs)
                    partes.pop(i)
                    break
        except Exception:
            return await ctx.reply("❌ Erro ao interpretar o tempo. Use formatos como 10m, 1h, 2d...")

        identificador = " ".join(partes)
        alvos = await identificar_alvo(ctx, identificador)
        if not alvos:
            return await ctx.reply("❌ Usuário(s) não encontrado(s).")

        if not isinstance(alvos, list):
            alvos = [alvos]

        for target in alvos:
            if ctx.author.id in self.bot.no_confirm_users:
                await self.aplicar_mute(ctx, target, tempo)
            else:
                msg = await ctx.reply(
                    f"{EMOJIS['info']} O usuário **{target.display_name}** será mutado. ✅ para confirmar, ❌ para cancelar."
                )
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

                try:
                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    if str(reaction.emoji) == "✅":
                        await self.aplicar_mute(ctx, target, tempo)
                    else:
                        await ctx.reply("❌ Ação cancelada.")
                except asyncio.TimeoutError:
                    await ctx.reply("⏳ Você demorou muito para reagir.")

    async def aplicar_mute(self, ctx, target, tempo):
        try:
            if tempo:
                fim_timeout = datetime.now(timezone.utc) + tempo
                await target.timeout(fim_timeout, reason="Punido pelo comando mute")
                self.ultimo_mutado[ctx.guild.id] = target.id
                await ctx.reply(f"{EMOJIS['mute']} Usuário **{target.display_name}** mutado por {tempo} com sucesso!")
            else:
                await ctx.reply(f"{EMOJIS['mute']} ⚠️ O mute permanente deve ser feito com cargos. Esse comando é só para castigo temporário.")
        except discord.Forbidden:
            await ctx.reply("❌ Não tenho permissão para mutar este usuário.")
        except Exception as e:
            await ctx.reply(f"⚠️ Erro ao aplicar mute: {str(e)}")

    @commands.command()
    async def unmute(self, ctx, target: discord.Member):
        dono = ctx.guild.owner
        if ctx.author == dono or ctx.author.guild_permissions.administrator:
            try:
                await target.timeout(None, reason="Desmutado pelo comando unmute")
                await ctx.reply(f"{EMOJIS['unmute']} Usuário **{target.display_name}** desmutado com sucesso!")
            except discord.Forbidden:
                await ctx.reply("❌ Não tenho permissão para desmutar este usuário.")
            except Exception as e:
                await ctx.reply(f"⚠️ Erro: {str(e)}")

    @commands.command()
    async def unmutelp(self, ctx):
        dono = ctx.guild.owner
        if ctx.author != dono and not ctx.author.guild_permissions.administrator:
            return await ctx.reply("❌ Você não tem permissão para isso.")

        guild_id = ctx.guild.id
        if guild_id not in self.ultimo_mutado:
            return await ctx.reply("❌ Nenhum usuário registrado como último mutado.")

        member = await ctx.guild.fetch_member(self.ultimo_mutado[guild_id])
        if not member:
            return await ctx.reply("❌ O último mutado não está mais no servidor.")

        try:
            await member.timeout(None, reason="Desmutado pelo comando unmutelp")
            await ctx.reply(f"{EMOJIS['unmute']} Usuário **{member.display_name}** foi desmutado com sucesso!")
        except discord.Forbidden:
            await ctx.reply("❌ Não tenho permissão para desmutar este usuário.")
        except Exception as e:
            await ctx.reply(f"⚠️ Erro: {str(e)}")

    @commands.command()
    async def mutefv(self, ctx, *, identificador):
        dono = ctx.guild.owner
        if ctx.author != dono and not ctx.author.guild_permissions.administrator:
            return await ctx.reply("❌ Você não tem permissão para isso.")

        alvos = await identificar_alvo(ctx, identificador)
        if not alvos:
            return await ctx.reply("❌ Usuário(s) não encontrado(s).")

        if not isinstance(alvos, list):
            alvos = [alvos]

        role = discord.utils.get(ctx.guild.roles, name="Mutado")
        if not role:
            role = await ctx.guild.create_role(name="Mutado", reason="Cargo para mutar membros")
            for channel in ctx.guild.channels:
                try:
                    await channel.set_permissions(role, send_messages=False, add_reactions=False)
                except Exception:
                    pass

        for target in alvos:
            try:
                await target.add_roles(role, reason="Mute para sempre (mutefv)")
                self.ultimo_mutado[ctx.guild.id] = target.id
                await ctx.reply(f"{EMOJIS['mute']} Usuário **{target.display_name}** mutado para sempre com sucesso!")
            except discord.Forbidden:
                await ctx.reply(f"❌ Não tenho permissão para mutar **{target.display_name}**.")
            except Exception as e:
                await ctx.reply(f"⚠️ Erro ao mutar **{target.display_name}**: {str(e)}")


async def setup(bot):
    await bot.add_cog(Mute(bot))
