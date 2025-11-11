import re
import os
from telegram import ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# التوكن من Environment Variable أو ضع التوكن مباشرة هنا
TOKEN = os.getenv("BOT_TOKEN")  # أو TOKEN = "123456:ABCdefGhIJKlmNOP..."

# Regex لاكتشاف أرقام الهواتف
PHONE_REGEX = re.compile(r"[+\d][\d\-\s\(\)]{5,}\d")

async def check_message(update, context):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    text = message.text or message.caption or ""

    # تجاهل رسائل البوت نفسه
    if user.is_bot:
        return

    if PHONE_REGEX.search(text):
        try:
            # كتم المستخدم
            await context.bot.restrict_chat_member(
                chat_id=chat.id,
                user_id=user.id,
                permissions=ChatPermissions(can_send_messages=False)
            )
            # حذف الرسالة
            await message.delete()
            # تحذير المجموعة
            await context.bot.send_message(
                chat.id,
                f"🚫 المستخدم {user.mention_html()} تم كتمه لإرساله رقم جوال!",
                parse_mode="HTML"
            )
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    # إنشاء البوت بدون Updater
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), check_message))
    print("✅ البوت يعمل الآن...")
    app.run_polling()
