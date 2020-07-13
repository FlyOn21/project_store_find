from functools import wraps
from timeit import default_timer as timer

def log_decorator(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        s = timer()
        print(f'Start func {func}')
        func(*args,**kwargs)
        f  = timer()
        print(f'Finish func {func}, time {s-f}')
    return wrap()

