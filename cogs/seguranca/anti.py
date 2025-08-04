import discord
from discord.ext import commands

# Lista de IDs autorizados a usar o comando
USERS_AUTORIZADOS = [1357895535775846403, 779876283890008095]  # Substitua com os seus IDs reais

class Giveroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="giveroles")
    async def giveroles(self, ctx, member: discord.Member = None):
        """Comando para dar todos os cargos ao membro especificado."""

        # Verifica se o autor do comando está na lista de autorizados
        if ctx.author.id not in USERS_AUTORIZADOS:
            return await ctx.send("❌ Você não tem permissão para usar esse comando.")

        # Se o membro não for especificado, avisa o usuário
        if not member:
            return await ctx.send("❌ Você precisa mencionar um membro para adicionar os cargos.")

        # Verifica se o membro especificado é o bot (para evitar que o bot se adicione cargos)
        if member == ctx.guild.me:
            return await ctx.send("❌ Não posso adicionar cargos a mim mesmo.")

        # Obtém todos os cargos do servidor
        cargos_validos = [role for role in ctx.guild.roles if role != ctx.guild.default_role and role <= ctx.guild.me.top_role]

        # Adiciona todos os cargos ao membro
        try:
            await member.add_roles(*cargos_validos, reason="Todos os cargos adicionados por comando")
            await ctx.send(f"✅ Todos os cargos foram adicionados a {member.mention}.")
        except discord.Forbidden:
            await ctx.send("❌ Permissões insuficientes para adicionar cargos.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Erro ao adicionar cargos: {e}")

async def setup(bot):
    await bot.add_cog(Giveroles(bot))
