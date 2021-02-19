import os


def calc_tap_segments():
    d = int(input("Введите диаметр голой трубы"))
    b = int(input("Введите толщину изоляции"))
    neck = int(input("Введите размер шейки"))
    back = int(input("Введите размер затылка"))
    L = int(input("Введите длину окружности по металлу"))
    count = int(input("Введите число сегментов"))
    my_count = count
    if back < 630:
        my_count = 5
    elif back < 1230:
        my_count = 7
    elif back < 2050:
        my_count = 9
    elif back < 3050:
        my_count = 11
    else:
        print("Слишком огромный отвод, сочувствую....")

    h = (back - neck) / (2 * my_count - 2)
    min_neck = neck / my_count
    max_back = min_neck + h
    radius = L / 6.28
    f = open("tmp.txt")
    f.write("высота h = " + str(h))
    f.write("шейка рыбки = " + str(min_neck))
    f.write("затылок рыбки = " + str(max_back))
    f.write("Радиус окружности = " + str(radius))
    f.close()
    os.startfile("tmp.txt", "print")
    os.remove("tmp.txt")
    return
