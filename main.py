import os
import re
import asyncio
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# เปิดเว็บเซิร์ฟเวอร์จำลองเพื่อตอบรับพอร์ตของ Render (แก้ปัญหา No open ports detected)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Discord Bot is active!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# รันเว็บเซิร์ฟเวอร์ควบคู่กับบอท Discord ในเบื้องหลัง
threading.Thread(target=run_web_server, daemon=True).start()

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
                f"⚠️ {message.author.mention} ห้ามส่งลิงก์ดิสอื่นในเซิร์ฟเวอร์นี้!",
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
