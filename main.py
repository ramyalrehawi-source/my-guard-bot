import asyncio
import re
import random
from datetime import datetime
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
CHANNEL_USERNAME = "@i80_ii"  # معرف قناتك
CHANNEL_LINK = "https://t.me/+Nf1ReXca_D45ODg0"  # رابط القناة

bot = Bot(token=TOKEN)
dp = Dispatcher()

# زر الاشتراك الإجباري
def force_sub_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 اشترك غصباً في تحديثات أراس", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="⚡️ تحقق من الاشتراك الآن", callback_data="check_sub")]
    ])

# أزرار الترحيب الشفافة
def welcome_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="! Aras 🕷️", url="https://t.me/i80_ibot")],
        [InlineKeyboardButton(text="📢 تحديثات أراس", url=CHANNEL_LINK)]
    ])

# كيبورد الأزرار السفلي الاحترافي (نفس سورس يجوي تماماً)
def main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="[ معلومات التنصيب ]"), KeyboardButton(text="[ الكروبات ]")],
            [KeyboardButton(text="[ قسم الاذاعه ]"), KeyboardButton(text="[ قسم التفعيلات ]")],
            [KeyboardButton(text="[ قسم الاشتراك الاجباري ]"), KeyboardButton(text="[ قسم القوائم ]")],
            [KeyboardButton(text="[ قسم النسخ ]"), KeyboardButton(text="[ قسم المتنوع والمسح ]")],
            [KeyboardButton(text="[ ترويج البوت ]"), KeyboardButton(text="[ اعلان البوت ]")],
            [KeyboardButton(text="[ السيرفر ]"), KeyboardButton(text="[ تحديث ]")],
            [KeyboardButton(text="[ نقل ملكيه البوت ]"), KeyboardButton(text="[ تغيير رمز السورس ]")],
            [KeyboardButton(text="📞 التواصل مع المطور"), KeyboardButton(text="[ حول ]")]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard

# دالة الفحص الآمنة للاشتراك
async def check_subscription(user_id: int) -> bool:
    if user_id == ADMIN_ID:
        return True
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception:
        return True

AUTO_RESPONSES = {
    "اراس": ["عيوني 🤍", "موجود يا قلبي، آمرني؟ 😊", "سمعني، وش بغيت يا غالي؟ ✨", "روحه وعيونه لأراس 🖤"],
    "صباح الخير": ["صباح النور والسرور ✨🌸", "صباحك يسعد روحك يا رب 🤍"],
    "مساء الخير": ["مساء الورد والياسمين 🌺", "مساءك روقان وراحة بال 🖤"],
    "منور": ["نورك ونور الموجودين يا عسل 🌟", "عكس نورك يا غالي ✨"],
    "احبك": ["وأراس يحبك ويحب روحك الحلوة 🖤✨"]
}

GAMES_DATA = {
    "لو_خيروك": ["🤔 لو خيروك بين: العيش بدون إنترنت لمدة أسبوع VS العيش بدون هاتف نهائياً؟"],
    "صراحة": ["🎯 صراحة: ايش أكتر موقف محرج صار بحياتك ولا يمكن تنساه؟"],
    "تحدي": ["🔥 تحدي: أرسل آخر صورة حافظها بالمعرض بدون خجل!"],
    "ألغاز": ["💡 لغز ذكاء: شيء يبتلعك إذا ما انتبهت له، وكل ما أخذت منه يكبر ولا ينقص فما هو؟ (الحفرة)"]
}

# أمر البدء الرئيسي
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    is_subbed = await check_subscription(message.from_user.id)
    if not is_subbed:
        await message.answer(
            f"⛔️ **عذراً يا {message.from_user.first_name}!**\n\n"
            f"الاشتراك **غصباً وليس اختيارياً** لاستخدام بوت **أراس**! 🕷️⚡️\n"
            f"اشترك في القناة أولاً ثم اضغط على زر التحقق بالأسفل لتفعيل البوت:",
            reply_markup=force_sub_keyboard(),
            parse_mode="Markdown"
        )
        return

    welcome = (
        f"🕷️ **! Aras**\n"
        f"/start\n\n"
        f"🕷️ **أهلاً بك عزيزي المطور الاساسي**\n"
        f"🕷️ **اليك كيبورد اوامر سورس يجوي والحماية والألعاب الكثيرة** 🎮✨"
    )
    await message.answer(welcome, reply_markup=main_reply_keyboard(), parse_mode="Markdown")

# زر التحقق من الاشتراك
@dp.callback_query(F.data == "check_sub")
async def check_sub_callback(call: types.CallbackQuery):
    is_subbed = await check_subscription(call.from_user.id)
    if is_subbed:
        await call.message.delete()
        welcome = (
            f"✅ **تم التحقق بنجاح! أهلاً بك في أراس.**\n\n"
            f"🕷️ **قناة التحديثات الرسمية:** [تحديثات أراس]({CHANNEL_LINK})"
        )
        await call.message.answer(welcome, reply_markup=main_reply_keyboard(), parse_mode="Markdown")
    else:
        await call.answer("❌ ما زلت غير مشترك! اشترك غصباً بالقناة أولاً ثم تحقق مرة أخرى ⚡️", show_alert=True)

# ----------------- معالجات الأزرار السفلية الاحترافية -----------------
@dp.message(F.text == "[ معلومات التنصيب ]")
async def btn_info(message: types.Message):
    await message.answer("ℹ️ **معلومات التنصيب:**\nالبوت يعمل بنجاح على سيرفر Render وتحديثات سورس يجوي مفعلة 100%.", parse_mode="Markdown")

@dp.message(F.text == "[ الكروبات ]")
async def btn_groups(message: types.Message):
    await message.answer("👥 **قسم الكروبات والمجموعات المفعلة:**\n• عدد المجموعات المحمية: 1 مجموعة حالياً.", parse_mode="Markdown")

@dp.message(F.text == "[ قسم الاذاعه ]")
async def btn_broadcast(message: types.Message):
    await message.answer("📢 **قسم الإذاعة:**\n• إذاعة عامة\n• إذاعة خاص\n• إذاعة بالتوجيه\nاختر نوع الإذاعة وقم بإرسال رسالتك.", parse_mode="Markdown")

@dp.message(F.text == "[ قسم التفعيلات ]")
async def btn_activations(message: types.Message):
    await message.answer("⚙️ **قسم التفعيلات:**\n• حماية الروابط ✅\n• الترحيب التلقائي ✅\n• الردود التلقائية ✅\n• بطاقة الايدي ✅", parse_mode="Markdown")

@dp.message(F.text == "[ قسم الاشتراك الاجباري ]")
async def btn_force_sub(message: types.Message):
    await message.answer(f"📢 **أوامر الاشتراك الاجباري:**\n• تفعيل / تعطيل الاشتراك\n• القناة الحالية: [تحديثات أراس]({CHANNEL_LINK})", parse_mode="Markdown")

@dp.message(F.text == "[ قسم القوائم ]")
async def btn_lists(message: types.Message):
    await message.answer("📋 **قسم القوائم العامة:**\n• قائمة المطورين\n• قائمة المحظورين\n• قائمة المكتومين", parse_mode="Markdown")

@dp.message(F.text == "[ قسم النسخ ]")
async def btn_backup(message: types.Message):
    await message.answer("💾 **قسم النسخ الاحتياطي:**\n• جلب النسخة الاحتياطية\n• جلب روابط المجموعات", parse_mode="Markdown")

@dp.message(F.text == "[ قسم المتنوع والمسح ]")
async def btn_misc(message: types.Message):
    await message.answer("🧹 **قسم المتنوع والمسح:**\n• تنظيف المشتركين\n• مسح الردود العامة\n• مسح تخزين البوت", parse_mode="Markdown")

@dp.message(F.text == "[ ترويج البوت ]")
async def btn_promote(message: types.Message):
    await message.answer("🚀 **قسم ترويج البوت:**\nأضف أراس لجروبك وزد من حمايته وتفاعله مجاناً.", parse_mode="Markdown")

@dp.message(F.text == "[ اعلان البوت ]")
async def btn_ads(message: types.Message):
    await message.answer("📣 **قسم إعلانات البوت:**\nللنشر والتسويق عبر شبكة بوتات أراس.", parse_mode="Markdown")

@dp.message(F.text == "[ السيرفر ]")
async def btn_server(message: types.Message):
    await message.answer("🖥️ **معلومات السيرفر:**\n• السيرفر: Render Cloud\n• الحالة: يعمل بكفاءة عالية 🟢\n• الاستهلاك: مستقر", parse_mode="Markdown")

@dp.message(F.text == "[ تحديث ]")
async def btn_update(message: types.Message):
    await message.answer("🔄 **تم تحديث الملفات بنجاح 🕷️**", parse_mode="Markdown")

@dp.message(F.text == "[ نقل ملكيه البوت ]")
async def btn_transfer(message: types.Message):
    await message.answer("👑 **نقل ملكية البوت:**\n• ارسل معرف المطور الجديد (يوزر آيدي) لتسليمه الصلاحيات.", parse_mode="Markdown")

@dp.message(F.text == "[ تغيير رمز السورس ]")
async def btn_change_token(message: types.Message):
    await message.answer("🔑 **تغيير رمز السورس:**\nأرسل الرمز الجديد المعتمد لتحديث البوت.", parse_mode="Markdown")

@dp.message(F.text == "📞 التواصل مع المطور")
async def btn_contact(message: types.Message):
    await message.answer("📬 **قسم التواصل:**\nاكتب رسالتك الآن وسوف يتم إرسالها إلى المطور مباشرة 📥", parse_mode="Markdown")

@dp.message(F.text == "[ حول ]")
async def btn_about(message: types.Message):
    await message.answer("🤖 **سورس أراس (Aras) المطور**\nللحماية والتفاعل وإدارة المجموعات والألعاب.", parse_mode="Markdown")
# -------------------------------------------------------------------------

# أمر الايدي
@dp.message(F.text.in_(["ا", "ايدي", "ايديك"]))
async def user_id_info(message: types.Message):
    user = message.from_user
    chat = message.chat

    if user.id == ADMIN_ID:
        rank = "المطور الاساسي"
    elif chat.type in ["group", "supergroup"]:
        try:
            member = await chat.get_member(user.id)
            rank = "مالك المجموعه" if member.status == "creator" else ("مشرف" if member.status == "administrator" else "عضو")
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

# الترحيب بالجروبات
@dp.message(F.new_chat_members)
async def welcome_new_member(message: types.Message):
    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    time_str = now.strftime("%I:%M%p")

    for new_member in message.new_chat_members:
        if new_member.is_bot:
            continue

        username = f"@{new_member.username}" if new_member.username else "لا يوجد"
        welcome_text = (
            f"═'𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 . 𝐆𝐑𝐎𝐔𝐏 ═\n"
            f"°•--------------•°\n"
            f"° : نورت جروبنا يا ⦗ {new_member.first_name} ⦘🥂✨.\n"
            f"° : اسمك ↩️ ⦗ {new_member.first_name} ⦘\n"
            f"° : ايديك ↩️ ⦗ `{new_member.id}` ⦘\n"
            f"° : يوزرك ↩️ ⦗ {username} ⦘\n\n"
            f"❞ ° : تاريخ انضمامك 📷 {date_str}\n"
            f"❞ ° : الساعة 📷 {time_str}.\n"
            f"°•--------------•°"
        )
        try:
            user_photos = await bot.get_user_profile_photos(new_member.id, limit=1)
            if user_photos.total_count > 0:
                await message.reply_photo(photo=user_photos.photos[0][-1].file_id, caption=welcome_text, reply_markup=welcome_keyboard(), parse_mode="Markdown")
            else:
                await message.reply(text=welcome_text, reply_markup=welcome_keyboard(), parse_mode="Markdown")
        except Exception:
            await message.reply(text=welcome_text, reply_markup=welcome_keyboard(), parse_mode="Markdown")

# المعالجة العامة للرسائل والردود والروابط
@dp.message(F.text)
async def handle_all_messages(message: types.Message):
    text = message.text.strip()

    if message.chat.type == "private":
        is_subbed = await check_subscription(message.from_user.id)
        if not is_subbed:
            await message.answer(
                f"⛔️ **عذراً! الاشتراك غصباً في [قناة تحديثات أراس]({CHANNEL_LINK}) لتفعيل البوت!**",
                reply_markup=force_sub_keyboard(),
                parse_mode="Markdown"
            )
            return

    if message.chat.type in ["group", "supergroup"]:
        member = await message.chat.get_member(message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            if re.search(r"(https?://[^\s]+|t\.me/[^\s]+)", text):
                try:
                    await message.delete()
                    warn = await message.answer(f"⚠️ يمنع إرسال الروابط يا {message.from_user.first_name}!")
                    await asyncio.sleep(4)
                    await warn.delete()
                    return
                except Exception:
                    pass

    for key, replies in AUTO_RESPONSES.items():
        if key in text.lower():
            await message.reply(random.choice(replies))
            break

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
