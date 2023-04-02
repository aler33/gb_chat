"""
Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""

word_1 = b"class"
word_2 = b"function"
word_3 = b"method"

print(f'Тип- {type(word_1)}, содержимое- {word_1}, длина- {len(word_1)}')
print(f'Тип- {type(word_2)}, содержимое- {word_2}, длина- {len(word_2)}')
print(f'Тип- {type(word_3)}, содержимое- {word_3}, длина- {len(word_3)}')
