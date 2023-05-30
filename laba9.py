import csv
import os
from PIL import Image

def z1():
    folder = 'D:\Python\lab9\p'

    if not os.path.exists("D:\Python\lab9\ 2"):
        os.mkdir("D:\Python\lab9\ 2")

    for j in os.listdir(folder):
        if j.endswith('.jpg') or j.endswith('.png'):
            img = Image.open(os.path.join(folder,j))
            img = img.resize((500, 500))
            img.save(os.path.join("D:\Python\lab9\ 2", j))
def z2():
    with open("data.csv") as file:
        text = csv.reader(file, delimiter = ",")
        s = 0
        print("Нужно купить")

        for row in text:
            print(f'{row[0]} - {row[1]} шт. за {row[2]} руб.')
            s = s + (int(row[1]) * int(row[2]))
        print(f'Итоговая сумма: {s} руб.')

z2()