print("Здравствуйте!\n")

name = input("Введите имя: ")
print(f"Привет, {name}!")

age_input = input("Введите возраст: ")
try:
    age = int(age_input)
    print(f"Ваш возраст: {age} лет.")
    if age < 18:
        print("Вы несовершеннолетний.")
except ValueError:
    print("Ошибка: возраст должен быть числом.")

print("\nСпасибо за использование программы! С вас 5$!")