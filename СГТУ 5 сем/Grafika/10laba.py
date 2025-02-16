from PIL import Image

image = Image.open("222.jpg")


result_image = Image.new("RGB", image.size)

for x in range(image.width):
    for y in range(image.height):
        r, g, b = image.getpixel((x, y))
        result_image.putpixel((x, y), (b, g, r))

result_image.show()




channels = image.split()

for channel in channels:
    channel.show()

reconstructed_image = Image.merge("RGB", channels)
reconstructed_image.show()

new_image = Image.merge("RGB", (channels[0], channels[1], channels[2]))
new_image.show()




"""
print(image.mode)
print(image.size)
histogram = image.histogram()
import matplotlib.pyplot as plt
plt.bar(range(len(histogram)), histogram)
plt.show()
"""



img2 = image.copy()
img2.show()
img2.thumbnail((100,100))
img2.show()





box = image.crop([0,0,100,100])
new_image = Image.new("RGB", (100, 100))
new_image.paste(box)
new_image.show()




img = Image.open("111.jpg")
img2 = img.rotate(90) 
img2.show() 

img3 = img.rotate(45, Image.NEAREST) 
img3.show()
img4 = img.rotate(45, expand=True) 
img4.show()
