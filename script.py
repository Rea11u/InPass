import tkinter as tk
from customtkinter import *
from customtkinter.windows.widgets.ctk_entry import CTkEntry  # Подключаем CTkEntry из вашего модуля

# Создаем окно приложения
app = tk.Tk()
app.geometry("300x165")

set_default_color_theme("green")

# Функция, которая будет вызываться при нажатии кнопки
def click_pass():
    password = entry.get()  # Получаем текст из CTkEntry
    print(password)  # Выводим текст в консоль

    # Определяем множества символов
    uppercase = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    symbols = set("-!*_")
    numbers = set("1234567890")
    russian_letters = set("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя")

    # Определяем список распространённых последовательностей
    common_sequences = [
        "qwerty", "asdfgh", "zxcvbn", "12345678", "password", "123456", "1234567", "123456789", "qwertyuiop",
        "1q2w3e4r", "1qaz2wsx", "admin", "letmein", "welcome", "monkey", "dragon", "football", "baseball",
        "abc123", "iloveyou", "sunshine", "princess", "admin123", "111111", "trustno1", "abc123456",
        "passw0rd", "zaq12wsx", "qazwsx", "michael", "superman", "batman", "master", "hello", "freedom",
        "whatever", "666666", "121212", "654321", "555555", "lovely", "welcome1", "123123", "654321",
        "000000", "1q2w3e4r5t", "1qazxsw2", "qweasdzxc", "q1w2e3r4", "password1", "password123", "qwerty123",
        "letmein123", "welcome123", "adminadmin", "lovely123", "mypass123", "123qwe", "321cba", "987654321",
        "password321", "myspace1", "mypassword", "temp1234", "password!"
    ]

    # Инициализируем флаги для каждого типа символов
    has_uppercase = False
    has_symbol = False
    has_number = False
    has_russian = False

    # Проходимся по каждому символу пароля
    for char in password:
        if char in uppercase:
            has_uppercase = True
        if char in symbols:
            has_symbol = True
        if char in numbers:
            has_number = True
        if char in russian_letters:
            has_russian = True

    # Подсчитываем количество типов символов
    quality = sum([has_uppercase, has_symbol, has_number])

    # Добавляем проверку длины пароля
    min_length = 8

    # Проверяем наличие подстрок из распространённых последовательностей
    password_lower = password.lower()
    is_common_sequence = any(seq in password_lower for seq in common_sequences)

    if has_russian:
        label.config(text="Смените язык!")
    elif len(password) < min_length:
        label.config(text="Ваш пароль слишком короткий")
    elif is_common_sequence:
        label.config(text="1/5, Совет: сделайте посложнее")
    elif quality == 0:
        label.config(text="2/5, Совет: добавьте заглавные")
    elif quality == 1:
        label.config(text="3/5, Совет: добавьте цифры")
    elif quality == 2:
        label.config(text="4/5, Совет: добавьте символы")
    elif quality == 3:
        label.config(text="5/5 Отличный пароль!")

# Показ защиты в очках
label = tk.Label(master=app, text="Насколько защищён ваш пароль")
label.pack(pady=20, padx=20)

# Создаем экземпляр CTkEntry и сохраняем ссылку на него в переменной
entry = CTkEntry(master=app, placeholder_text="Введите пароль...", width=250, height=30)
entry.pack()

# Создаем кнопку
button = CTkButton(app, text="Проверить пароль", command=click_pass)
button.pack(pady=20, padx=20)

# Запускаем главный цикл приложения
app.mainloop()