import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# Генерируем данные для трех классов
np.random.seed(42) # Фиксируем seed для генератора случайных чисел, чтобы результаты были воспроизводимы. 42 - простое число
class1_x = np.random.normal(loc=2, scale=1, size=50) # Генерируем 50 значений для координаты x первого класса, распределенных нормально со средним 2 и стандартным отклонением 1
class1_y = np.random.normal(loc=2, scale=1, size=50) # Генерируем 50 значений для координаты y первого класса, распределенных нормально со средним 2 и стандартным отклонением 1
class2_x = np.random.normal(loc=7, scale=1, size=50) # Аналогично для второго класса, среднее 7
class2_y = np.random.normal(loc=7, scale=1, size=50) # Аналогично для второго класса, среднее 7
class3_x = np.random.normal(loc=4, scale=1, size=50) # Аналогично для третьего класса, среднее 4
class3_y = np.random.normal(loc=7, scale=1, size=50) # Аналогично для третьего класса, среднее 7

# Объединяем данные и метки классов
X = np.column_stack((np.concatenate((class1_x, class2_x, class3_x)), # объединяем координаты x всех классов в один массив
                     np.concatenate((class1_y, class2_y, class3_y)))) # объединяем координаты y всех классов в один массив
# X теперь содержит все точки данных, каждая строка - это точка (x, y)
y = np.concatenate((np.zeros(50), np.ones(50), 2 * np.ones(50))) # создаем массив меток классов: 0 для первого класса, 1 для второго, 2 для третьего

# Разделяем данные на тренировочный и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 20% данных - тестовые, 80% - тренировочные. random_state=42 гарантирует одинаковое разделение при каждом запуске

# Обучаем модель k-NN (k=3)
knn = KNeighborsClassifier(n_neighbors=3) # создаем объект классификатора k-NN с k=3 (3 ближайших соседа)
knn.fit(X_train, y_train) # обучаем модель на тренировочных данных

# Предсказываем классы для тестового набора
predictions = knn.predict(X_test) # предсказываем классы для тестовых данных

# Оцениваем точность
accuracy = np.mean(predictions == y_test) # считаем долю правильных предсказаний
print(f"Точность: {accuracy}")

# Визуализация
plt.figure(figsize=(8, 6)) # создаем график размером 8x6 дюймов
plt.scatter(class1_x, class1_y, label='Класс 1', color='red') # отображаем точки первого класса красным
plt.scatter(class2_x, class2_y, label='Класс 2', color='green') # отображаем точки второго класса зеленым
plt.scatter(class3_x, class3_y, label='Класс 3', color='blue') # отображаем точки третьего класса синим
plt.scatter(X_test[:, 0], X_test[:, 1], marker='x', color='black', label='Тестовые точки', s=100) # отображаем тестовые точки черными крестиками

# Рисуем границы принятия решений (упрощенное представление)
x_min, x_max = plt.xlim() # получаем границы области по x
y_min, y_max = plt.ylim() # получаем границы области по y
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100)) # создаем сетку точек для построения границ
Z = knn.predict(np.c_[xx.ravel(), yy.ravel()]) # предсказываем классы для каждой точки сетки
Z = Z.reshape(xx.shape) # преобразуем предсказания в форму сетки
plt.contourf(xx, yy, Z, alpha=0.2) # рисуем границы принятия решений с прозрачностью 0.2

plt.xlabel('X') # подпись оси x
plt.ylabel('Y') # подпись оси y
plt.title('Классификация точек методом k-NN') # заголовок графика
plt.legend() # отображаем легенду
plt.show() # показываем график

k_values = [1, 3, 5, 10, 20, 30, 50]

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    predictions = knn.predict(X_test)
    accuracy = np.mean(predictions == y_test)
    print(f"Точность при k={k}: {accuracy}")

    plt.figure(figsize=(8, 6))
    plt.scatter(class1_x, class1_y, label='Класс 1', color='red')
    plt.scatter(class2_x, class2_y, label='Класс 2', color='green')
    plt.scatter(class3_x, class3_y, label='Класс 3', color='blue')
    plt.scatter(X_test[:, 0], X_test[:, 1], marker='x', color='black', label='Тестовые точки', s=100)

    x_min, x_max = plt.xlim()
    y_min, y_max = plt.ylim()
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.2)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Классификация при k={k}')
    plt.legend()
    plt.show()


metrics = [
    ('euclidean', 'Евклидова метрика'),
    ('manhattan', 'Манхэттенская метрика'),
    ('chebyshev', 'Метрика Чебышева'),
    ('minkowski_p2', 'Минковского (p=2)'),
    ('minkowski_p3', 'Минковского (p=3)'),
]

for metric, name in metrics:
    if metric.startswith('minkowski'):
        p = int(metric.split('_')[-1][1:])
        knn = KNeighborsClassifier(n_neighbors=3, metric='minkowski', p=p)
    else:
        knn = KNeighborsClassifier(n_neighbors=3, metric=metric)
    
    knn.fit(X_train, y_train)
    predictions = knn.predict(X_test)
    accuracy = np.mean(predictions == y_test)
    print(f"Точность при метрике '{name}': {accuracy}")

    plt.figure(figsize=(8, 6))
    plt.scatter(class1_x, class1_y, label='Класс 1', color='red')
    plt.scatter(class2_x, class2_y, label='Класс 2', color='green')
    plt.scatter(class3_x, class3_y, label='Класс 3', color='blue')
    plt.scatter(X_test[:, 0], X_test[:, 1], marker='x', color='black', label='Тестовые точки', s=100)

    x_min, x_max = plt.xlim()
    y_min, y_max = plt.ylim()
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.2)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Классификация с метрикой: {name}')
    plt.legend()
    plt.show()