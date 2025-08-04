import discord
import os
from datetime import datetime
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Exibe o ping do bot."""
        latency = round(self.bot.latency * 1000)
        await ctx.reply(f"!pong :ping_pong:\n:globe_with_meridians: | ping: ``{latency}ms``")

    @commands.command()
    async def dask(self, ctx):
        """Desativa confirmações de kick e ban para o usuário."""
        self.bot.no_confirm_users.add(ctx.author.id)
        await ctx.reply("🔒 As confirmações para 'kick' e 'ban' foram desativadas para você. Para reativá-las, use o comando '!askmeg'.")

    @commands.command()
    async def askmeg(self, ctx):
        """Reativa confirmações de kick e ban para o usuário."""
        self.bot.no_confirm_users.discard(ctx.author.id)
        await ctx.reply("🔓 As confirmações para 'kick' e 'ban' foram reativadas para você.")

    @commands.command()
    async def version(self, ctx):
        """Mostra a versão do bot."""
        bot_version = "1.7.6"  # Defina a versão do seu bot aqui
        await ctx.reply(f"<:icon1:1371284668481015868> | Versão do bot: `{bot_version}`")

    @commands.command()
    async def botinfo(self, ctx):
        """Exibe informações sobre o bot, incluindo número de linhas de código, data de criação da conta e servidores."""
        bot_name = self.bot.user.name
        bot_id = self.bot.user.id
        total_guilds = len(self.bot.guilds)
        bot_creation_date = self.bot.user.created_at.strftime("%d/%m/%Y %H:%M:%S")

        total_linhas = 0
        for dirpath, _, filenames in os.walk("./cogs"):
            for filename in filenames:
                if filename.endswith(".py"):
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        total_linhas += len(f.readlines())

        embed = discord.Embed(title="📌 Informações do Bot", color=discord.Color.blue())
        embed.add_field(name="🤖 Nome", value=bot_name, inline=True)
        embed.add_field(name="🆔 ID", value=bot_id, inline=True)
        embed.add_field(name="📆 Conta criada em", value=bot_creation_date, inline=True)
        embed.add_field(name="🌍 Servidores", value=total_guilds, inline=True)
        embed.add_field(name="📜 Linhas de código", value=f"{total_linhas} linhas", inline=False)
        embed.set_footer(text=f"Comando solicitado por {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def showservers(self, ctx):
        """Lista os servidores e oferece enviar os links de convite no privado."""
        guilds = sorted(self.bot.guilds, key=lambda g: g.me.joined_at)
        embed = discord.Embed(title="Servidores", description="Aqui estão os servidores que participo:")

        for i, guild in enumerate(guilds, start=1):
            embed.add_field(name=f"{i}. {guild.name}", value=f"ID: {guild.id}", inline=False)

        embed.set_footer(text="Reaja com ✅ para receber os links dos servidores no privado.")
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✅"

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            
            invite_message = "**Links de convite:**\n"
            for guild in guilds:
                try:
                    # Seleciona um canal específico (por exemplo, o primeiro canal de texto visível)
                    target_channel = next((channel for channel in guild.text_channels if channel.permissions_for(guild.me).create_instant_invite), None)
                    
                    if target_channel:
                        invite = await target_channel.create_invite(max_age=86400, max_uses=5)  # Convite válido por 24 horas e 5 usos
                        invite_message += f"\n🔗 {guild.name}: {invite.url}"
                    else:
                        invite_message += f"\n❌ {guild.name}: Convites indisponíveis."

                except discord.Forbidden:
                    invite_message += f"\n🚫 {guild.name}: Sem permissão para acessar convites."

            await user.send(invite_message)
            
        except discord.errors.Forbidden:
            await ctx.send("Não consigo enviar mensagens privadas para você.")
        except TimeoutError:
            await ctx.send("Tempo limite para resposta expirado.")

async def setup(bot):
    """Configuração da cog e inicialização das variáveis do bot."""
    if not hasattr(bot, 'no_confirm_users'):
        bot.no_confirm_users = set()

    await bot.add_cog(Utils(bot))