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
        await ctx.send(f"✅ {amount} mensagens foram apagadas!", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearp(self, ctx, member: discord.Member, amount: int = None):
        """Apaga mensagens recentes de um usuário específico."""
        if amount:
            deleted = await ctx.channel.purge(limit=amount, check=lambda m: m.author == member)
            await ctx.send(f"✅ {len(deleted)} mensagens recentes de {member.mention} foram apagadas!", delete_after=5)
        else:
            deleted = await ctx.channel.purge(limit=500, check=lambda m: m.author == member)
            await ctx.send(f"✅ Todas as mensagens recentes de {member.mention} foram apagadas!", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def oldclear(self, ctx, amount: int):
        """Apaga mensagens mais antigas no canal."""
        await ctx.channel.purge(limit=amount + 1, oldest_first=True)
        await ctx.send(f"✅ {amount} mensagens antigas foram apagadas!", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def oldclearp(self, ctx, member: discord.Member, amount: int = None):
        """Apaga mensagens antigas de um usuário específico."""
        messages = [message async for message in ctx.channel.history(limit=500, oldest_first=True)]
        user_messages = [m for m in messages if m.author == member]

        if amount:
            to_delete = user_messages[:amount]
        else:
            to_delete = user_messages

        if to_delete:
            await ctx.channel.delete_messages(to_delete)
            await ctx.send(f"✅ {len(to_delete)} mensagens antigas de {member.mention} foram apagadas!", delete_after=5)
        else:
            await ctx.send(f"❌ Nenhuma mensagem antiga encontrada para {member.mention}.", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearallp(self, ctx, member: discord.Member):
        """Apaga mensagens de um usuário em todos os canais do servidor."""
        deleted_count = 0
        for channel in ctx.guild.text_channels:
            try:
                messages = [msg async for msg in channel.history(limit=1000) if msg.author == member]
                recent_msgs = [m for m in messages if (discord.utils.utcnow() - m.created_at).days < 14]
                old_msgs = [m for m in messages if (discord.utils.utcnow() - m.created_at).days >= 14]

                if recent_msgs:
                    await channel.delete_messages(recent_msgs)
                    deleted_count += len(recent_msgs)

                for msg in old_msgs:
                    try:
                        await msg.delete()
                        deleted_count += 1
                    except (discord.Forbidden, discord.HTTPException):
                        pass

            except (discord.Forbidden, discord.HTTPException):
                continue

        await ctx.send(f"✅ Foram apagadas {deleted_count} mensagens de {member.mention} em todo o servidor!", delete_after=10)

async def setup(bot):
    """Configuração da cog para a pasta admins."""
    await bot.add_cog(Clear(bot))