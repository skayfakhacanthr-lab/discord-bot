import os
import re
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

INVITE_REGEX = r"(https?://)?(www\.)?(discord\(app\)?\.com/invite|discord\.gg)/[a-zA-Z0-9]+"

@bot.event
async def on_ready():
    print(f"บอทออนไลน์แล้วในชื่อ: {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if re.search(INVITE_REGEX, message.content):
        try:
            await message.delete()
            await message.channel.send(
                f"⚠️ {message.author.mention} ห้ามส่งลิงก์เชิญ Discord ในช่องนี้ครับ!",
                delete_after=5,
            )
        except discord.Forbidden:
            print("เกิดข้อผิดพลาด: บอทไม่มีสิทธิ์ Manage Messages ในการลบข้อความนี้")
        except discord.HTTPException as e:
            print(f"เกิดข้อผิดพลาดในการลบข้อความ: {e}")

    await bot.process_commands(message)

TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ไม่พบ DISCORD_TOKEN ใน Environment Variables")
