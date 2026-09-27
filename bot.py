import telebot

BOT_TOKEN = "1703492706:AAHsAqppfHebxqVhs6DS-m85IferOo7Yrno"

# قائمة الحسابات المسموح لها
ALLOWED_IDS = [5122597, 681133243]

# ID القناة
CHANNEL_ID = -1004328862298

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True, content_types=telebot.util.content_type_media)
def copy_and_post_to_channel(message):
    user_id = message.from_user.id

    # 1. فحص الصلاحية
    if user_id not in ALLOWED_IDS:
        return

    try:

        bot.copy_message(chat_id=CHANNEL_ID,from_chat_id=message.chat.id,message_id=message.message_id)

        bot.reply_to(message, "✅ تم نشر الرسالة في القناة باسم البوت مباشرة!")

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء النشر:\n`{e}`", parse_mode="Markdown")

bot.infinity_polling()
