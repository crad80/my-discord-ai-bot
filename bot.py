import os
import threading
from flask import Flask
import discord
from discord.ext import commands
from dotenv import load_dotenv

from openai import OpenAI
from google import genai  # Google 공식 최신 SDK
import anthropic

load_dotenv()

# Render 포트 타임아웃 방지용 웹서버
app = Flask('')

@app.route('/')
def home():
    return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.start()

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

# 2. Gemini (최신 SDK 호출 방식)
@bot.command(name="gemini")
async def ask_gemini(ctx, *, prompt: str):
    if not GEMINI_API_KEY:
        await ctx.send("Gemini API 키가 설정되지 않았습니다.")
        return
    async with ctx.typing():
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            await ctx.send(f"**[Gemini]**\n{response.text}")
        except Exception as e:
            await ctx.send(f"**[Gemini 오류]** {e}")

# 3. Claude (최신 표준 모델명)
@bot.command(name="claude")
async def ask_claude(ctx, *, prompt: str):
    if not CLAUDE_API_KEY:
        await ctx.send("Claude API 키가 설정되지 않았습니다.")
        return
    async with ctx.typing():
        try:
            client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
            response = client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            await ctx.send(f"**[Claude]**\n{response.content[0].text}")
        except Exception as e:
            await ctx.send(f"**[Claude 오류]** {e}")

# 4. Grok
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

if __name__ == "__main__":
    keep_alive()
    bot.run(DISCORD_TOKEN)
