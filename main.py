import os
import logging
import csv
import requests
from io import StringIO

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Inisialisasi logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Bot Token dari environment
TOKEN = os.getenv("BOT_TOKEN")

# URL CSV Google Sheet
CSV_URL = "https://docs.google.com/spreadsheets/d/1CgpbTCg_0D8uXe8sKZEBBzfjRJmH2XOGX2cafTj5L7Q/gviz/tq?tqx=out:csv"

# Perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Welcome to YouApp HR Bot.\nUse /jobs to see our current job openings.")

# Perintah /jobs untuk ambil data dari Google Sheets
async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()

        f = StringIO(response.text)
        reader = csv.DictReader(f)

        keyboard = []
        text = "📋 *Available Job Openings:*\n\n"
        count = 0

        for row in reader:
            if row.get("Active", "0").strip() != "1":
                continue  # skip job yang tidak aktif

            job_id = row.get("ID", "").strip()
            title = row.get("Job Title", "No Title").strip()
            dept = row.get("Department", "General").strip()

            # Kamu bisa arahkan ke Google Form yang pakai ID lowongan sebagai param
            form_url = f"https://your-form-link.com?job_id={job_id}"

            text += f"• *{title}* — _{dept}_\n"
            keyboard.append([InlineKeyboardButton(f"{title}", url=form_url)])
            count += 1

        if count == 0:
            await update.message.reply_text("😕 No active job openings at the moment.")
            return

        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except Exception as e:
        logging.error(f"Failed to fetch jobs: {e}")
        await update.message.reply_text("❌ Failed to load jobs. Please try again later.")

# Main function
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", jobs))

    app.run_polling()
