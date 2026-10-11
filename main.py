import asyncio
import re
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

TOKEN = "8963723966:AAE7qIh7ci0w4tROnYdvP-6KoOzWMn74AEo"
ADMIN_ID = 8921676913  # ID المطور الأساسي
CHANNEL_USERNAME = "@i80_ii"  # معرف قناتك للاشتراك الإجباري
CHANNEL_LINK = "https://t.me/+Nf1ReXca_D45ODg0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# زر الاشتراك الإجباري
def sub_channel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="[ قناة البوت ]", url=CHANNEL_LINK)]
    ])

# كيبورد الأزرار السفلي
def main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="[ معلومات التنصيب ]")],
            [KeyboardButton(text="[ قسم الاذاعه ]"), KeyboardButton(text="[ قسم التفعيلات ]")],
            [KeyboardButton(text="[ قسم الاشتراك الاجباري ]")],
            [KeyboardButton(text="[ قسم القوائم ]"), KeyboardButton(text="[ قسم النسخ ]")],
            [KeyboardButton(text="[ قسم المتنوع والمسح ]")],
            [KeyboardButton(text="[ ترويج البوت ]"), KeyboardButton(text="[ اعلان البوت ]")],
            [KeyboardButton(text="📞 التواصل مع المطور")],
            [KeyboardButton(text="[ حول ]")]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard

# التحقق من الاشتراك الإجباري بالقناة
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception:
        return True  # في حال عدم رفع البوت مشرف بالقناة يتجاوز الفحص

# ردود تفاعلية
AUTO_RESPONSES = {
    "اراس": ["عيوني 🤍", "موجود يا قلبي، آمرني؟ 😊", "سمعني، وش بغيت يا غالي؟ ✨", "روحه وعيونه لأراس 🖤"],
    "صباح الخير": ["صباح النور والسرور ✨🌸", "صباحك يسعد روحك يا رب 🤍"],
    "مساء الخير": ["مساء الورد والياسمين 🌺", "مساءك روقان وراحة بال 🖤"],
    "منور": ["نورك ونور الموجودين يا عسل 🌟", "عكس نورك يا غالي ✨"],
    "احبك": ["وأراس يحبك ويحب روحك الحلوة 🖤✨"]
}

# بنك الألعاب
GAMES_DATA = {
    "لو_خيروك": [
        "🤔 لو خيروك بين: العيش بدون إنترنت لمدة أسبوع VS العيش بدون هاتف نهائياً؟",
        "🤔 لو خيروك بين: السفر لأي مكان بالماضي VS السفر للمستقبل؟"
    ],
    "صراحة": [
        "🎯 صراحة: ايش أكتر موقف محرج صار بحياتك ولا يمكن تنساه؟",
        "🎯 صراحة: مين الشخص الي مستحيل تنسى فضل عليّك؟"
    ],
    "تحدي": [
        "🔥 تحدي: أرسل آخر صورة حافظها بالمعرض بدون خجل!",
        "🔥 تحدي: اكتب اسمك المفضل وانت مغمض عيونك."
    ],
    "ألغاز": [
        "💡 لغز ذكاء: شيء يبتلعك إذا ما انتبهت له، وكل ما أخذت منه يكبر ولا ينقص فما هو؟ (الحفرة)"
    ]
}

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    welcome = (
        f"🕷️ **! Aras**\n"
        f"/start\n\n"
        f"🕷️ **اهلا بك عزيزي المطور الاساسي**\n"
        f"🕷️ **اليك كيبورد اوامر سورس يجوي**"
    )
    await message.answer(welcome, reply_markup=main_reply_keyboard(), parse_mode="Markdown")

# أمر "ايدي"
@dp.message(F.text.in_(["ا", "ايدي", "ايديك"]))
async def user_id_info(message: types.Message):
    user = message.from_user
    chat = message.chat

    if user.id == ADMIN_ID:
        rank = "المطور الاساسي"
    elif chat.type in ["group", "supergroup"]:
        try:
            member = await chat.get_member(user.id)
            if member.status == "creator":
                rank = "مالك المجموعه"
            elif member.status == "administrator":
                rank = "مشرف المجموعه"
            else:
                rank = "عضو"
        except Exception:
            rank = "عضو"
    else:
        rank = "عضو"

    username = f"@{user.username}" if user.username else "لا يوجد"
    info_text = (
        f"▪️ : مو صوره ضيم\n"
        f"▪️ : ايديك ↩️ [ `{user.id}` ]\n"
        f"▪️ : معرفك ↩️ [ {username} ]\n"
        f"▪️ : رتبتك ↩️ [ {rank} ]\n"
        f"▪️ : تفاعلك ↩️ [ ممتاز جداً ]"
    )

    user_photos = await bot.get_user_profile_photos(user.id, limit=1)
    if user_photos.total_count > 0:
        await message.reply_photo(photo=user_photos.photos[0][-1].file_id, caption=info_text, parse_mode="Markdown")
    else:
        await message.reply(info_text, parse_mode="Markdown")

# أوامر الإدارة (طرد / حظر) مع التحقق من الصلاحيات والاشتراك
@dp.message(F.text.in_(["طرد", "كتم", "حظر"]))
async def admin_actions(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    # 1. التحقق من الاشتراك الإجباري
    is_subbed = await check_subscription(message.from_user.id)
    if not is_subbed:
        await message.reply("مـ : اشترك بقناة البوت لتتمكن من استخدامه ⚡️.", reply_markup=sub_channel_keyboard())
        return

    # 2. التحقق من صلاحية المستخدم (هل هو ادمن أو المطور؟)
    member = await message.chat.get_member(message.from_user.id)
    if member.status not in ["administrator", "creator"] and message.from_user.id != ADMIN_ID:
        await message.reply("• عذراً الأمر يخص ↩️ 〖 الادمن 〗 فقط .")
        return

    # 3. التأكد من الرد على شخص
    if not message.reply_to_message:
        await message.reply("⚠️ يجب عليك الرد على رسالة العضو المراد طرده/حظره!")
        return

    target_user = message.reply_to_message.from_user
    
    # تنفيـذ الطرد
    try:
        if message.text == "طرد":
            await message.chat.ban(user_id=target_user.id)
            await message.chat.unban(user_id=target_user.id)
            await message.reply(f"✅ تم طرد العضو [{target_user.first_name}](tg://user?id={target_user.id}) بنجاح.", parse_mode="Markdown")
        elif message.text == "حظر":
            await message.chat.ban(user_id=target_user.id)
            await message.reply(f"🚫 تم حظر العضو [{target_user.first_name}](tg://user?id={target_user.id}) بنجاح.", parse_mode="Markdown")
    except Exception:
        await message.reply("❌ تأكد من رفع البوت مشرفاً ومنحه صلاحية الحظر/الردود!")

# الألعاب
@dp.message(Command("لو_خيروك", "لوخيروك"))
async def game_lw_5yrwk(message: types.Message):
    await message.reply(random.choice(GAMES_DATA["لو_خيروك"]))

@dp.message(Command("صراحة"))
async def game_sra7a(message: types.Message):
    await message.reply(random.choice(GAMES_DATA["صراحة"]))

# معالجة الروابط والردود
@dp.message(F.text & ~F.text.startswith("/"))
async def handle_messages(message: types.Message):
    text = message.text.lower()

    if message.chat.type in ["group", "supergroup"]:
        member = await message.chat.get_member(message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            if re.search(r"(https?://[^\s]+|t\.me/[^\s]+)", message.text):
                try:
                    await message.delete()
                    warn = await message.answer(f"⚠️ يمنع إرسال الروابط يا {message.from_user.first_name}!")
                    await asyncio.sleep(4)
                    await warn.delete()
                    return
                except Exception:
                    pass

    for key, replies in AUTO_RESPONSES.items():
        if key in text:
            await message.reply(random.choice(replies))
            break

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
