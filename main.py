import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token and Admin User ID
BOT_TOKEN = "7673239490:AAHH3Hf9IPpWtGYfpjSdhqJplMhJepCbnR4"
ADMIN_ID = "1977956668"

# Authorized Users (Admin ID included here)
authorized_users = [ADMIN_ID]

# Function to fetch vehicle details
def fetch_vehicle_details(vehicle_number):
    url = f"https://www.acko.com/asset_service/api/assets/search/vehicle/{vehicle_number}?validate=false&source=rto"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Cookie": "trackerid=9033febc-7256-4b84-9efb-fc99c9dfdf60; user_id=j3hMTZKo1oCf4RctlFxdgw:1733332955688:cc4982d8ea5d040043af07feae033e693b8ff953;"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json():
        return response.json()
    else:
        return None

# Improved field names for readability and prioritization
prioritized_fields = [
    "asset_number",
    "owner_name",
    "registration_date",
    "make_model",
    "fuel_type",
    "vehicle_type",
    "registration_address",
    "permanent_address",
    "present_address",
    "previous_policy_expiry_date",
    "is_commercial"
]

field_mapping = {
    "asset_number": "Vehicle Number",
    "asset_type": "Vehicle Type",
    "registration_year": "Registration Year",
    "registration_month": "Registration Month",
    "make_model": "Make Model",
    "vehicle_type": "Vehicle Type",
    "make_name": "Make Name",
    "fuel_type": "Fuel Type",
    "owner_name": "Owner Name",
    "previous_insurer": "Previous Insurer",
    "previous_policy_expiry_date": "Previous Policy Expiry Date",
    "is_commercial": "Is Commercial",
    "vehicle_type_v2": "Vehicle Type V2",
    "vehicle_type_processed": "Vehicle Type Processed",
    "permanent_address": "Permanent Address",
    "present_address": "Present Address",
    "registration_date": "Registration Date",
    "registration_address": "Registration Address",
    "model_name": "Model Name",
    "make_name2": "Make Name (Detailed)",
    "model_name2": "Model Name (Detailed)",
    "variant_id": "Variant ID",
    "previous_policy_expired": "Previous Policy Expired"
}

# Function to format the vehicle details with prioritization and different emojis
def format_vehicle_details(data):
    # Unique emojis for each field
    field_emojis = {
        "asset_number": "📝",
        "owner_name": "🧑‍💼",
        "make_model": "🚘",
        "registration_year": "🗓️",
        "registration_date": "📅",
        "registration_address": "📍",
        "fuel_type": "⛽",
        "engine_number": "🔧",
        "chassis_number": "🪛",
        "is_commercial": "🏢",
        "previous_insurer": "📜",
        "previous_policy_expiry_date": "📆",
        "vehicle_type": "🚙",
        "permanent_address": "🏠",
        "present_address": "🏡",
        "vehicle_type_v2": "🛻",
        "vehicle_type_processed": "🛠️",
        "model_name": "📝",
        "make_name2": "🔧",
        "model_name2": "🚗",
        "variant_id": "🔢",
        "previous_policy_expired": "📅",
        "registration_month": "📅",
        "make_name": "🏭",
        "vehicle_type": "🚗",
    }

    message = "========================================\n"
    message += f"🚙 <b>Vehicle Details for {data.get('asset_number')}:</b>\n"
    message += "========================================\n"
    
    # First add prioritized fields
    for field in prioritized_fields:
        if field in data:
            emoji = field_emojis.get(field, "🔹")
            formatted_key = field_mapping.get(field, field.replace("_", " ").upper())
            formatted_value = data.get(field) or "N/A"
            message += f"{emoji} <b>{formatted_key}:</b> <code>{formatted_value}</code>\n"
    message += "\nAdditional Details:\n"
    message += "----------------------------------------\n"
    
    # Then add remaining fields
    for field, value in data.items():
        if field not in prioritized_fields:
            emoji = field_emojis.get(field, "🔹")
            formatted_key = field_mapping.get(field, field.replace("_", " ").upper())
            formatted_value = value or "N/A"
            message += f"{emoji} <b>{formatted_key}:</b> <code>{formatted_value}</code>\n"
    message += "\n========================================"
    message += "\n📌 𝗙𝗼𝗿 𝗠𝗼𝗿𝗲 𝗝𝗼𝗶𝗻 𝗨𝘀:"
    message += "https://t.me/httpdarkie404/"

    return message

# Function to handle /start command
async def start(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    logger.info(f"User ID: {user_id}")  # Debugging log

    if user_id in authorized_users:
        # Make sure only supported HTML tags are used
        welcome_message = """
        <b>𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗨𝘀𝗲𝗿!</b> 🎉
        <b>𝗧𝗵𝗶𝘀 𝗶𝘀 𓆩𝐃𝐀𝐑𝐊𝐈𝐄𓆪 𝗩𝗲𝗵𝗶𝗰𝗹𝗲 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝗟𝗼𝗼𝗸𝘂𝗽 𝗕𝗼𝘁.</b> 🛐
        
        ✅ <b>𝗛𝗼𝘄 𝘁𝗼 𝗨𝘀𝗲:</b>
        🚀 Use /search <i><b>VEHICLE NUMBER</b></i> to get vehicle details.
        💬 Need help? Use /help
	Contact the admin at @http_darkie.
        
        <b>𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗯𝘆 𓆩𝐃𝐀𝐑𝐊𝐈𝐄𓆪 ❤️</b>

	📌 𝗙𝗼𝗿 𝗠𝗼𝗿𝗲 𝗝𝗼𝗶𝗻 𝗨𝘀:https://t.me/httpdarkie404/
        """
        await update.message.reply_html(welcome_message)
    else:
        unauthorized_message = """
        🚫 <b>You are not authorized to use this bot.</b> 🚫

        <b>Please contact the admin for access:</b>
        👉 @http_darkie
        👉 @darkie404bot (If restricted)

	   𝗧𝗵𝗶𝘀 𝗕𝗼𝘁 𝗶𝘀 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗯𝘆  𓆩𝐃𝐀𝐑𝐊𝐈𝐄𓆪 🔥
	📌 𝗙𝗼𝗿 𝗠𝗼𝗿𝗲 𝗝𝗼𝗶𝗻 𝗨𝘀:https://t.me/httpdarkie404/
        """
        await update.message.reply_html(unauthorized_message)

# Function to handle /search command
async def search(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    username = update.message.from_user.username
    full_name = update.message.from_user.full_name
    logger.info(f"User {full_name} (ID: {user_id}, Username: @{username}) is searching for vehicle: {context.args[0]}")  # Debugging log
    
    if user_id not in authorized_users:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Please provide a vehicle number. Usage: /search <VEHICLE NUMBER>")
        return
    
    vehicle_number = context.args[0]
    await update.message.reply_text("🔄 Fetching vehicle details...")

    vehicle_data = fetch_vehicle_details(vehicle_number)
    
    if not vehicle_data:
        await update.message.reply_text("❌ Unable to fetch vehicle details. Please try again later.")
        return

    formatted_message = format_vehicle_details(vehicle_data)
    await update.message.reply_html(formatted_message)

    # Send the user details and vehicle search result to admin
    admin_chat_id = ADMIN_ID  # Replace with the actual admin's chat ID
    admin_message = f"""
    🔔 <b>𝗡𝗲𝘄 𝗩𝗲𝗵𝗶𝗰𝗹𝗲 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝗾𝘂𝗲𝘀𝘁</b> 🔔

    <b>User Information:</b>
    👤 <b>Name:</b> {full_name}
    🆔 <b>User ID:</b> {user_id}
    📱 <b>Username:</b> @{username}
    🚗 <b>Vehicle Number Searched:</b> {vehicle_number}

    <b>Vehicle Details:</b>
    {formatted_message}
    """
    await context.bot.send_message(chat_id=admin_chat_id, text=admin_message, parse_mode="HTML")

# Function to handle /add command to add authorized users
async def add(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to add users.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("⚠️ Please provide a user ID to add. Usage: /add <USER ID>")
        return

    new_user = context.args[0]
    if new_user in authorized_users:
        await update.message.reply_text(f"ℹ️ User {new_user} is already authorized.")
    else:
        authorized_users.append(new_user)
        await update.message.reply_text(f"✅ User {new_user} has been successfully authorized.")

# Function to handle /remove command to remove authorized users
async def remove(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to remove users.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("⚠️ Please provide a user ID to remove. Usage: /remove <USER ID>")
        return

    user_to_remove = context.args[0]
    if user_to_remove in authorized_users:
        authorized_users.remove(user_to_remove)
        await update.message.reply_text(f"✅ User {user_to_remove} has been successfully removed.")
    else:
        await update.message.reply_text(f"ℹ️ User {user_to_remove} is not authorized.")

# Function to handle /list command to list authorized users
async def list_users(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to view the user list.")
        return

    user_list = "\n".join(authorized_users)
    if user_list:
        await update.message.reply_text(f"Authorized Users:\n{user_list}")
    else:
        await update.message.reply_text("No authorized users.")

# Function to handle the /help command
async def help(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    help_message = """
    🚨 𝗡𝗲𝗲𝗱 𝗵𝗲𝗹𝗽? 𝗧𝗵𝗲 𝗳𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 𝗮𝗿𝗲 𝘁𝗵𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝘆𝗼𝘂 𝗰𝗮𝗻 𝘂𝘀𝗲:

    🔹 /start - Start the bot and get a welcome message.
    🔹 /search <code>vehicle_number</code> - Search for vehicle details by vehicle number (e.g. /search KA01AB1234).
    🔹 /help - Get this help message.
    
    📞 𝗡𝗲𝗲𝗱 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝗰𝗲? 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝘁𝗵𝗲 𝗮𝗱𝗺𝗶𝗻:
     	👤 @http_darkie
     	👤 @darkie404bot (If restricted)

    🔥 𝗧𝗵𝗶𝘀 𝗕𝗼𝘁 𝗶𝘀 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗯𝘆 𓆩𝐃𝐀𝐑𝐊𝐈𝐄𓆪 🔥
    📌 𝗙𝗼𝗿 𝗠𝗼𝗿𝗲 𝗝𝗼𝗶𝗻 𝗨𝘀:https://t.me/httpdarkie404/	
    """
    await context.bot.send_message(chat_id=chat_id, text=help_message, parse_mode="HTML")

# Function to send authorized users list to admin
async def send_authorized_users_to_admin(context: CallbackContext):
    admin_chat_id = ADMIN_ID
    if authorized_users:
        user_list = "\n".join(authorized_users)
        message = f"📜 <b>Daily Authorized Users List:</b>\n\n{user_list}"
    else:
        message = "ℹ️ No authorized users available."
    
    await context.bot.send_message(chat_id=admin_chat_id, text=message, parse_mode="HTML")

# Schedule the task to run daily
def schedule_daily_authorized_users(application: Application):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_authorized_users_to_admin, 
        trigger="interval", 
        days=1, 
        args=[application.bot]
    )
    scheduler.start()

# Main function to set up the bot
async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Adding command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("remove", remove))
    application.add_handler(CommandHandler("list", list_users))
    application.add_handler(CommandHandler("help", help))
    schedule_daily_authorized_users(application)	
    
    # Start the bot
    await application.run_polling()
# Run the bot
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()  # Apply the fix for already running event loop
    asyncio.run(main())  # Run the bot
