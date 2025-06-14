import time

def timer(func):
    def wrapper(*args):
        t1 = time.time()
        func(*args)
        t2 = time.time() - t1
        print(f"Function {func.__name__} took {t2} seconds")
    return wrapper
