import discord
from discord.ext import commands, tasks
import sqlite3
import json
from datetime import datetime
import asyncio

TOKEN="your token" 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
user_cache = {}

BIRTHDAYS_FILE = "sent_birthdays.json"

def load_sent_birthdays():
    try:
        with open(BIRTHDAYS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_sent_birthdays(data):
    with open(BIRTHDAYS_FILE, "w") as f:
        json.dump(data, f, indent=4)

sent_birthdays = load_sent_birthdays()

def get_db_connection():
    return sqlite3.connect("birthdays.db")

def setup_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS birthdays (
                user_id INTEGER PRIMARY KEY,
                birthday TEXT
            );
            CREATE TABLE IF NOT EXISTS birthday_messages (
                guild_id INTEGER PRIMARY KEY,
                message TEXT DEFAULT '🎉 ¡Feliz cumpleaños {mention}! 🎂🎁',
                image_url TEXT
            );
            CREATE TABLE IF NOT EXISTS birthday_channels (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER
            );
        ''')
        conn.commit()
setup_database()

@bot.command()
@commands.has_permissions(administrator=True)
async def add_birthday(ctx, member: discord.Member, date: str):
    try:
        datetime.strptime(date, "%m-%d")
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("REPLACE INTO birthdays (user_id, birthday) VALUES (?, ?)", (member.id, date))
            conn.commit()
        await ctx.send(f"🎉 Cumpleaños de {member.mention} registrado para {date}!")
    except ValueError:
        await ctx.send("⚠️ Formato incorrecto. Usa MM-DD.")

@bot.command()
@commands.has_permissions(administrator=True)
async def remove_birthday(ctx, member: discord.Member):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM birthdays WHERE user_id = ?", (member.id,))
        conn.commit()
    await ctx.send(f"❌ Cumpleaños de {member.mention} eliminado.")

@bot.command()
async def birthdays(ctx):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, birthday FROM birthdays")
        rows = cursor.fetchall()
    if rows:
        message = "🎂 Lista de cumpleaños:\n" + '\n'.join(f"<@{user_id}>: {birthday}" for user_id, birthday in rows)
        await ctx.send(message)
    else:
        await ctx.send("📭 No hay cumpleaños registrados.")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_birthday_channel(ctx, channel: discord.TextChannel):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO birthday_channels (guild_id, channel_id) VALUES (?, ?)", (ctx.guild.id, channel.id))
        conn.commit()
    await ctx.send(f"📢 Canal de cumpleaños establecido en {channel.mention}")

@tasks.loop(hours=1)
async def check_birthdays():
    today = datetime.today().strftime("%m-%d")
    if today in sent_birthdays:
        return 
    
    sent_birthdays[today] = []
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM birthdays WHERE birthday = ?", (today,))
        users = cursor.fetchall()
        cursor.execute("SELECT guild_id, channel_id FROM birthday_channels")
        channels = cursor.fetchall()
    for guild_id, channel_id in channels:
        channel = bot.get_channel(channel_id)
        if not channel:
            continue
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT message, image_url FROM birthday_messages WHERE guild_id = ?", (guild_id,))
            result = cursor.fetchone()
        message = result[0] if result else "🎉 ¡Feliz cumpleaños {mention}! 🎂🎁"
        image_url = result[1] if result else ""
        for (user_id,) in users:
            if user_id in sent_birthdays[today]:
                continue
            user = await bot.fetch_user(user_id)
            final_message = message.replace("{mention}", user.mention)
            embed = discord.Embed(description=final_message, color=discord.Color.gold())
            if image_url:
                embed.set_image(url=image_url)
            await channel.send(embed=embed)
            sent_birthdays[today].append(user_id)
    save_sent_birthdays(sent_birthdays)

@bot.command(name="help_commands")
async def help_commands(ctx):
    embed = discord.Embed(title="📜 Lista de comandos", description="Aquí están todos los comandos disponibles:", color=discord.Color.blue())
    embed.add_field(name="!add_birthday @usuario MM-DD", value="Agrega un cumpleaños (admin).", inline=False)
    embed.add_field(name="!birthdays", value="Muestra la lista de cumpleaños registrados.", inline=False)
    embed.add_field(name="!remove_birthday @usuario", value="Elimina un cumpleaños registrado (admin).", inline=False)
    embed.add_field(name="!set_birthday_channel #canal", value="Establece el canal donde se enviarán los cumpleaños (admin).", inline=False)
    embed.add_field(name="!help_commands", value="Muestra esta lista de comandos.", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user}")
    if not check_birthdays.is_running():
        check_birthdays.start()

bot.run(TOKEN)
