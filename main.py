import os
import re
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# สร้างเว็บเซิร์ฟเวอร์รับพอร์ตเพื่อตอบสนอง Render (Web Service Health Check)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# รันเว็บเซิร์ฟเวอร์ไว้เบื้องหลัง
threading.Thread(target=run_server, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ปรับ Regex ให้ครอบคลุมลิงก์เชิญทุกรูปแบบ
INVITE_REGEX = r"(https?://)?(www\.)?(discord\(app\)?\.com/invite|discord\.gg)/[a-zA-Z0-9]+"

@bot.event
async def on_ready():
    print(f"บอทออนไลน์แล้วในชื่อ: {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ตรวจจับลิงก์เชิญ
    if re.search(INVITE_REGEX, message.content, re.IGNORECASE):
        try:
            await message.delete()
            await message.channel.send(
                f"⚠️ {message.author.mention} ห้ามส่งลิงก์ดิสอื่นในเซิร์ฟเวอร์นี้!",
                delete_after=5,
            )
            print(f"Deleted invite link from {message.author}")
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
