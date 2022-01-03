def generation_number():
    """
    Генерация числа
    """
    s = 0
    while True:
        yield s
        s += 1
