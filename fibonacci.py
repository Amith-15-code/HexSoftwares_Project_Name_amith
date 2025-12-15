def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

for num in fibonacci():
    print(num, end=" ")
