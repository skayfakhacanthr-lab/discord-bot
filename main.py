import os
import time
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Health Check Server สำหรับ Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        return

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), SimpleHandler).serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()

INVITE_PATTERNS = ("discord.gg/", "discord.com/invite/", "discordapp.com/invite/")

def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        content = message.content.lower()
        if any(p in content for p in INVITE_PATTERNS):
            try:
                await message.delete()
                await message.channel.send(
                    f"⚠️ {message.author.mention} ห้ามส่งลิงก์ดิสอื่นในเซิร์ฟเวอร์นี้!",
                    delete_after=5,
                )
                print(f"Deleted invite link from {message.author}")
            except discord.Forbidden:
                print("Error: บอทไม่มีสิทธิ์ Manage Messages")
            except Exception as e:
                print(f"Error: {e}")

        await bot.process_commands(message)

    return bot

TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found.")
    else:
        delay = 60
        while True:
            try:
                create_bot().run(TOKEN)
                break  # ปิดตามปกติ
            except discord.HTTPException as e:
                print(f"HTTP error {e.status}: โดน rate limit/บล็อก รอ {delay}s แล้วลองใหม่")
            except Exception as e:
                print(f"Unexpected error: {e} รอ {delay}s แล้วลองใหม่")
            time.sleep(delay)
            delay = min(delay * 2, 1800)  # สูงสุด 30 นาที
