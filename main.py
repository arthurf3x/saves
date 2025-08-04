import discord
from discord.ext import commands
import os
from config import TOKEN  # Mantendo o token no config.py

# Habilitar os intents necessários
intents = discord.Intents.default()
intents.message_content = True

# Criar o bot com suporte a comandos slash
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

# Função para carregar todos os cogs corretamente, inclusive os de subdiretórios
async def load_cogs():
    for dirpath, _, filenames in os.walk("./cogs"):
        for filename in filenames:
            if not filename.endswith(".py") or filename in ["__init__.py", "identifier.py"]:
                continue

            cog_name = dirpath.replace(os.sep, ".")[2:] + "." + filename[:-3]
            if cog_name == "cogs.admin":
                continue

            print(f"Tentando carregar o cog: {cog_name}")
            try:
                await bot.load_extension(cog_name)
                print(f"✅ Cog carregado: {cog_name}")
            except Exception as e:
                print(f"❌ Erro ao carregar {cog_name}: {e}")

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user} ({bot.user.id})")
    print(f"🌐 Conectado a {len(bot.guilds)} servidores!")

    await load_cogs()

    try:
        synced = await bot.tree.sync()
        print(f"🔧 Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(f"❌ Erro ao sincronizar comandos slash: {e}")

# Sistema de identificação de usuário e menções
@bot.event
async def on_message(message):
    if message.mentions:
        for mentioned in message.mentions:
            if mentioned.bot:
                continue
    await bot.process_commands(message)

# Iniciar o bot
bot.run(TOKEN)