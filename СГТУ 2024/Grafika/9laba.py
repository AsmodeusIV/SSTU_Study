from PIL import Image
"""
img = Image.open("C:\\Users\\admin\\Downloads\\111.jpg")

img.show()
"""

"""
f1 = open("C:\\Users\\admin\\Downloads\\111.jpg","rb")
img1 = Image.open(f1)
img1.show()
f1.close()
"""
"""
f1 = open("C:\\Users\\admin\\Downloads\\111.jpg","rb")
i = f1.read()
f1.close()
import io
img = Image.open(io.BytesIO(i))
img.show()
"""


"""
image = Image.open("C:\\Users\\admin\\Downloads\\111.jpg")

print(f"Формат файла: {image.format}")
print(f"Размер изображения: {image.size}")
print(f"Цветовая модель: {image.mode}")

print(f"Цветовая модель: {image.mode}")

print(f"Ширина: {image.width}")
print(f"Высота: {image.height}")

print(f"Прямоугольная область: {image.getbbox()}")
"""



from PIL import Image

# Черный квадрат
img = Image.new("RGB", (100, 100))
img.show()

# Красный квадрат
img = Image.new("RGB", (100, 100), (255, 0, 0))
img.show()

# Цветной прямоугольник
img = Image.new("RGB", (320, 240), "rgb(205, 100,200)")
img.show()

# Сиреневый прямоугольник
img = Image.new("RGB", (640, 480), "rgb(205, 100,200)")
img.show()

# Прямоугольник с функциональной раскраской
for x in range(640):
    for y in range(480):
        img.putpixel((x, y), (x // 3, (x + y) // 6, y // 3))
img.save("okno.png", "PNG")
img.show()
