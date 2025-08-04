import discord
from discord.ext import commands
import os
from config import TOKEN  # Mantendo o token no config.py

# Habilitar os intents necessários
intents = discord.Intents.default()
intents.message_content = True  # Permissão para ler conteúdo das mensagens

# Criar o bot e tornar os comandos insensíveis a maiúsculas e minúsculas
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

# Função para carregar todos os cogs corretamente, inclusive os de subdiretórios
async def load_cogs():
    for dirpath, _, filenames in os.walk("./cogs"):
        for filename in filenames:
            # Ignorar arquivos não .py, __init__.py, identifier.py
            if not filename.endswith(".py") or filename in ["__init__.py", "identifier.py"]:
                continue

            # Formatando o nome do cog corretamente, incluindo subdiretórios
            cog_name = dirpath.replace(os.sep, ".")[2:] + "." + filename[:-3]

            # Ignorar a pasta cogs/admin como cog diretamente
            if cog_name == "cogs.admin":
                continue

            print(f"Tentando carregar o cog: {cog_name}")  # Depuração
            try:
                await bot.load_extension(cog_name)
                print(f"✅ Cog carregado: {cog_name}")
            except Exception as e:
                print(f"❌ Erro ao carregar {cog_name}: {e}")

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user} ({bot.user.id})")
    print(f"🌐 Conectado a {len(bot.guilds)} servidores!")
    await load_cogs()  # Carregar os cogs ao iniciar

# Sistema de identificação de usuário e menções
@bot.event
async def on_message(message):
    if message.mentions:
        for mentioned in message.mentions:
            if mentioned.bot:
                continue  # Ignorar bots

    await bot.process_commands(message)  # Permite que comandos ainda funcionem
