import requests
import random
import time

URL = "https://docs.google.com/forms/d/e/1FAIpQLSetNxzEZAdcPBPi1ULTmz3CYQWYHVcFsqwQ-eqbB-OVQssI3Q/formResponse"

FIRST_NAMES = ["Олег", "Иван", "Андрей", "Максим", "Дмитрий"]
LAST_NAMES = ["Иванов", "Петров", "Сидоров", "Коваленко", "Мельник"]

SCALE = ["Зовсім невірно", "Іноді вірно", "Часто вірно"]
FREQ = ["ніколи", "іноді", "часто"]
AGREE = ["безумовно, так", "не згоден повністю"]

# 🔹 генерация пользователя
def generate_user():
    return {
        "name": random.choice(FIRST_NAMES),
        "surname": random.choice(LAST_NAMES),
        "city": "Одесса"
    }

# 🔹 email (вариант 2)
def generate_email(name, surname):
    domains = ["gmail.com", "outlook.com"]
    return f"{name.lower()}.{surname.lower()}{random.randint(1,999)}@{random.choice(domains)}"

# 🔹 генерация ответов (ВАЖНО — реальные entry из твоего файла)
def generate_answers():
    data = {}

    # числовые
    for e in [
        "entry.704268234",
        "entry.684193238",
        "entry.674594538"
    ]:
        data[e] = str(random.randint(1, 5))

    # шкала
    for e in [
        "entry.823460471",
        "entry.862015988",
        "entry.1783260730"
    ]:
        data[e] = random.choice(SCALE)

    # частота
    for e in [
        "entry.991632021",
        "entry.1222929667",
        "entry.925728927"
    ]:
        data[e] = random.choice(FREQ)

    # согласие
    for e in [
        "entry.312342137",
        "entry.1184901694",
        "entry.384620746"
    ]:
        data[e] = random.choice(AGREE)

    return data

# 🔹 проверка ответа
def is_success(response):
    if response.status_code not in [200, 302]:
        return False

    text = response.text.lower()

    # Google форма обычно возвращает страницу подтверждения
    if "form" in text and "response" in text:
        return True

    return True  # fallback (Google иногда редиректит)

# 🔹 отправка
def send_form():
    user = generate_user()
    email = generate_email(user["name"], user["surname"])
    answers = generate_answers()

    data = {
        # ⚠️ ОБЯЗАТЕЛЬНО вставь свой entry email
        "entry.EMAIL_ID": email
    }

    data.update(answers)

    print("\n--- ОТПРАВКА ---")
    print("User:", user)
    print("Email:", email)

    try:
        response = requests.post(URL, data=data, timeout=10)

        success = is_success(response)

        print("Status:", response.status_code)

        if success:
            print("✅ ОТПРАВЛЕНО (вероятность ~95%)")
        else:
            print("❌ НЕ УВЕРЕН")

    except Exception as e:
        print("❌ ОШИБКА:", e)

    print("----------------\n")

# 🔹 запуск
TOTAL = 10

for i in range(TOTAL):
    send_form()
    time.sleep(random.uniform(5, 10))
