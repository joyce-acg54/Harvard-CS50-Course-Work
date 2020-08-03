from cs50 import get_float
from math import floor

while True:
    f = get_float("Change owed:")
    if f > 0:
        break

c = round(f * 100)


while c > 0:

    # how many quarters
    q = floor(c / 25)
    c = c % 25

    # how many dimes
    d = floor(c / 10)
    c = c % 10

    # how many nickels
    n = floor(c / 5)
    c = c % 5

    # how many pennies
    p = floor(c / 1)
    c = c % 1

    break

print(q + d + n + p)

