import asyncio
import discord
from discord.ext import commands
from .base import EMOJIS
from cogs.identifier import identificar_alvo

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ultimo_banido = {}

    @commands.command()
    async def ban(self, ctx, target: discord.Member):
        dono = ctx.guild.owner
        if ctx.author == dono or ctx.author.guild_permissions.administrator:
            if ctx.author.id in self.bot.no_confirm_users:
                try:
                    await target.ban(reason=f"Banido por {ctx.author.display_name}")
                    self.ultimo_banido[ctx.guild.id] = target.id
                    await ctx.reply(f"{EMOJIS['ban']} Usuário **{target.display_name}** foi banido diretamente.")
                except discord.Forbidden:
                    await ctx.reply("❌ Não tenho permissão para banir este usuário.")
                except Exception as e:
                    await ctx.reply(f"⚠️ Ocorreu um erro: {str(e)}")
            else:
                msg = await ctx.reply(
                    f"{EMOJIS['info']} O usuário **{target.display_name}** foi encontrado. Reaja com ✅ para confirmar ou ❌ para cancelar."
                )
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

                try:
                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    if str(reaction.emoji) == "✅":
                        await target.ban(reason=f"Banido por {ctx.author.display_name}")
                        self.ultimo_banido[ctx.guild.id] = target.id
                        await ctx.reply(f"{EMOJIS['ban']} Usuário **{target.display_name}** foi banido com sucesso!")
                    else:
                        await ctx.reply("❌ Ação cancelada.")
                except asyncio.TimeoutError:
                    await ctx.reply("⏳ Você demorou muito para reagir.")
                except Exception as e:
                    await ctx.reply(f"⚠️ Ocorreu um erro: {str(e)}")
        else:
            await ctx.reply("❌ Você não tem permissão para isso.")

    @commands.command()
    async def unban(self, ctx, target: discord.User):
        dono = ctx.guild.owner
        if ctx.author == dono or ctx.author.guild_permissions.administrator:
            if ctx.author.id in self.bot.no_confirm_users:
                try:
                    await ctx.guild.unban(target, reason=f"Desbanido por {ctx.author.display_name}")
                    await ctx.reply(f"{EMOJIS['unban']} Usuário **{target.name}** foi desbanido diretamente.")
                    await target.send("Você foi desbanido do servidor! https://discord.gg/aaUd5ABQgD")
                except discord.NotFound:
                    await ctx.reply("❌ O usuário não está banido.")
                except Exception as e:
                    await ctx.reply(f"⚠️ Ocorreu um erro: {str(e)}")
            else:
                msg = await ctx.reply(
                    f"⚠️ Deseja desbanir o usuário **{target.name}**? Reaja com ✅ para confirmar ou ❌ para cancelar."
                )
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

                try:
                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    if str(reaction.emoji) == "✅":
                        await ctx.guild.unban(target, reason=f"Desbanido por {ctx.author.display_name}")
                        await ctx.reply(f"{EMOJIS['unban']} Usuário **{target.name}** foi desbanido com sucesso!")
                        await target.send("Você foi desbanido do servidor! https://discord.gg/aaUd5ABQgD")
                    else:
                        await ctx.reply("❌ Ação cancelada.")
                except asyncio.TimeoutError:
                    await ctx.reply("⏳ Você demorou muito para reagir.")
                except Exception as e:
                    await ctx.reply(f"⚠️ Ocorreu um erro: {str(e)}")
        else:
            await ctx.reply("❌ Você não tem permissão para isso.")

    @commands.command()
    async def unbanlp(self, ctx):
        dono = ctx.guild.owner
        if ctx.author == dono or ctx.author.guild_permissions.administrator:
            if ctx.guild.id in self.ultimo_banido:
                try:
                    user_id = self.ultimo_banido[ctx.guild.id]
                    user = await self.bot.fetch_user(user_id)
                    await ctx.guild.unban(user, reason=f"Desbanido por {ctx.author.display_name} através de !unbanlp")
                    await ctx.reply(f"{EMOJIS['unban']} Usuário **{user.name}** foi desbanido com sucesso!")
                    await user.send("Você foi desbanido do servidor! https://discord.gg/aaUd5ABQgD")
                except discord.NotFound:
                    await ctx.reply("❌ O usuário não está banido.")
                except discord.Forbidden:
                    await ctx.reply("❌ Não tenho permissão.")
                except Exception as e:
                    await ctx.reply(f"⚠️ Ocorreu um erro: {str(e)}")
            else:
                await ctx.reply("❌ Nenhum usuário registrado como último banido.")
        else:
            await ctx.reply("❌ Você não tem permissão para isso.")

async def setup(bot):
    await bot.add_cog(Ban(bot))
