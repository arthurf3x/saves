import discord
from discord.ext import commands
from .base import EMOJIS
from cogs.identifier import identificar_alvo


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, target: discord.Member):
        dono = ctx.guild.owner
        if ctx.author == dono or ctx.author.guild_permissions.administrator:
            if ctx.author.id in self.bot.no_confirm_users:
                try:
                    await target.kick(reason=f"Expulso por {ctx.author.display_name}")
                    await ctx.reply(f"{EMOJIS['kick']} Usuário **{target.display_name}** foi expulso diretamente.")
                except discord.Forbidden:
                    await ctx.reply("❌ Não tenho permissão para expulsar este usuário.")
                except Exception as e:
                    await ctx.reply(f"⚠️ Ocorreu um erro: {str(e)}")
            else:
                msg = await ctx.reply(
                    f"🛑 O usuário **{target.display_name}** foi encontrado. Reaja com ✅ para confirmar ou ❌ para cancelar."
                )
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

                try:
                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    if str(reaction.emoji) == "✅":
                        await target.kick(reason=f"Expulso por {ctx.author.display_name}")
                        await ctx.reply(f"{EMOJIS['kick']} Usuário **{target.display_name}** foi expulso com sucesso!")
                    else:
                        await ctx.reply("❌ Ação cancelada.")
                except TimeoutError:
                    await ctx.reply("⏳ Você demorou muito para reagir.")
                except Exception as e:
                    await ctx.reply(f"⚠️ Ocorreu um erro: {str(e)}")
        else:
            await ctx.reply("❌ Você não tem permissão para isso.")

async def setup(bot):
    await bot.add_cog(Kick(bot))
