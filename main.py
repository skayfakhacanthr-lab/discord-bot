import os
import re
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# สร้าง Health Check Server สำหรับ Render โดยเฉพาะ
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
    def log_message(self, format, *args):
        return # ปิด Log ขยะเพื่อไม่ให้รกหน้าจอ

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# รัน HTTP Server แยกออกไปอีก Thread หนึ่งทันที
server_thread = threading.Thread(target=run_http_server, daemon=True)
server_thread.start()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

INVITE_REGEX = r"(https?://)?(www\.)?(discord\(app\)?\.com/invite|discord\.gg)/[a-zA-Z0-9]+"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if re.search(INVITE_REGEX, message.content, re.IGNORECASE):
        try:
            await message.delete()
            await message.channel.send(
                f"⚠️ {message.author.mention} ห้ามส่งลิงก์ดิสอื่นในเซิร์ฟเวอร์นี้!",
                delete_after=5,
            )
        except Exception as e:
            print(f"Error: {e}")

    await bot.process_commands(message)

TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN not found.")
