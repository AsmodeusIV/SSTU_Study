import matplotlib.pyplot as plt
import numpy as np

# Определение функции принадлежности
def mu(x):
    if x <= 1:
        return 1
    elif 1 < x <= 3:
        return -0.5*x+1.5
    elif 3 < x <= 5:
        return 1-1
    elif 5 < x <= 7:
        return 0.03*x
    else:
        return 1

# Создание массива значений x, начиная с 1
x = np.arange(1, 8, 0.1)  # от 1 до 8 с шагом 0.1

# Вычисление значений функции принадлежности для каждого x
y = [mu(val) for val in x]

# Построение графика
plt.plot(x, y)
plt.xlabel("День недели")
plt.ylabel("Функция принадлежности")
plt.title("Нечеткое множество \"Начало недели\"")
plt.xticks(range(1, 8), ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]) # Подписи на оси X, начиная с 1
plt.grid(True)
plt.xlim(1,7) # Устанавливаем пределы оси X, чтобы не показывать 0
plt.show()
