import re
import os
from telegram import ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")  # التوكن من BotFather

# Regex لاكتشاف أرقام الهواتف (مثل +966555555555 أو 0555555555)
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
            # كتم المستخدم (لا يستطيع إرسال أي شيء)
            await context.bot.restrict_chat_member(
                chat_id=chat.id,
                user_id=user.id,
                permissions=ChatPermissions(can_send_messages=False)
            )

            # حذف الرسالة
            await message.delete()

            # إرسال تحذير للمجموعة
            await context.bot.send_message(
                chat.id,
                f"🚫 المستخدم {user.mention_html()} تم كتمه لإرساله رقم جوال!",
                parse_mode="HTML"
            )
        except Exception as e:
            print("حدث خطأ:", e)

# إنشاء التطبيق
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), check_message))

print("✅ البوت يعمل الآن...")
app.run_polling()
