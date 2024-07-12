import tkinter as tk
import customtkinter as ctk

# Алгоритмы шифрования и дешифрования с поддержкой русского языка
def caesar_cipher(text, shift, encrypt=True):
    result = ""
    shift = shift if encrypt else -shift
    for char in text:
        if char.isalpha():
            if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
                shift_base = 65 if char.isupper() else 97
                result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            elif 'А' <= char <= 'Я' or 'а' <= char <= 'я':
                shift_base = 1040 if char.isupper() else 1072
                result += chr((ord(char) - shift_base + shift) % 32 + shift_base)
        else:
            result += char
    return result

def vigenere_cipher(text, key, encrypt=True):
    result = ""
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
                shift = ord(key[key_index]) - 97 if 'a' <= key[key_index] <= 'z' else ord(key[key_index]) - 65
                shift = shift if encrypt else -shift
                shift_base = 65 if char.isupper() else 97
                result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            elif 'А' <= char <= 'Я' or 'а' <= char <= 'я':
                shift = ord(key[key_index]) - 1072 if 'а' <= key[key_index] <= 'я' else ord(key[key_index]) - 1040
                shift = shift if encrypt else -shift
                shift_base = 1040 if char.isupper() else 1072
                result += chr((ord(char) - shift_base + shift) % 32 + shift_base)
            key_index = (key_index + 1) % len(key)
        else:
            result += char
    return result

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.', 'Ж': '...-', 'З': '--..', 'И': '..', 'Й': '.---',
    'К': '-.-', 'Л': '.-..', 'М': '--', 'Н': '-.', 'О': '---', 'П': '.--.', 'Р': '.-.', 'С': '...', 'Т': '-', 'У': '..-',
    'Ф': '..-.', 'Х': '....', 'Ц': '-.-.', 'Ч': '---.', 'Ш': '----', 'Щ': '--.-', 'Ъ': '.--.-.', 'Ы': '-.--', 'Ь': '-..-',
    'Э': '..-..', 'Ю': '..--', 'Я': '.-.-',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

def morse_code(text, encrypt=True):
    if encrypt:
        return ' '.join(MORSE_CODE_DICT[char] for char in text.upper())
    else:
        inverse_morse_dict = {value: key for key, value in MORSE_CODE_DICT.items()}
        return ''.join(inverse_morse_dict[code] for code in text.split(' '))

# Создание GUI с использованием customtkinter
class EncryptorDecryptorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Keeper")
        self.geometry("500x550")

        self.algorithm_label = ctk.CTkLabel(self, text="Выберите шифр:")
        self.algorithm_label.pack(pady=10)

        self.algorithm = tk.StringVar(value="Цезаря")
        self.algorithm_menu = ctk.CTkOptionMenu(self, variable=self.algorithm, values=["Цезаря", "Виженера", "Азбука Морзе"])
        self.algorithm_menu.pack(pady=10)

        self.input_label = ctk.CTkLabel(self, text="Введите текст:")
        self.input_label.pack(pady=10)

        self.input_text = ctk.CTkEntry(self, width=400)
        self.input_text.pack(pady=10)

        self.key_label = ctk.CTkLabel(self, text="Введите ключ (если требуется):")
        self.key_label.pack(pady=10)

        self.key_entry = ctk.CTkEntry(self, width=400)
        self.key_entry.pack(pady=10)

        self.encrypt_button = ctk.CTkButton(self, text="Зашифровать", command=self.encrypt)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = ctk.CTkButton(self, text="Расшифровать", command=self.decrypt)
        self.decrypt_button.pack(pady=10)

        self.use_result_button = ctk.CTkButton(self, text="Использовать результат", command=self.use_result)
        self.use_result_button.pack(pady=10)

        self.output_label = ctk.CTkLabel(self, text="Результат:")
        self.output_label.pack(pady=10)

        self.output_text = ctk.CTkEntry(self, width=400)
        self.output_text.pack(pady=10)

    def encrypt(self):
        algorithm = self.algorithm.get()
        text = self.input_text.get()
        key = self.key_entry.get()

        if algorithm == "Цезаря":
            try:
                shift = int(key)
                result = caesar_cipher(text, shift, encrypt=True)
            except ValueError:
                result = "Ошибка: Ключ должен быть числом"
        elif algorithm == "Виженера":
            result = vigenere_cipher(text, key, encrypt=True)
        elif algorithm == "Азбука Морзе":
            result = morse_code(text, encrypt=True)
        else:
            result = "Неизвестный шифр"

        self.output_text.delete(0, tk.END)
        self.output_text.insert(0, result)

    def decrypt(self):
        algorithm = self.algorithm.get()
        text = self.input_text.get()
        key = self.key_entry.get()

        if algorithm == "Цезаря":
            try:
                shift = int(key)
                result = caesar_cipher(text, shift, encrypt=False)
            except ValueError:
                result = "Ошибка: Ключ должен быть числом"
        elif algorithm == "Виженера":
            result = vigenere_cipher(text, key, encrypt=False)
        elif algorithm == "Азбука Морзе":
            result = morse_code(text, encrypt=False)
        else:
            result = "Неизвестный шифр"

        self.output_text.delete(0, tk.END)
        self.output_text.insert(0, result)

    def use_result(self):
        result = self.output_text.get()
        self.input_text.delete(0, tk.END)
        self.input_text.insert(0, result)

if __name__ == "__main__":
    app = EncryptorDecryptorApp()
    app.mainloop()