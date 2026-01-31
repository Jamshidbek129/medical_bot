from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '8508837142:AAFBr3rxyizkj2J3rU7xPihU32D9n1YGlYw'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# /start komandasi va menyuni ko'rsatish
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/newpatient'))
    await message.answer("Assalomu alaykum! Quyidagi buyruqlardan foydalaning:", reply_markup=keyboard)

# /newpatient komandasi handleri
@dp.message_handler(commands=['newpatient'])
async def new_patient_handler(message: types.Message):
    await message.answer("Yangi bemor uchun qon bosimini kiriting:")

# Qon bosimi qiymatini qabul qilish uchun oddiy handler (keyingi bosqichda yaxshilaymiz)
@dp.message_handler()
async def handle_blood_pressure(message: types.Message):
    # Bu yerda modelni chaqirish va natijani hisoblash bo'lishi mumkin
    bp = message.text
    # Hozircha faqat javob qaytaramiz
    await message.answer(f"Siz kiritdingiz: {bp}. Model natijasini bu yerga qo‘yamiz.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
