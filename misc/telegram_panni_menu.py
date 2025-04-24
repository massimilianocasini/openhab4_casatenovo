import json
import datetime
import pandas as pd
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configurazione del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,  # Aumentato il livello di logging a DEBUG
    filename='bot.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

# Tabella alimentare quindicinale (inizialmente vuota)
meal_plan = {}

def get_meal(day: str, period: str) -> str:
    """Restituisce il pasto in base al giorno e alla fascia oraria."""
    day = day.capitalize()
    period = period.capitalize()
    logger.debug(f"Richiesta pasto: giorno={day}, fascia={period}")
    try:
        meal = meal_plan[day][period]
        return f"{day} ({period}): {meal}"
    except KeyError:
        return "Dati non disponibili. Assicurati di inserire il giorno e la fascia oraria correttamente."

async def meal_command(update: Update, context: CallbackContext) -> None:
    """Gestisce il comando /meal."""
    if len(context.args) < 2:
        await update.message.reply_text("Usa il formato: /meal <giorno> <fascia> (es: /meal lunedì pranzo)")
        return
    
    day, period = context.args[0], context.args[1]
    response = get_meal(day, period)
    await update.message.reply_text(response)

async def show_meal_plan(update: Update, context: CallbackContext) -> None:
    """Mostra i dati caricati dal file Excel."""
    meal_plan_str = json.dumps(meal_plan, indent=4, ensure_ascii=False)
    logger.debug(f"Dati attuali della tabella alimentare: {meal_plan_str}")
    await update.message.reply_text(f"Dati caricati:\n```{meal_plan_str}```", parse_mode='Markdown')

def parse_excel(file_path):
    """Estrae e converte la tabella alimentare dall'Excel in un dizionario."""
    global meal_plan
    meal_plan = {}
    try:
        df = pd.read_excel(file_path)
        df.fillna("", inplace=True)
        
        for _, row in df.iterrows():
            day = row.iloc[0].capitalize()
            meal_plan[day] = {
                "Colazione": row.iloc[1],
                "Metà Mattina": row.iloc[2],
                "Pranzo": row.iloc[3],
                "Merenda": row.iloc[4],
                "Cena": row.iloc[5]
            }
        
        logger.debug(f"Tabella alimentare aggiornata: {json.dumps(meal_plan, indent=4, ensure_ascii=False)}")
    except Exception as e:
        logger.error(f"Errore nel parsing del file Excel: {e}")
        return str(e)
    return "Tabella alimentare aggiornata con successo!"

async def upload_excel(update: Update, context: CallbackContext) -> None:
    """Gestisce l'upload del file Excel e aggiorna la tabella alimentare."""
    try:
        file = await update.message.document.get_file()
        file_path = "meal_plan.xlsx"
        await file.download_to_drive(file_path)
        logger.info("File Excel ricevuto e salvato.")
        response = parse_excel(file_path)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Errore durante l'upload del file Excel: {e}")
        await update.message.reply_text("Si è verificato un errore durante l'elaborazione del file Excel.")

async def help_command(update: Update, context: CallbackContext) -> None:
    """Mostra i comandi disponibili."""
    help_text = """Comandi disponibili:
    /meal <giorno> <fascia> - Ottieni il pasto per un determinato giorno e fascia oraria.
    /show_meal_plan - Mostra i dati della tabella alimentare caricata.
    Invia un file Excel con la tabella alimentare per aggiornarla.
    /help - Mostra questo messaggio di aiuto.
    """
    await update.message.reply_text(help_text)

def main():
    """Avvia il bot."""
    TOKEN = "8191598189:AAGPioYjHPYeC91m2JGoS0o1QuFurJoFpB4"
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("meal", meal_command))
    app.add_handler(CommandHandler("show_meal_plan", show_meal_plan))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.Document.MimeType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"), upload_excel))
    
    logger.info("Bot avviato...")
    app.run_polling()

if __name__ == "__main__":
    main()
