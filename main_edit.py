import discord
import random
import csv
import logging
import asyncio

# === 設定區 ===
csv_file_path = "./message.csv"
channel_id = 0000000000000000
message_id = 0000000000000000  # <-- 你自己事先送出的訊息 ID
discord_token = ""  # <-- 換成你自己的 Token

# === 初始化 logging ===
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
console_handler = logging.StreamHandler()
logging.basicConfig(
    handlers=[handler, console_handler],
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

# === 載入字串訊息 ===
def load_messages_from_csv(file_path):
    messages = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            messages.append({
                "title": row["title"],
                "message": row["message"],
                "final": row["final"]
            })
    return messages

string_list = load_messages_from_csv(csv_file_path)

def get_sea_string():
    random.shuffle(string_list)
    return string_list[0]

# === Discord bot 建立 ===
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
cooldown_lock = asyncio.Lock()

class SeaButtonHandler(discord.ui.Button):
    def __init__(self, label, style):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        message = get_sea_string()
        embed = discord.Embed(
            title=message["title"],
            description="➤ " + message["message"],
            color=0x007bff
        )
        embed.set_author(name="海港事件")
        embed.add_field(name="事件結果", value="• " + message["final"], inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class JobButtonHandler(discord.ui.Button):
    def __init__(self, label, style):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        new_view = discord.ui.View(timeout=30)
        new_view.add_item(SeaButtonHandler(label="海港", style=discord.ButtonStyle.success))
        await interaction.response.send_message("> 去跳海吧", view=new_view, ephemeral=True)

def generate_main_view():
    view = discord.ui.View(timeout=60)

    view.clear_items()
    view.add_item(JobButtonHandler(label="工作", style=discord.ButtonStyle.primary))

    async def on_timeout():
        logging.info("View timeout，自動更新按鈕")
        print("View 已超時，重新生成按鈕。")
        await asyncio.sleep(3)
        await update_view_only()

    view.on_timeout = on_timeout
    return view

# === 核心函數：更新指定訊息的 View ===
async def update_view_only():
    global message_id
    channel = client.get_channel(channel_id)
    if not channel:
        logging.error("找不到頻道")
        return

    async with cooldown_lock:
        try:
            sent_message = await channel.fetch_message(message_id)
            view = generate_main_view()
            await sent_message.edit(view=view)
            logging.info(f"訊息 {message_id} 已更新 view。")
        except discord.NotFound:
            logging.warning(f"找不到訊息 ID：{message_id}，請確認該訊息仍存在")
        except discord.Forbidden:
            logging.error("Bot 沒有編輯訊息的權限")
        except discord.HTTPException as e:
            logging.exception(f"HTTP 發生錯誤：{e}")

# === 事件 ===
@client.event
async def on_ready():
    logging.info(f"Bot 登入為 {client.user}")
    await update_view_only()

@client.event
async def on_resumed():
    await update_view_only()

@client.event
async def on_error(event, *args, **kwargs):
    logging.exception(f"錯誤事件: {event} {args} {kwargs}")

# === 執行 Bot ===
client.run(discord_token, log_handler=handler, log_level=logging.INFO)
