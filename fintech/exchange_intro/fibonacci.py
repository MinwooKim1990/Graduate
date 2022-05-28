# Fibonacci using variables only
fib0 = 0
fib1 = 1
fib2 = fib1 + fib0
fib3 = fib2 + fib1
fib4 = fib3 + fib2
fib5 = fib4 + fib3
fib6 = fib5 + fib4

print(fib6)


# Fibonacci using a list and a while-loop
fib = [0, 1]
while len(fib) < 7:
    fib_1st_prev = fib[-1]
    fib_2nd_prev = fib[-2]
    fib.append(fib_1st_prev + fib_2nd_prev)

print(fib, fib[6])


# Fibonacci using a recurring function
def fibf(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    return fibf(n - 1) + fibf(n - 2)

print(fibf(6))
