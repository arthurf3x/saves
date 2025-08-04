import discord
import google.generativeai as genai
import random
import asyncio
from discord.ext import commands

# 🔥 Sua API KEY da Gemini (Google AI)
genai.configure(api_key="AIzaSyA1Z-XHMJLaZdLOftnyvJRY8A22gWazcrs")

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores = {}  # Armazena pontos dos jogadores
        self.active_quiz = {}  # Armazena quizzes ativos por servidor

    async def generate_question(self):
        """Gera uma pergunta e sua resposta usando Gemini."""
        print("🔄 Gerando pergunta...")

        model = genai.GenerativeModel('gemini-pro')

        prompt = (
            "Crie uma pergunta desafiadora para um quiz de múltiplas áreas como História, Ciência, Matemática, Tecnologia ou Cultura Geral. "
            "Responda no formato: Pergunta | Resposta"
        )

        response = model.generate_content(prompt)
        content = response.text

        try:
            question, answer = content.split("|")
        except:
            question, answer = content, "Resposta não disponível"

        print(f"📌 Pergunta gerada: {question}")
        return question.strip(), answer.strip()

    async def check_answer(self, user_answer, correct_answer):
        """Verifica se a resposta do usuário está correta (checagem simples)."""
        return user_answer.lower().strip() in correct_answer.lower().strip()

    @commands.command(name="quiz")
    async def quiz(self, ctx, num_questions: int = 5):
        """Inicia um quiz multiplayer com perguntas geradas pela IA."""
        if ctx.guild.id in self.active_quiz:
            await ctx.send("❌ Já existe um quiz ativo neste servidor! Aguarde ele terminar.")
            return

        self.active_quiz[ctx.guild.id] = True
        answered_users = set()

        await ctx.send(f"🎉 **Quiz iniciado!** {num_questions} perguntas. Responda corretamente para ganhar pontos!")

        for i in range(num_questions):
            question, correct_answer = await self.generate_question()

            if correct_answer == "Resposta não disponível":
                await ctx.send("⚠️ Erro ao gerar a pergunta! Pulando para a próxima...")
                continue

            msg = await ctx.send(f"🧠 Pergunta {i + 1}/{num_questions}: {question}\n⏳ Tempo restante: **15s**")

            for time_left in range(14, 0, -1):
                await asyncio.sleep(1)
                await msg.edit(content=f"🧠 Pergunta {i + 1}/{num_questions}: {question}\n⏳ Tempo restante: **{time_left}s**")

            def check(m):
                return m.channel == ctx.channel and m.author not in answered_users and not m.author.bot

            try:
                response = await self.bot.wait_for("message", timeout=15.0, check=check)

                if response:
                    is_correct = await self.check_answer(response.content, correct_answer)

                    if is_correct:
                        user = response.author
                        points = max(5, int(50 - (15 - time_left) * 3))  # Pontuação baseada no tempo

                        self.scores[user] = self.scores.get(user, 0) + points

                        await ctx.send(f"✅ {user.mention} acertou! Pontos ganhos: {points}")
                        answered_users.add(user)

                    else:
                        await ctx.send(f"❌ {response.author.mention} errou! Tente na próxima pergunta.")
                        answered_users.add(response.author)

            except asyncio.TimeoutError:
                await ctx.send("⏰ Tempo esgotado para essa pergunta!")

        self.active_quiz.pop(ctx.guild.id)
        await ctx.send("🎉 **Quiz encerrado!**")

        if self.scores:
            ranking = "\n".join(f"🏅 {user}: {score} pontos" for user, score in sorted(self.scores.items(), key=lambda x: x[1], reverse=True))
            await ctx.send(f"**🏆 Ranking final:**\n{ranking}")
        else:
            await ctx.send("😢 Ninguém marcou pontos nesse quiz.")

async def setup(bot):
    await bot.add_cog(Quiz(bot))
