import os
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# สร้าง Health Check Server สำหรับ Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
    def log_message(self, format, *args):
        return

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_http_server, daemon=True)
server_thread.start()

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

    # แปลงข้อความให้เป็นตัวพิมพ์เล็กทั้งหมดเพื่อเช็กคำง่ายขึ้น
    content = message.content.lower()

    # เช็กคำว่า discord.gg หรือ invite ในข้อความ (ครอบคลุมทุกลิงก์ชวนเพื่อน)
    if "discord.gg/" in content or "discord.com/invite/" in content or "discordapp.com/invite/" in content:
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

TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN not found.")
