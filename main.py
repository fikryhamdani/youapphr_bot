from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

LOWONGAN = {
    "1": {"posisi": "Backend Developer", "link_tes": "https://forms.gle/tes1", "link_form": "https://forms.gle/form1"},
    "2": {"posisi": "UI/UX Designer", "link_tes": "https://forms.gle/tes2", "link_form": "https://forms.gle/form2"},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(job["posisi"], callback_data=key)] for key, job in LOWONGAN.items()]
    await update.message.reply_text("Pilih lowongan:", reply_markup=InlineKeyboardMarkup(keyboard))

async def pilih_posisi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pilihan = query.data
    context.user_data["posisi"] = pilihan
    job = LOWONGAN[pilihan]
    await query.edit_message_text(
        f"Lowongan: *{job['posisi']}*\n\nTes: {job['link_tes']}\n\nSetelah selesai, ketik `Selesai`.",
        parse_mode="Markdown"
    )

async def selesai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    posisi = context.user_data.get("posisi")
    if posisi:
        await update.message.reply_text(f"Terima kasih! Isi form ini: {LOWONGAN[posisi]['link_form']}")
    else:
        await update.message.reply_text("Silakan ketik /start dulu.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(pilih_posisi))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("(?i)selesai"), selesai))

if __name__ == "__main__":
    app.run_polling()