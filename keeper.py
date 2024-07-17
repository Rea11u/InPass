from PIL import Image
import numpy as np
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

def atbash_cipher(text, encrypt=True):
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                result += chr(219 - ord(char))  # 219 is the ASCII code for 'z'
            elif char.isupper():
                result += chr(155 - ord(char))  # 155 is the ASCII code for 'Z'
        else:
            result += char
    return result

def playfair_cipher(text, key, encrypt=True):
    def prepare_text(text):
        # Remove spaces and convert to uppercase
        text = text.upper().replace(" ", "")
        # Replace 'J' with 'I'
        text = text.replace("J", "I")
        # Split into bigrams
        pairs = []
        i = 0
        while i < len(text):
            if i == len(text) - 1 or text[i] == text[i + 1]:
                pairs.append(text[i] + 'X')
                i += 1
            else:
                pairs.append(text[i] + text[i + 1])
                i += 2
        return pairs

    def generate_square(key):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Without 'J'
        key = key.upper().replace("J", "I")
        key_set = set(key)
        remaining_letters = [l for l in alphabet if l not in key_set]

        square = list(key)
        for letter in remaining_letters:
            square.append(letter)

        return square

    def find_coordinates(square, letter):
        index = square.index(letter)
        return (index // 5, index % 5)

    def playfair_encrypt_decrypt(text, key, encrypt=True):
        square = generate_square(key)
        pairs = prepare_text(text)
        result = []
        direction = 1 if encrypt else -1

        for pair in pairs:
            row1, col1 = find_coordinates(square, pair[0])
            row2, col2 = find_coordinates(square, pair[1])

            if row1 == row2:
                result.append(square[row1 * 5 + (col1 + direction) % 5])
                result.append(square[row2 * 5 + (col2 + direction) % 5])
            elif col1 == col2:
                result.append(square[((row1 + direction) % 5) * 5 + col1])
                result.append(square[((row2 + direction) % 5) * 5 + col2])
            else:
                result.append(square[row1 * 5 + col2])
                result.append(square[row2 * 5 + col1])

        return ''.join(result)

    return playfair_encrypt_decrypt(text, key, encrypt)

def morse_code(text, encrypt=True):
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

    if encrypt:
        return ' '.join(MORSE_CODE_DICT[char] for char in text.upper() if char in MORSE_CODE_DICT)
    else:
        inverse_morse_dict = {value: key for key, value in MORSE_CODE_DICT.items()}
        return ''.join(inverse_morse_dict[code] for code in text.split(' '))

# Создание GUI с использованием customtkinter
class EncryptorDecryptorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Keeper")
        self.geometry("500x650")

        self.algorithm_label = ctk.CTkLabel(self, text="Выберите шифр:")
        self.algorithm_label.pack(pady=10)

        self.algorithm = tk.StringVar(value="Цезаря")
        self.algorithm_menu = ctk.CTkOptionMenu(self, variable=self.algorithm, values=["Цезаря", "Виженера", "Атбаш", "Плейфер", "Азбука Морзе", "Стеганография"])
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
        elif algorithm == "Атбаш":
            result = atbash_cipher(text, encrypt=True)
        elif algorithm == "Плейфер":
            result = playfair_cipher(text, key, encrypt=True)
        elif algorithm == "Азбука Морзе":
            result = morse_code(text, encrypt=True)
        elif algorithm == "Стеганография":
            # Создаем черное изображение
            image = Image.new('RGB', (100, 100), color=(0, 0, 0))
            pixels = np.array(image)

            # Секретное сообщение
            secret_message = text
            binary_message = ''.join(format(ord(char), '08b') for char in secret_message)

            # Встраиваем сообщение в изображение
            index = 0
            for i in range(pixels.shape[0]):
                for j in range(pixels.shape[1]):
                    if index < len(binary_message):
                        r, g, b = pixels[i, j]
                        r = (r & ~1) | int(binary_message[index])
                        pixels[i, j] = (r, g, b)
                        index += 1

            # Сохраняем изображение
            encoded_image = Image.fromarray(pixels)
            encoded_image.save('encoded_image.png')

            result = "Сообщение успешно встроено в изображение 'encoded_image.png'"

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
        elif algorithm == "Атбаш":
            result = atbash_cipher(text, encrypt=False)
        elif algorithm == "Плейфер":
            result = playfair_cipher(text, key, encrypt=False)
        elif algorithm == "Азбука Морзе":
            result = morse_code(text, encrypt=False)
        elif algorithm == "Стеганография":
            try:
                # Загружаем изображение с закодированным сообщением
                encoded_image = Image.open('encoded_image.png')
                pixels = np.array(encoded_image)

                # Извлекаем сообщение из изображения
                binary_message = ""
                for i in range(pixels.shape[0]):
                    for j in range(pixels.shape[1]):
                        r, g, b = pixels[i, j]
                        binary_message += str(r & 1)

                # Преобразуем бинарное сообщение обратно в текст
                secret_message = ""
                for k in range(0, len(binary_message), 8):
                    byte = binary_message[k:k+8]
                    secret_message += chr(int(byte, 2))

                result = "Извлеченное сообщение: " + secret_message
            except FileNotFoundError:
                result = "Ошибка: Файл 'encoded_image.png' не найден"

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
