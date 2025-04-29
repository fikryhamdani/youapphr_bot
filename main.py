import csv
import requests
from io import StringIO

# URL CSV publik dari Google Sheet
CSV_URL = "https://docs.google.com/spreadsheets/d/1CgpbTCg_0D8uXe8sKZEBBzfjRJmH2XOGX2cafTj5L7Q/gviz/tq?tqx=out:csv"

def jobs(update: Update, context: CallbackContext):
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()
        f = StringIO(response.text)
        reader = csv.DictReader(f)
        
        keyboard = []
        text = "📋 *Lowongan yang Tersedia:*\n\n"
        for row in reader:
            title = row.get("Job Title", "No Title")
            link = row.get("Apply Link", "#")
            desc = row.get("Description", "")
            text += f"• *{title}*\n  {desc}\n\n"
            keyboard.append([InlineKeyboardButton(title, url=link)])
        
        update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    except Exception as e:
        update.message.reply_text("Gagal mengambil data lowongan. Coba lagi nanti.")
        print("Error:", e)
