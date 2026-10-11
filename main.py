import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

TOKEN = "8963723966:AAE7qIh7ci0w4tROnYdvP-6KoOzWMn74AEo"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# الترحيب بالأعضاء الجدد
@dp.message(F.new_chat_members)
async def welcome_new_member(message: Message):
    for member in message.new_chat_members:
        if member.id == bot.id:
            await message.answer("شكرًا لإضافتي! يرجى رفعي مشرفاً لأتمكن من حماية المجموعة.")
        else:
            await message.answer(f"أهلاً بك يا {member.full_name} في المجموعة! 🌹")

# حذف الروابط للحماية من الإعلانات والسبام
@dp.message(F.chat.type.in_({"group", "supergroup"}) & F.text & (F.text.contains("http://") | F.text.contains("https://") | F.text.contains("t.me/")))
async def anti_link(message: Message):
    try:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in ["creator", "administrator"]:
            return  # استثناء المشرفين

        await message.delete()
        warn = await message.answer(f"⚠️ يمنع إرسال الروابط يا {message.from_user.first_name}!")
        await asyncio.sleep(4)
        await warn.delete()
    except Exception as e:
        print(f"Error: {e}")

async def main():
    print("البوت يعمل...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
