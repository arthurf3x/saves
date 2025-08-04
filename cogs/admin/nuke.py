import discord
from discord.ext import commands
import asyncio

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        """Apaga todas as mensagens do canal onde o comando foi usado e informa o número deletado."""
        try:
            mensagens = await ctx.channel.purge(limit=None)
            total_mensagens = len(mensagens)
            await ctx.send(f"💥 `{total_mensagens}` mensagens foram apagadas neste canal! 🔥")
        except Exception as e:
            await ctx.send(f"❌ Erro ao executar o comando Nuke: {str(e)}")


class NukeChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nukechannels(self, ctx):
        """Apaga todas as mensagens de todos os canais do servidor e informa o número total deletado."""
        total_mensagens = 0

        try:
            await ctx.send("🚀 Iniciando limpeza de todos os canais...")
            for channel in ctx.guild.text_channels:
                try:
                    mensagens = await channel.purge(limit=None)
                    total_mensagens += len(mensagens)
                except Exception as e:
                    await ctx.send(f"⚠️ Erro ao apagar `{channel.name}`: {str(e)}")

            await ctx.send(f"✅ `{total_mensagens}` mensagens foram apagadas de todos os canais!")
        except Exception as e:
            await ctx.send(f"❌ Erro ao executar o comando nukechannels: {str(e)}")


class ExtremeNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def extremenuke(self, ctx):
        """Exclui e recria apenas o canal onde o comando foi usado, com opção de cancelamento."""
        try:
            mensagem_aviso = await ctx.send("🚨 Este canal será excluído e recriado! Reaja com ❌ para cancelar!")
            await mensagem_aviso.add_reaction("❌")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "❌" and reaction.message.id == mensagem_aviso.id

            if await self.confirmar_cancelamento(ctx, mensagem_aviso):
             return

            nome_canal = ctx.channel.name
            categoria = ctx.channel.category
            await ctx.channel.delete()
            novo_canal = await ctx.guild.create_text_channel(nome_canal, category=categoria)
            await novo_canal.send(f"✅ Canal `{nome_canal}` recriado com sucesso!")
        except Exception as e:
            await ctx.send(f"❌ Erro ao executar o comando ExtremeNuke: {str(e)}")


class ExtremeNukeChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def extremenukechannels(self, ctx):
        """Exclui e recria todos os canais de texto do servidor, com opção de cancelamento."""
        try:
            mensagem_aviso = await ctx.send("🚨 Todos os canais serão excluídos! Reaja com ❌ para cancelar!")
            await mensagem_aviso.add_reaction("❌")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "❌" and reaction.message.id == mensagem_aviso.id

            if await self.confirmar_cancelamento(ctx, mensagem_aviso):
             return

            canais_originais = [(c.name, c.category) for c in ctx.guild.text_channels]

            for channel in ctx.guild.text_channels:
                try:
                    await channel.delete()
                except Exception as e:
                    await ctx.send(f"⚠️ Erro ao excluir `{channel.name}`: {str(e)}")

            for nome, categoria in canais_originais:
                try:
                    novo_canal = await ctx.guild.create_text_channel(nome, category=categoria)
                    await novo_canal.send(f"✅ Canal `{nome}` recriado!")
                except Exception as e:
                    await ctx.send(f"⚠️ Erro ao recriar `{nome}`: {str(e)}")

            await ctx.send("🔥 Todos os canais foram recriados!")
        except Exception as e:
            await ctx.send(f"❌ Erro ao executar o comando ExtremeNukeChannels: {str(e)}")

import discord
from discord.ext import commands
import asyncio

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        """Apaga todas as mensagens do canal escolhido ou do canal onde o comando foi usado."""
        canal_alvo = channel if channel else ctx.channel
        try:
            mensagens = await canal_alvo.purge(limit=None)
            total_mensagens = len(mensagens)
            await ctx.send(f"💥 `{total_mensagens}` mensagens foram apagadas no canal `{canal_alvo.name}`! 🔥")
        except Exception as e:
            await ctx.send(f"❌ Erro ao executar o comando Nuke: {str(e)}")


class ExtremeNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def extremenuke(self, ctx, channel: discord.TextChannel = None):
        """Exclui e recria um canal específico ou o canal onde o comando foi usado, com opção de cancelamento."""
        canal_alvo = channel if channel else ctx.channel
        try:
            mensagem_aviso = await ctx.send(f"🚨 **ATENÇÃO!** O canal `{canal_alvo.name}` será excluído e recriado!\n"
                                            "Reaja com ❌ dentro de 10 segundos para cancelar!")
            await mensagem_aviso.add_reaction("❌")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "❌" and reaction.message.id == mensagem_aviso.id

            for segundos in range(10, 0, -1):
                await mensagem_aviso.edit(content=f"🚨 **ATENÇÃO!** `{canal_alvo.name}` será excluído e recriado!\n"
                                                  f"Reaja com ❌ para cancelar! **{segundos} segundos restantes...**")
                try:
                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=1, check=check)
                    await ctx.send("❌ **Comando cancelado!** Nenhum canal foi excluído.")
                    return
                except asyncio.TimeoutError:
                    pass  

            nome_canal = canal_alvo.name
            categoria = canal_alvo.category
            await canal_alvo.delete()
            novo_canal = await ctx.guild.create_text_channel(nome_canal, category=categoria)
            await novo_canal.send(f"✅ Canal `{novo_canal.name}` recriado com sucesso!")

        except Exception as e:
            await ctx.send(f"❌ Erro ao executar o comando ExtremeNuke: {str(e)}")

async def confirmar_cancelamento(self, ctx, mensagem_aviso):
    await mensagem_aviso.add_reaction("❌")
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "❌" and reaction.message.id == mensagem_aviso.id

    try:
        await self.bot.wait_for("reaction_add", timeout=10, check=check)
        await ctx.send("❌ **Comando cancelado!** Nenhum canal foi excluído.")
        return True  # Retorna True se o comando for cancelado
    except asyncio.TimeoutError:
        return False  # Retorna False se não houver reação

async def setup(bot):
    await bot.add_cog(Nuke(bot))
    await bot.add_cog(ExtremeNuke(bot))

async def setup(bot):
    await bot.add_cog(Nuke(bot))
    await bot.add_cog(NukeChannels(bot))
    await bot.add_cog(ExtremeNuke(bot))
    await bot.add_cog(ExtremeNukeChannels(bot))