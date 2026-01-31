from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = '8508837142:AAFBr3rxyizkj2J3rU7xPihU32D9n1YGlYw'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! Yangi bemor qo'shish uchun /newpatient buyrug'ini yuboring.")

@dp.message_handler(commands=['newpatient'])
async def ask_blood_pressure(message: types.Message):
    await message.reply("Iltimos, bemorning qon bosimini kiriting (masalan: 120/80).")

@dp.message_handler()
async def handle_bp(message: types.Message):
    bp = message.text
    # Bu yerda modelga tekshirish funksiyasini qo'shasiz, hozir oddiy javob beramiz
    await message.reply(f"Siz kiritgan qon bosimi: {bp}. Model natijasi hali yo'q.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
