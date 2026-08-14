import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from openai import OpenAI
import google.generativeai as genai
import anthropic

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"로그인 성공: {bot.user.name}")

# 1. ChatGPT
@bot.command(name="gpt")
async def ask_gpt(ctx, *, prompt: str):
    if not OPENAI_API_KEY:
        await ctx.send("OpenAI API 키가 설정되지 않았습니다.")
        return
    async with ctx.typing():
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            await ctx.send(f"**[ChatGPT]**\n{response.choices[0].message.content}")
        except Exception as e:
            await ctx.send(f"**[ChatGPT 오류]** {e}")

# 2. Gemini (수정: gemini-1.5-flash-latest)
@bot.command(name="gemini")
async def ask_gemini(ctx, *, prompt: str):
    if not GEMINI_API_KEY:
        await ctx.send("Gemini API 키가 설정되지 않았습니다.")
        return
    async with ctx.typing():
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(prompt)
            await ctx.send(f"**[Gemini]**\n{response.text}")
        except Exception as e:
            await ctx.send(f"**[Gemini 오류]** {e}")

# 3. Claude (수정: claude-3-haiku-20240307)
@bot.command(name="claude")
async def ask_claude(ctx, *, prompt: str):
    if not CLAUDE_API_KEY:
        await ctx.send("Claude API 키가 설정되지 않았습니다.")
        return
    async with ctx.typing():
        try:
            client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            await ctx.send(f"**[Claude]**\n{response.content[0].text}")
        except Exception as e:
            await ctx.send(f"**[Claude 오류]** {e}")

# 4. Grok (수정: grok-2-latest)
@bot.command(name="grok")
async def ask_grok(ctx, *, prompt: str):
    if not GROK_API_KEY:
        await ctx.send("Grok API 키가 설정되지 않았습니다.")
        return
    async with ctx.typing():
        try:
            client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")
            response = client.chat.completions.create(
                model="grok-2-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            await ctx.send(f"**[Grok]**\n{response.choices[0].message.content}")
        except Exception as e:
            await ctx.send(f"**[Grok 오류]** {e}")

bot.run(DISCORD_TOKEN)
