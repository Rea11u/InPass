import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import random

# Настройка приложения
app = ctk.CTk()
app.geometry("500x350")
app.title("Шифр")

# Список возможных сообщений
messages = [
    "Hello, this is a secret message!",
    "Python is fun and easy to learn.",
    "Cryptography is fascinating.",
    "Keep your passwords safe and secure.",
    "This is a challenging game.",
]

# Функция для шифра Цезаря
def caesar_cipher_encrypt(text, shift):
    encrypted = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted += char
    return encrypted

# Функция для шифра Атбаш
def atbash_cipher_encrypt(text):
    encrypted = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted += chr(shift_base + (25 - (ord(char) - shift_base)))
        else:
            encrypted += char
    return encrypted

# Функция для расшифровки шифра Цезаря
def caesar_cipher_decrypt(text, shift):
    return caesar_cipher_encrypt(text, -shift)

# Функция для расшифровки шифра Атбаш
def atbash_cipher_decrypt(text):
    return atbash_cipher_encrypt(text)

# Функция для выбора случайного зашифрованного сообщения
def generate_random_encrypted_message():
    shift = random.randint(1, 25)
    cipher = random.choice(["caesar", "atbash"])
    message = random.choice(messages)
    if cipher == "caesar":
        encrypted_message = caesar_cipher_encrypt(message, shift)
    elif cipher == "atbash":
        encrypted_message = atbash_cipher_encrypt(message)
    return encrypted_message, cipher, shift

# Функция для обработки ввода
def decrypt_message():
    message = entry_message.get()
    selected_cipher = var_cipher.get()
    if selected_cipher == "Caesar":
        shift = int(entry_shift.get())
        decrypted_message = caesar_cipher_decrypt(message, shift)
    elif selected_cipher == "Atbash":
        decrypted_message = atbash_cipher_decrypt(message)
    else:
        decrypted_message = "Unknown cipher selected."
    
    messagebox.showinfo("Decrypted Message", f"The decrypted message is:\n{decrypted_message}")

# UI элементы
label_title = ctk.CTkLabel(app, text="Интерактив", font=("Arial", 20))
label_title.pack(pady=20)

frame_input = ctk.CTkFrame(app)
frame_input.pack(pady=10)

label_message = ctk.CTkLabel(frame_input, text="Сообщение:", font=("Arial", 14))
label_message.grid(row=0, column=0, padx=10, pady=5)
entry_message = ctk.CTkEntry(frame_input, width=200)
entry_message.grid(row=0, column=1, padx=10, pady=5)

label_shift = ctk.CTkLabel(frame_input, text="Ключ (для Цезаря)", font=("Arial", 14))
label_shift.grid(row=1, column=0, padx=10, pady=5)
entry_shift = ctk.CTkEntry(frame_input, width=50)
entry_shift.grid(row=1, column=1, padx=10, pady=5)

label_cipher = ctk.CTkLabel(frame_input, text="Шифр:", font=("Arial", 14))
label_cipher.grid(row=2, column=0, padx=10, pady=5)
var_cipher = tk.StringVar(value="Caesar")
radio_caesar = ctk.CTkRadioButton(frame_input, text="Цезарь", variable=var_cipher, value="Caesar")
radio_atbash = ctk.CTkRadioButton(frame_input, text="Атбаш", variable=var_cipher, value="Atbash")
radio_caesar.grid(row=2, column=1, padx=10, pady=5)
radio_atbash.grid(row=2, column=2, padx=10, pady=5)

button_decrypt = ctk.CTkButton(app, text="Дешифровать", command=decrypt_message)
button_decrypt.pack(pady=20)

button_generate = ctk.CTkButton(app, text="Сгенерировать новое сообщение", command=lambda: generate_new_message())
button_generate.pack(pady=10)

# Функция для генерации нового случайного зашифрованного сообщения
def generate_new_message():
    encrypted_message, cipher, shift = generate_random_encrypted_message()
    entry_message.delete(0, tk.END)
    entry_message.insert(0, encrypted_message)
    if cipher == "caesar":
        var_cipher.set("Caesar")
        entry_shift.delete(0, tk.END)
        entry_shift.insert(0, shift)
    elif cipher == "atbash":
        var_cipher.set("Atbash")
        entry_shift.delete(0, tk.END)

# Генерация начального зашифрованного сообщения
generate_new_message()

app.mainloop()