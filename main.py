import asyncio
import re
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8963723966:AAE7qIh7ci0w4tROnYdvP-6KoOzWMn74AEo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# أزرار الترويج السريع
def share_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ أضف أراس لجروبك مجاناً", url="https://t.me/i80_ibot?startgroup=true")],
        [InlineKeyboardButton(text="📢 القناة الرسمية", url="https://t.me/i80_ii")]
    ])

# ردود تفاعلية منوعة
AUTO_RESPONSES = {
    "اراس": ["عيوني 🤍", "موجود يا قلبي، آمرني؟ 😊", "سمعني، وش بغيت يا غالي؟ ✨", "روحه وعيونه لأراس 🖤"],
    "صباح الخير": ["صباح النور والسرور ✨🌸", "صباحك يسعد روحك يا رب 🤍"],
    "مساء الخير": ["مساء الورد والياسمين 🌺", "مساءك روقان وراحة بال 🖤"],
    "منور": ["نورك ونور الموجودين يا عسل 🌟", "عكس نورك يا غالي ✨"],
    "احبك": ["وأراس يحبك ويحب روحك الحلوة 🖤✨"]
}

# بنك الألعاب والتسلية الكثيرة
GAMES_DATA = {
    "لو_خيروك": [
        "🤔 لو خيروك بين: العيش بدون إنترنت لمدة أسبوع VS العيش بدون هاتف نهائياً؟",
        "🤔 لو خيروك بين: السفر لأي مكان بالماضي VS السفر للمستقبل؟",
        "🤔 لو خيروك بين: قراءة أفكار الآخرين VS الاختفاء وقت ما تشاء؟",
        "🤔 لو خيروك بين: خسارة كل أموالك VS خسارة كل ذكرياتك؟"
    ],
    "صراحة": [
        "🎯 صراحة: ايش أكتر موقف محرج صار بحياتك ولا يمكن تنساه؟",
        "🎯 صراحة: مين الشخص الي مستحيل تنسى فضل عليّك؟",
        "🎯 صراحة: هل تحب العزلة والهدوء ولا الزحمة والجمعات؟",
        "🎯 صراحة: لو رجع بك الزمن لورا، ايش الشي الي بتغيره؟"
    ],
    "تحدي": [
        "🔥 تحدي: أرسل آخر صورة حافظها بالمعرض بدون خجل!",
        "🔥 تحدي: امدح الشخص الي قبلك بثلاث صفات حلوة.",
        "🔥 تحدي: اكتب اسمك المفضل وانت مغمض عيونك.",
        "🔥 تحدي: غيّر صورتك الشخصية لمدة ساعة لصورة كرتونية."
    ],
    "ألغاز": [
        "💡 لغز ذكاء: شيء يبتلعك إذا ما انتبهت له، وكل ما أخذت منه يكبر ولا ينقص فما هو؟ (الحفرة)",
        "💡 لغز ذكاء: ما هو الشيء الذي يمشي بلا أرجل ويطير بلا أجنحة ويبكي بلا عيون؟ (السحاب)",
        "💡 لغز ذكاء: من هو الشخص الذي يرى عدوه وصديقه بعين واحدة؟ (الأعور)"
    ]
}

QUOTES = [
    "«لا تقاس العقول بالأعمار، فكم من صغير عقله بارع، وكم من كبير عقله فارغ.»",
    "«الأمل هو الثورة الوحيدة التي لا تخون صاحبها أبداً.»",
    "«ابتسم، فسبحان من جعل الابتسامة في ديننا عبادة عليها نؤجر.»"
]

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    welcome = (
        f"👋 أهلاً بك يا {message.from_user.first_name}!\n\n"
        f"🤖 **أنا أراس (Aras) - حارس ومتفاعل المجموعات الذكي!**\n"
        f"أقوم بحماية جروبك، الرد على الأعضاء، وتوفير **ألعاب حماسية كثيرة** للجروب 🎮✨\n\n"
        f"👇 **أضفني لجروبك واستمتع بالألعاب والحماية:**"
    )
    await message.answer(welcome, reply_markup=share_keyboard(), parse_mode="Markdown")

# أوامر الألعاب الترفيهية
@dp.message(Command("لو_خيروك", "لوخيروك"))
async def game_lw_5yrwk(message: types.Message):
    await message.reply(random.choice(GAMES_DATA["لو_خيروك"]))

@dp.message(Command("صراحة"))
async def game_sra7a(message: types.Message):
    await message.reply(random.choice(GAMES_DATA["صراحة"]))

@dp.message(Command("تحدي"))
async def game_challenge(message: types.Message):
    await message.reply(random.choice(GAMES_DATA["تحدي"]))

@dp.message(Command("لغز", "ألغاز"))
async def game_puzzle(message: types.Message):
    await message.reply(random.choice(GAMES_DATA["ألغاز"]))

@dp.message(Command("اقتباس"))
async def send_quote(message: types.Message):
    await message.reply(random.choice(QUOTES))

@dp.message(F.text & ~F.text.startswith("/"))
async def handle_messages(message: types.Message):
    text = message.text.lower()

    if message.chat.type in ["group", "supergroup"]:
        # 1. الحماية من الروابط
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

    # 2. الردود التفاعلية العفوية
    for key, replies in AUTO_RESPONSES.items():
        if key in text:
            await message.reply(random.choice(replies))
            break

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
