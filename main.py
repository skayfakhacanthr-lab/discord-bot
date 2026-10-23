import os
import re
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Web server สำหรับหลอกพอร์ต Render
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    # ป้องกันไม่ให้บอทลบข้อความของตัวเอง
    if message.author == bot.user:
        return

    # เช็กคำว่า discord.gg หรือ discord.com/invite ในข้อความ
    content = message.content.lower()
    if "discord.gg/" in content or "discord.com/invite/" in content or "discordapp.com/invite/" in content:
        try:
            await message.delete()
            await message.channel.send(
                f"⚠️ {message.author.mention} ห้ามส่งลิงก์ดิสอื่นในเซิร์ฟเวอร์นี้!",
                delete_after=5
            )
            print(f"Deleted invite link from {message.author}")
        except Exception as e:
            print(f"Error deleting message: {e}")

    await bot.process_commands(message)

TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN not found!")
