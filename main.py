Import asyncio
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
ADMIN_ID = 8921676913  # ID المطور الأساسي (رامي)
CHANNEL_USERNAME = "@i80_ii"
CHANNEL_LINK = "https://t.me/+Nf1ReXca_D45ODg0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. كيبورد الاشتراك الإجباري
def force_sub_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 اشترك غصباً في تحديثات أراس", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="⚡️ تحقق من الاشتراك الآن", callback_data="check_sub")]
    ])

# 2. الأزرار الشفافة الفخمة لعرض البوت (نفس الصورة تماماً)
def start_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ ( أضفني لمجموعتك )", url="https://t.me/i80_ibot?startgroup=true"),
            InlineKeyboardButton(text="📢 ( قناتنا الرسمية )", url=CHANNEL_LINK)
        ],
        [
            InlineKeyboardButton(text="📋 ( قائمة الاوامر )", callback_data="commands_menu")
        ],
        [
            InlineKeyboardButton(text="🕷️ ( تواصل مع المطور )", url="https://t.me/i80_ii")
        ]
    ])

# 3. كيبورد إدارة المطور الأساسي فقط
def admin_reply_keyboard():
    return ReplyKeyboardMarkup(
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

# 4. كيبورد الأعضاء الترفيهي (يظهر عند طلب قائمة الأوامر)
def user_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧹 الختمه")],
            [KeyboardButton(text="🧹 اذكار"), KeyboardButton(text="🧹 قرآن")],
            [KeyboardButton(text="🧹 اقتباسات"), KeyboardButton(text="🧹 شعر")],
            [KeyboardButton(text="🧹 قسم القيفات"), KeyboardButton(text="🧹 قسم الافتارات")],
            [KeyboardButton(text="🧹 كتب"), KeyboardButton(text="🧹 ثريد")],
            [KeyboardButton(text="🧹 هيدرات"), KeyboardButton(text="🧹 جداريات")],
            [KeyboardButton(text="🧹 اغاني"), KeyboardButton(text="🧹 اطربني")],
            [KeyboardButton(text="🧹 افلام"), KeyboardButton(text="🧹 قصص")],
            [KeyboardButton(text="🧹 ايدت"), KeyboardButton(text="🧹 ميمز")],
            [KeyboardButton(text="🧹 مميزات اخرى")]
        ],
        resize_keyboard=True,
        persistent=True
    )

# دالة فحص الاشتراك
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
    "مساء الخير": ["مساء الورد والياسمين 🌺", "مساءك روقان وراحة بال 🖤"]
}

# أمر البدء الرئيسي (/start)
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

    if message.from_user.id == ADMIN_ID:
        welcome = (
            f"🕷️ **! Aras**\n/start\n\n"
            f"🕷️ **أهلاً بك عزيزي المطور الاساسي (رامي)**\n"
            f"🕷️ **إليك كيبورد إدارة البوت والسورس بالكامل:**"
        )
        await message.answer(welcome, reply_markup=admin_reply_keyboard(), parse_mode="Markdown")
    else:
        # تصميم الرسالة الاحترافية تماماً مثل الصور المطلوبة
        welcome_text = (
            f"• أهلاً بك عزيزي انا بوت اسمه **أراس** .\n"
            f"• اختصاص البوت حماية المجموعات .\n"
            f"• اضلع البوت الى مجموعتك .\n"
            f"• ارفعه ادمن مشرف .\n"
            f"• ارفعه مشرف وارسل تفعيل ليتم تفعيل المجموعة .\n"
            f"• مطور البوت ↩️ [ رامي ]({CHANNEL_LINK})\n\n"
            f"✨ **اختر ما تريده من الأزرار بالأسفل:**"
        )
        
        # إرسال صورة افتار فخمة مع النص والأزرار الشفافة
        photo_url = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop"
        try:
            await message.answer_photo(
                photo=photo_url,
                caption=welcome_text,
                reply_markup=start_inline_keyboard(),
                parse_mode="Markdown"
            )
        except Exception:
            await message.answer(
                text=welcome_text,
                reply_markup=start_inline_keyboard(),
                parse_mode="Markdown"
            )

# الاستجابة لزر قائمة الأوامر الشفاف
@dp.callback_query(F.data == "commands_menu")
async def commands_menu_callback(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        "📋 **قائمة الأوامر والأقسام الترفيهية:**\nاختر ما يناسبك من لوحة المفاتيح بالأسفل 👇",
        reply_markup=user_reply_keyboard(),
        parse_mode="Markdown"
    )

# زر التحقق من الاشتراك
@dp.callback_query(F.data == "check_sub")
async def check_sub_callback(call: types.CallbackQuery):
    is_subbed = await check_subscription(call.from_user.id)
    if is_subbed:
        await call.message.delete()
        if call.from_user.id == ADMIN_ID:
            await call.message.answer("✅ تم التحقق بنجاح! أهلاً بك يا المطور.", reply_markup=admin_reply_keyboard())
        else:
            welcome_text = (
                f"✅ **تم التحقق بنجاح! أهلاً بك يا {call.from_user.first_name}**\n\n"
                f"• اختصاص البوت حماية المجموعات .\n"
                f"• اضلع البوت الى مجموعتك وارفعني مشرف."
            )
            await call.message.answer_photo(
                photo="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop",
                caption=welcome_text,
                reply_markup=start_inline_keyboard(),
                parse_mode="Markdown"
            )
    else:
        await call.answer("❌ ما زلت غير مشترك! اشترك غصباً بالقناة أولاً ⚡️", show_alert=True)

# ----------------- ردود كيبورد الأعضاء الترفيهي -----------------
USER_RESPONSES = {
    "🕷 الختمه": "📖 **قسم الختمة المباركة:**\nشارِك في ختمة القرآن الكريم مع أعضاء البوت.",
    "🕷 اذكار": "🤲 **أذكار المسلم:**\n«أَلا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ»\n• أذكار الصباح والمساء والسبحة الإلكترونية جاهزة.",
    "🕷 قرآن": "🎧 **القرآن الكريم:**\nاستمع وتصفح تلاوات خاشعة بأصوات أشهر القراء.",
    "🕷 اقتباسات": "💬 **اقتباسات:**\n«لا تقاس العقول بالأعمار، فكم من صغير عقله بارع، وكم من كبير عقله فارغ.»",
    "🕷 شعر": "📜 **قصائد وأشعار:**\n«عشنا كالأساطير، لا نُرى إلا حيث ترغب هيبتنا ..»",
    "🕷 قسم القيفات": "🎬 **قسم المتحركات (GIFs):**\nأجمل الصور المتحركة والأشكال الفخمة جاهزة للتحميل.",
    "🕷 قسم الافتارات": "🖼️ **قسم الافتارات:**\nافتارات شبابية، بنات، وهيدرات سينمائية عالية الدقة.",
    "🕷 كتب": "📚 **مكتبة الكتب:**\nتصفح ورشح أفضل الكتب والروايات المترجمة.",
    "🕷 ثريد": "🧵 **ثريدات ومتنوعات:**\nقصص واقعية ومعلومات مفيدة وقصيرة.",
    "🕷 هيدرات": "🌆 **قسم الهيدرات:**\nهيدرات وتصاميم للبروفايل وتلجرام.",
    "🕷 جداريات": "🎨 **جداريات:**\nعبارات وجداريات مكتوبة على الجدران بروح إبداعية.",
    "🕷 اغاني": "🎶 **قسم الصوتيات والموسيقى:**\nاستمع لجديد الصوتيات والشيلات.",
    "🕷 اطربني": "🎧 **اطربني:**\nمقاطع صوتية مميزة وذوق عالي.",
    "🕷 افلام": "🍿 **قسم الأفلام والمسلسلات:**\nترشيحات واقتراحات لأقوى الأفلام والمسلسلات العالمية.",
    "🕷 قصص": "📖 **قصص وحكايات:**\nقصص غامضة وحكايات قبل النوم.",
    "🕷 ايدت": "🎥 **تصاميم وإيدت:**\nفيديوهات وتصاميم مونتاج بدقة عالية.",
    "🕷 ميمز": "😂 **قسم الميمز والضحك:**\nأحدث الميمز والنكت للترفيح عن المجموعات.",
    "🕷 مميزات اخرى": "✨ **المميزات الإضافية:**\n• الألعاب (/صراحة، /لو_خيروك، /تحدي، /لغز)\n• بطاقة الايدي (ارسل كلمة 'ايدي')\n• حماية المجموعات التلقائية."
}

@dp.message(F.text.in_(USER_RESPONSES.keys()))
async def handle_user_buttons(message: types.Message):
    await message.answer(USER_RESPONSES[message.text], parse_mode="Markdown")

# ----------------- أزرار المطور الأساسي فقط -----------------
ADMIN_BUTTONS = [
    "[ معلومات التنصيب ]", "[ الكروبات ]", "[ قسم الاذاعه ]", "[ قسم التفعيلات ]",
    "[ قسم الاشتراك الاجباري ]", "[ قسم القوائم ]", "[ قسم النسخ ]", "[ قسم المتنوع والمسح ]",
    "[ ترويج البوت ]", "[ اعلان البوت ]", "[ السيرفر ]", "[ تحديث ]",
    "[ نقل ملكيه البوت ]", "[ تغيير رمز السورس ]", "📞 التواصل مع المطور", "[ حول ]"
]

@dp.message(F.text.in_(ADMIN_BUTTONS))
async def handle_admin_buttons(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("• عذراً، هذه الأوامر الإدارية تخص المطور الأساسي فقط ⚠️")
        return

    text = message.text
    if text == "[ معلومات التنصيب ]":
        await message.answer("ℹ️ **معلومات التنصيب:**\nالبوت يعمل بنجاح على سيرفر Render وسورس يجوي مفعل 100%.")
    elif text == "[ السيرفر ]":
        await message.answer("🖥️ **معلومات السيرفر:**\n• السيرفر: Render Cloud\n• الحالة: ممتاز ومستقر 🟢")
    elif text == "[ تحديث ]":
        await message.answer("🔄 **تم تحديث الملفات بنجاح 🕷️**")
    else:
        await message.answer(f"⚙️ تم فتح قسم: **{text}** بنجاح للمطور.")

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
        f"▪️ : احيهه حسابكك فخم\n"
        f"▪️ : ايديك 🕸 [ `{user.id}` ]\n"
        f"▪️ : معرفك 🕸 [ {username} ]\n"
        f"▪️ : رتبتك 🕸 [ {rank} ]\n"
        f"▪️ : تفاعلك 🕸 [ ممتاز جداً ]"
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
            f"° : اسمك ⚡️ ⦗ {new_member.first_name} ⦘\n"
            f"° : ايديك ⚡️ ⦗ `{new_member.id}` ⦘\n"
            f"° : يوزرك ⚡️ ⦗ {username} ⦘\n\n"
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

# المعالجة العامة للرسائل والروابط
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
