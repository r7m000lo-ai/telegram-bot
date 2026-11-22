import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

BOT_TOKEN = "9299056956:AAGp2fezoHpZ7IaEARLVCUrOw83enaOMboM"
OWNER_ID = 9299056956

SELECT_LANGUAGE, MAIN_MENU, SELECT_CATEGORY, WAITING_MEDIA = range(4)

user_lang = {}
user_category = {}
user_media_type = {}

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def get_lang_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("🇸🇦 عربي"), KeyboardButton("🇺🇸 English")]],
        resize_keyboard=True
    )

def get_main_keyboard(lang):
    if lang == "ar":
        keyboard = [
            [KeyboardButton("📷 إرسال صورة"), KeyboardButton("🎬 إرسال مقطع")],
            [KeyboardButton("✉️ إرسال رسالة"), KeyboardButton("🔄 تغيير اللغة")]
        ]
    else:
        keyboard = [
            [KeyboardButton("📷 Send Photo"), KeyboardButton("🎬 Send Video")],
            [KeyboardButton("✉️ Send Message"), KeyboardButton("🔄 Change Language")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_category_keyboard(lang):
    if lang == "ar":
        keyboard = [
            [KeyboardButton("مشاهير عرب"), KeyboardButton("مشاهير أجانب")],
            [KeyboardButton("فرك"), KeyboardButton("لزلز")],
            [KeyboardButton("سكس"), KeyboardButton("تجليخ")],
            [KeyboardButton("أخرى"), KeyboardButton("🔙 رجوع")]
        ]
    else:
        keyboard = [
            [KeyboardButton("Arab Celebs"), KeyboardButton("Foreign Celebs")],
            [KeyboardButton("Fark"), KeyboardButton("Lazlaz")],
            [KeyboardButton("Sex"), KeyboardButton("Tajleekh")],
            [KeyboardButton("Other"), KeyboardButton("🔙 Back")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً 👋\nاختر اللغة / Choose language:",
        reply_markup=get_lang_keyboard()
    )
    return SELECT_LANGUAGE

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if "عربي" in text or "🇸🇦" in text:
        user_lang[user_id] = "ar"
        await update.message.reply_text(
            "تم اختيار العربية ✅\nاختر ما تريد إرساله:",
            reply_markup=get_main_keyboard("ar")
        )
    else:
        user_lang[user_id] = "en"
        await update.message.reply_text(
            "English selected ✅\nChoose what you want to send:",
            reply_markup=get_main_keyboard("en")
        )
    return MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "ar")

    if "تغيير اللغة" in text or "Change Language" in text:
        await update.message.reply_text(
            "اختر اللغة / Choose language:",
            reply_markup=get_lang_keyboard()
        )
        return SELECT_LANGUAGE

    if "صورة" in text or "Photo" in text:
        user_media_type[user_id] = "photo"
        msg = "اختر الفئة:" if lang == "ar" else "Choose category:"
        await update.message.reply_text(msg, reply_markup=get_category_keyboard(lang))
        return SELECT_CATEGORY

    if "مقطع" in text or "Video" in text:
        user_media_type[user_id] = "video"
        msg = "اختر الفئة:" if lang == "ar" else "Choose category:"
        await update.message.reply_text(msg, reply_markup=get_category_keyboard(lang))
        return SELECT_CATEGORY

    if "رسالة" in text or "Message" in text:
        msg = "اكتب رسالتك الآن ✉️" if lang == "ar" else "Write your message now ✉️"
        await update.message.reply_text(msg)
        return WAITING_MEDIA

    return MAIN_MENU

async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id
