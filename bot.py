import os
import joblib
import numpy as np
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# 1. Sozlamalar
API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Modelni yuklash
model = joblib.load('knn_model.pkl')

# 2. Savollar zanjiri (FSM)
class DiabetForm(StatesGroup):
    pregnancies = State()
    glucose = State()
    blood_pressure = State()
    bmi = State()
    dpf = State()
    age = State()

# 3. Start va New Patient buyruqlari
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Assalomu alaykum! Diabet xavfini aniqlash botiga xush kelibsiz. Tahlilni boshlash uchun /newpatient buyrug'ini yozing.")

@dp.message_handler(commands=['newpatient'])
async def start_analysis(message: types.Message):
    await message.answer("Tahlilni boshlaymiz.\n1. Homiladorliklar sonini kiriting (Erkaklar uchun 0):")
    await DiabetForm.pregnancies.set()

# 4. Ma'lumotlarni yig'ish (Handlers)
@dp.message_handler(state=DiabetForm.pregnancies)
async def get_preg(message: types.Message, state: FSMContext):
    await state.update_data(p=message.text)
    await message.answer("2. Glyukoza miqdorini kiriting:")
    await DiabetForm.glucose.set()

@dp.message_handler(state=DiabetForm.glucose)
async def get_gluc(message: types.Message, state: FSMContext):
    await state.update_data(g=message.text)
    await message.answer("3. Qon bosimini kiriting (Blood Pressure):")
    await DiabetForm.blood_pressure.set()

@dp.message_handler(state=DiabetForm.blood_pressure)
async def get_bp(message: types.Message, state: FSMContext):
    await state.update_data(bp=message.text)
    await message.answer("4. Tana vazni indeksini (BMI) kiriting (Masalan: 26.6):")
    await DiabetForm.bmi.set()

@dp.message_handler(state=DiabetForm.bmi)
async def get_bmi(message: types.Message, state: FSMContext):
    await state.update_data(bmi=message.text)
    await message.answer("5. Diabetes Pedigree Function qiymatini kiriting (Masalan: 0.351):")
    await DiabetForm.dpf.set()

@dp.message_handler(state=DiabetForm.dpf)
async def get_dpf(message: types.Message, state: FSMContext):
    await state.update_data(dpf=message.text)
    await message.answer("6. Yoshingizni kiriting:")
    await DiabetForm.age.set()

# 5. Yakuniy tahlil va Outcome
@dp.message_handler(state=DiabetForm.age)
async def get_age_and_predict(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    
    # Barcha yig'ilgan ma'lumotlarni olamiz
    user_data = await state.get_data()
    
    try:
        # Ma'lumotlarni tartib bilan massivga joylaymiz
        input_features = np.array([[
            float(user_data['p']), 
            float(user_data['g']), 
            float(user_data['bp']), 
            float(user_data['bmi']), 
            float(user_data['dpf']), 
            float(user_data['age'])
        ]])

        # Bashorat (Outcome)
        prediction = model.predict(input_features)
        
        if prediction[0] == 1:
            result = "Diabet ehtimoli bor (Outcome: 1) 🆘. Shifokor bilan maslahatlashing."
        else:
            result = "Sizda diabet ehtimoli past (Outcome: 0) ✅. Sog'ligingizga e'tiborli bo'ling!"

        await message.answer(f"Tahlil natijasi: \n\n{result}")
    
    except ValueError:
        await message.answer("Xatolik: Iltimos faqat raqamlardan foydalaning. Qaytadan /newpatient buyrug'ini bosing.")
    
    # Holatni yakunlash
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)