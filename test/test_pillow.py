from PIL import Image

image = Image.open("D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\")
print(image)

image_bytes = image.tobytes()
print(image_bytes)

hash_value = hash(image_bytes)
print(hash_value)