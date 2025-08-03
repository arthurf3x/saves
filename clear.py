import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Apaga mensagens recentes no canal."""
        await ctx.channel.purge(limit=amount + 1)  # +1 para remover o comando do usuário
        await ctx.send(f":white_check_mark: {amount} mensagens foram apagadas!", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearp(self, ctx, member: discord.Member, amount: int = None):
        """Apaga mensagens recentes de um usuário específico."""
        if amount:
            # Apaga apenas a quantidade de mensagens especificada
            deleted = await ctx.channel.purge(limit=amount, check=lambda m: m.author == member)
            await ctx.send(f":white_check_mark: {len(deleted)} mensagens recentes de {member.mention} foram apagadas!", delete_after=5)
        else:
            # Se não especificar quantidade, apaga todas as mensagens do usuário
            deleted = await ctx.channel.purge(limit=500, check=lambda m: m.author == member)
            await ctx.send(f":white_check_mark: Todas as mensagens recentes de {member.mention} foram apagadas!", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def oldclear(self, ctx, amount: int):
        """Apaga mensagens mais antigas no canal."""
        await ctx.channel.purge(limit=amount + 1, oldest_first=True)
        await ctx.send(f":white_check_mark: {amount} mensagens antigas foram apagadas!", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def oldclearp(self, ctx, member: discord.Member, amount: int = None):
        """Apaga mensagens antigas de um usuário específico."""
        
        messages = [message async for message in ctx.channel.history(limit=500, oldest_first=True)]
        user_messages = [m for m in messages if m.author == member]

        if amount:
            to_delete = user_messages[:amount]  # Pegamos apenas a quantidade informada
        else:
            to_delete = user_messages  # Se não informar quantidade, apagamos todas as encontradas

        if to_delete:
            await ctx.channel.delete_messages(to_delete)
            await ctx.send(f":white_check_mark: {len(to_delete)} mensagens antigas de {member.mention} foram apagadas!", delete_after=5)
        else:
            await ctx.send(f":x: Nenhuma mensagem antiga encontrada para {member.mention}.", delete_after=5)

async def setup(bot):
    """Configuração da cog para a pasta admins."""
    await bot.add_cog(Clear(bot))
