"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
"""

word_1, word_2, word_3, word_4 = "разработка", "администрирование", "protocol", "standard"
print(f"Изначальные слова:\n {word_1}\n {word_2}\n {word_3}\n {word_4}")

word_b_1 = word_1.encode('utf-8')
word_b_2 = word_2.encode('utf-8')
word_b_3 = word_3.encode('utf-8')
word_b_4 = word_4.encode('utf-8')
print(f"Слова в байтовом виде:\n {word_b_1}\n {word_b_2}\n {word_b_3}\n {word_b_4}")

word_e_1 = word_b_1.decode('utf-8')
word_e_2 = word_b_2.decode('utf-8')
word_e_3 = word_b_3.decode('utf-8')
word_e_4 = word_b_4.decode('utf-8')
print(f"Слова в строковом виде преобразованные из байт:\n {word_e_1}\n {word_e_2}\n {word_e_3}\n {word_e_4}")
