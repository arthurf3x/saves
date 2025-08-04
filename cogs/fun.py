import discord
import random
import aiohttp
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ultima_piada = None  # Variável para armazenar a última piada

        # Lista de piadas personalizadas
        self.piadas_fixas = [
            "O que o pato disse para a pata? R.: Vem Quá!",
            "Por que o menino estava falando ao telefone deitado? R.: Para não cair a ligação.",
            "Qual é a fórmula da água benta? R.: H Deus O!"
        ]

    @commands.command()
    async def piada(self, ctx):
        """Conta uma piada aleatória misturando API e lista fixa."""
        usar_api = random.choice([True, False])

        if usar_api:
            url = "https://v2.jokeapi.dev/joke/Any?lang=pt"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    nova_piada = data["joke"] if data["type"] == "single" else f"{data['setup']}\n{data['delivery']}"
        else:
            nova_piada = random.choice(self.piadas_fixas)

        await ctx.reply(nova_piada)

    @commands.command()
    async def Pedro(self, ctx):
        """Responde com uma frase aleatória."""
        frases = [
            "Pedro rebola de ladinho pros cria",
            "ain pedrinho apelão",
            "Pedro é o rei do rebolado!"
        ]
        await ctx.reply(random.choice(frases))

    @commands.command()
    async def eae(self, ctx):
        """Cumprimenta o usuário."""
        nome = ctx.author.display_name
        await ctx.reply(f"eae {nome}, blz?")

    @commands.command()
    async def guess(self, ctx):
        """Jogo de adivinhação via reações."""
        numero_correto = random.randint(1, 10)
        mensagem = await ctx.send("🎲 Escolha um número entre 1 e 10 clicando na reação abaixo!")

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for emoji in emojis:
            await mensagem.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == mensagem.id and reaction.emoji in emojis

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except TimeoutError:
            await ctx.send("⏳ Tempo esgotado! Tente novamente.")
            return

        escolha_usuario = emojis.index(reaction.emoji) + 1

        if escolha_usuario == numero_correto:
            await ctx.send(f"🎉 Parabéns, {ctx.author.mention}! Você acertou! O número era {numero_correto}.")
        else:
            await ctx.send(f"❌ Errado! O número era {numero_correto}. Tente novamente!")

import discord
import random
import aiohttp
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ultima_piada = None  # Variável para armazenar a última piada

        # Lista de piadas personalizadas
        self.piadas_fixas = [
"O que o pato disse para a pata? R.: Vem Quá!",
            "Por que o menino estava falando ao telefone deitado? R.: Para não cair a ligação.",
            "A enfermeira diz ao médico:\n- Tem um homem invisível na sala de espera.\nO médico responde:\n- Diga a ele que não posso vê-lo agora.",
            "Qual é a fórmula da água benta? R.: H Deus O!",
            "O sujeito vai ao médico:\n– Doutor, tenho tendências suicidas. O que faço?\n– Em primeiro lugar, pague a consulta.",
            "Qual a diferença entre um padre e um tenista?\nR.: As bolas com que o tenista brinca têm pelinhos.",
            "Porque é que a Anne Frank não acabou o diário?\nR. :Problemas de concentração.",
            "sabe por que michael jackson não pode dirigir um onibus?/nR. :por que ele esta morto.",
            "Sabias que sem árabes não tinha acontecido o 11/9?\nR:. Tinha acontecido o XI/IX.",
            "Qual é a diferença entre uma pizza e um judeu?\nR:. A pizza quando vai ao forno não grita.",
            "Por que o livro de matemática cometeu suicídio?\nR:. — Porque tinha muitos problemas.",
            "Um cego entra numa loja, pega o seu cão-guia e começa a balançá-lo sobre a sua cabeça.\nR: – O que você está fazendo? \nR:– Ah, só dando uma olhada. ",
            "– Com licença, qual é a senha do Wi-Fi aqui?\nR: – Isso é um funeral! \nR:– Funeral com letra inicial maiúscula ou minúscula?",
            "Os nascidos em 2000 facilitaram muito para as pessoas que passam por seus túmulos calcular a idade."
        ]

    @commands.command()
    async def piada(self, ctx):
        """Conta uma piada aleatória misturando API e lista fixa."""
        usar_api = random.choice([True, False])

        if usar_api:
            url = "https://v2.jokeapi.dev/joke/Any?lang=pt"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    nova_piada = data["joke"] if data["type"] == "single" else f"{data['setup']}\n{data['delivery']}"
        else:
            nova_piada = random.choice(self.piadas_fixas)

        await ctx.reply(nova_piada)

    @commands.command()
    async def Pedro(self, ctx):
        """Responde com uma frase aleatória."""
        frases = [
            "Pedro rebola de ladinho pros cria",
            "ain pedrinho apelão",
            "Pedro é o rei do rebolado!"
        ]
        await ctx.reply(random.choice(frases))

    @commands.command()
    async def eae(self, ctx):
        """Cumprimenta o usuário."""
        nome = ctx.author.display_name
        await ctx.reply(f"eae {nome}, blz?")

    @commands.command()
    async def guess(self, ctx):
        """Jogo de adivinhação via reações."""
        numero_correto = random.randint(1, 10)
        mensagem = await ctx.send("🎲 Escolha um número entre 1 e 10 clicando na reação abaixo!")

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for emoji in emojis:
            await mensagem.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == mensagem.id and reaction.emoji in emojis

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except TimeoutError:
            await ctx.send("⏳ Tempo esgotado! Tente novamente.")
            return

        escolha_usuario = emojis.index(reaction.emoji) + 1

        if escolha_usuario == numero_correto:
            await ctx.send(f"🎉 Parabéns, {ctx.author.mention}! Você acertou! O número era {numero_correto}.")
        else:
            await ctx.send(f"❌ Errado! O número era {numero_correto}. Tente novamente!")

    @commands.command()
    async def randomroll(self, ctx, quantidade: int = None, intervalo: int = None):
        """Sorteia múltiplos números dentro de um intervalo escolhido pelo usuário (Ex: !randomroll 4 10)."""

        if quantidade is None or intervalo is None:
            await ctx.reply("❌ Você precisa fornecer a quantidade de números e o intervalo! Exemplo: `!randomroll 4 10`")
            return

        if quantidade < 1 or quantidade > intervalo:
            await ctx.reply("❌ A quantidade deve ser menor ou igual ao intervalo! Exemplo: `!randomroll 4 10`")
            return

        numeros_sorteados = random.sample(range(1, intervalo + 1), quantidade)
        await ctx.reply(f"🎲 Os {quantidade} números sorteados dentro do intervalo de 1 a {intervalo} foram: {', '.join(map(str, numeros_sorteados))}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
async def setup(bot):
    await bot.add_cog(Fun(bot))