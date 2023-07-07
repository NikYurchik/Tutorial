def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        s = cache.get(n)
        if s == None:
            s = 0
            if n <= 0:
                return 0
            elif n == 1:
                return 1
            else:
                s = fibonacci(n-1) + fibonacci(n-2)
                cache.update({n: s})
                print('calc = '+ str(s))
                return s
        else:
            print('cache = '+str(s))
            return s
        
    return fibonacci

fib = caching_fibonacci()
# print(2, fib(2))
# print(15, fib(15))
print(6, fib(6))
print(5, fib(5))
