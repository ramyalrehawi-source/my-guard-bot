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

# زر الاشتراك الغصب / الإجباري
def force_sub_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 اشترك غصباً في تحديثات أراس", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="⚡️ تحقق من الاشتراك الان", callback_data="check_sub")]
    ])

# أزرار الترحيب الشفافة
def welcome_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="! Aras 🕷️", url="https://t.me/i80_ibot")],
        [InlineKeyboardButton(text="📢 تحديثات أراس", url=CHANNEL_LINK)]
    ])

# كيبورد الأزرار السفلي (سورس يجوي)
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

# دالة الفحص الصارم للاشتراك
async def check_subscription(user_id: int) -> bool:
    if user_id == ADMIN_ID:
        return True  # المطور يتجاوز الفحص تلقائياً
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception:
        return True  # في حال عدم رفع البوت مشرف في القناة يتجاوز الفحص مؤقتاً

# ردود الأزرار السفلية
BUTTON_RESPONSES = {
    "[ معلومات التنصيب ]": "ℹ️ **معلومات التنصيب:**\nالبوت يعمل بنجاح على سيرفر Render وتحديثات سورس يجوي مفعلة 100%.",
    "[ قسم الاذاعه ]": "📢 **قسم الإذاعة:**\nيمكنك إرسال التوجيهات أو الرسائل لجميع المجموعات والأعضاء هنا.",
    "[ قسم التفعيلات ]": "⚙️ **قسم التفعيلات:**\nتم تفعيل: حماية الروابط ✅ | الردود التلقائية ✅ | الألعاب الترفيهية ✅ | بطاقة الايدي ✅ | الترحيب ✅",
    "[ قسم الاشتراك الاجباري ]": f"📢 **قسم الاشتراك الغصب:**\nقناة الاشتراك الإجباري الحالية: [تحديثات أراس]({CHANNEL_LINK})",
    "[ قسم القوائم ]": "📋 **قسم القوائم:**\nقائمة المحظورين، قائمة المشرفين، وقوائم المكتومين جاهزة.",
    "[ قسم النسخ ]": "💾 **قسم النسخ الاحتياطي:**\nيمكنك أخذ نسخة احتياطية إلكترونية لإعدادات البوت والجروبات.",
    "[ قسم المتنوع والمسح ]": "🧹 **قسم المسح والمتنوعات:**\nلتمسح الرسائل المحظورة أو تنظيف المحادثة.",
    "[ ترويج البوت ]": "🚀 **قسم ترويج البوت:**\nشارِك البوت في مجموعاتك لتفعيله وزيادة حمايتها.",
    "[ اعلان البوت ]": "📣 **قسم إعلانات البوت:**\nيمكنك نشر إعلاناتك عبر شبكة البوت.",
    "📞 التواصل مع المطور": "📬 **قسم التواصل:**\nاكتب رسالتك الآن وسوف يتم إرسالها إلى المطور مباشرة 📥",
    "[ حول ]": "🤖 **سورس أراس (Aras) المطور**\nللحماية والتفاعل وإدارة المجموعات والألعاب."
}

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

# أمر البدء مع الفحص الغصب
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
        f"🕷️ **أهلاً بك في بوت أراس الذكي**\n"
        f"🕷️ **قناة التحديثات الرسمية:** [تحديثات أراس]({CHANNEL_LINK})\n"
        f"🕷️ **إليك كيبورد الأوامر والسورس كامل:**"
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
            f"° : اسمك 🦂 ⦗ {new_member.first_name} ⦘\n"
            f"° : ايديك 🦂 ⦗ `{new_member.id}` ⦘\n"
            f"° : يوزرك 🦂 ⦗ {username
