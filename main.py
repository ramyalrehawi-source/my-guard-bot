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
ADMIN_ID = 8921676913  # آيدي الخاص بك
CHANNEL_USERNAME = "@i80_ii"
CHANNEL_LINK = "https://t.me/+Nf1ReXca_D45ODg0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# الأزرار الشفافة لبدء التشغيل
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

# لوحة تحكم المطور الأساسي
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

# لوحة الأعضاء الترفيهية
def user_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🕷 الختمه")],
            [KeyboardButton(text="🕷 اذكار"), KeyboardButton(text="🕷 قرآن")],
            [KeyboardButton(text="🕷 اقتباسات"), KeyboardButton(text="🕷 شعر")],
            [KeyboardButton(text="🕷 قسم القيفات"), KeyboardButton(text="🕷 قسم الافتارات")],
            [KeyboardButton(text="🕷 كتب"), KeyboardButton(text="🕷 ثريد")],
            [KeyboardButton(text="🕷 هيدرات"), KeyboardButton(text="🕷 جداريات")],
            [KeyboardButton(text="🕷 اغاني"), KeyboardButton(text="🕷 اطربني")],
            [KeyboardButton(text="🕷 افلام"), KeyboardButton(text="🕷 قصص")],
            [KeyboardButton(text="🕷 ايدت"), KeyboardButton(text="🕷 ميمز")],
            [KeyboardButton(text="🕷 مميزات اخرى")]
        ],
        resize_keyboard=True,
        persistent=True
    )

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "🕷️ **أهلاً بك عزيزي المطور الأساسي (رامي)**\nإليك لوحة تحكم السورس:",
            reply_markup=admin_reply_keyboard(),
            parse_mode="Markdown"
        )
    else:
        welcome_text = (
            f"• أهلاً بك عزيزي انا بوت اسمه **أراس** .\n"
            f"• اختصاص البوت حماية المجموعات .\n"
            f"• اضلع البوت الى مجموعتك وارفعني مشرف.\n"
            f"• مطور البوت ↩️ [ رامي ]({CHANNEL_LINK})\n\n"
            f"✨ **اختر ما تريده من الأزرار بالأسفل:**"
        )
        try:
            await message.answer_photo(
                photo="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop",
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

@dp.callback_query(F.data == "commands_menu")
async def commands_menu_callback(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        "📋 **قائمة الأوامر والأقسام الترفيهية:**",
        reply_markup=user_reply_keyboard(),
        parse_mode="Markdown"
    )

USER_RESPONSES = {
    "🕷 الختمه": "📖 **قسم الختمة المباركة**",
    "🕷 اذكار": "🤲 **أذكار المسلم**",
    "🕷 قرآن": "🎧 **القرآن الكريم**",
    "🕷 اقتباسات": "💬 **اقتباسات مميزة**",
    "🕷 شعر": "📜 **قصائد وأشعار**",
    "🕷 مميزات اخرى": "✨ **المميزات الإضافية مفعلة**"
}

@dp.message(F.text.in_(USER_RESPONSES.keys()))
async def handle_user_buttons(message: types.Message):
    await message.answer(USER_RESPONSES[message.text], parse_mode="Markdown")

ADMIN_BUTTONS = [
    "[ معلومات التنصيب ]", "[ الكروبات ]", "[ قسم الاذاعه ]", "[ قسم التفعيلات ]",
    "[ قسم الاشتراك الاجباري ]", "[ قسم القوائم ]", "[ قسم النسخ ]", "[ قسم المتنوع والمسح ]",
    "[ ترويج البوت ]", "[ اعلان البوت ]", "[ السيرفر ]", "[ تحديث ]",
    "[ نقل ملكيه البوت ]", "[ تغيير رمز السورس ]", "📞 التواصل مع المطور", "[ حول ]"
]

@dp.message(F.text.in_(ADMIN_BUTTONS))
async def handle_admin_buttons(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer(f"⚙️ تم تنفيذ أمر: **{message.text}** بنجاح.", parse_mode="Markdown")

@dp.message(F.text.in_(["ا", "ايدي", "ايديك"]))
async def user_id_info(message: types.Message):
    user = message.from_user
    info_text = (
        f"▪️ : احيهه حسابكك فخم\n"
        f"▪️ : ايديك 🕸 [ `{user.id}` ]\n"
        f"▪️ : معرفك 🕸 [ @{user.username if user.username else 'لا يوجد'} ]"
    )
    await message.reply(info_text, parse_mode="Markdown")

@dp.message(F.text)
async def handle_all_messages(message: types.Message):
    if message.text and "اراس" in message.text.lower():
        await message.reply("عيوني أراس موجود 🖤")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
