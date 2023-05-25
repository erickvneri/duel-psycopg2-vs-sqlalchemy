import tracemalloc
import time


def trace_exec_time(func):
    start = time.time()
    func()
    end = time.time() - start
    print(f"time: {end}")


def trace_mem_allocated(func):
    tracemalloc.start()
    before = tracemalloc.get_traced_memory()
    func()
    after = tracemalloc.get_traced_memory()
    usage = after[0] - before[0]

    print(f"memory allocated: {usage}")
