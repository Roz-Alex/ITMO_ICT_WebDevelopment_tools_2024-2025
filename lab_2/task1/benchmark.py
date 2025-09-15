import asyncio
import threading
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

TARGET = 1_000_000_000
NUM_TASKS = 4

def calculate_sum(start: int, end: int) -> int:
    total = 0
    for i in range(start, end):
        total += i
    return total


# THREADING
def run_threading():
    print("\n1 Запуск с использованием threading...")

    def worker(start, end, results, index):
        results[index] = calculate_sum(start, end)

    chunk_size = TARGET // NUM_TASKS
    threads = []
    results = [0] * NUM_TASKS

    start_time = time.perf_counter()

    for i in range(NUM_TASKS):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1 if i < NUM_TASKS - 1 else TARGET + 1
        thread = threading.Thread(target=worker, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    elapsed = time.perf_counter() - start_time

    print(f"Итоговая сумма: {total_sum:,}")
    print(f"время выполнения (threading): {elapsed:.2f} секунд")
    return elapsed

# MULTIPROCESSING
def run_multiprocessing():
    print("\n2 Запуск с использованием multiprocessing...")

    chunk_size = TARGET // NUM_TASKS
    tasks = []

    start_time = time.perf_counter()

    with multiprocessing.Pool(processes=NUM_TASKS) as pool:
        for i in range(NUM_TASKS):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size + 1 if i < NUM_TASKS - 1 else TARGET + 1
            tasks.append(pool.apply_async(calculate_sum, (start, end)))

        results = [task.get() for task in tasks]

    total_sum = sum(results)
    elapsed = time.perf_counter() - start_time

    print(f"Итоговая сумма: {total_sum:,}")
    print(f"Время выполнения (multiprocessing): {elapsed:.2f} секунд")
    return elapsed

# ASYNC
async def calculate_sum_async(start: int, end: int) -> int:

    total = 0
    for i in range(start, end):
        total += i
        if i % 10_000_000 == 0:
            await asyncio.sleep(0)
    return total

async def run_async():
    print("\n3 Запуск с использованием asyncio...")

    chunk_size = TARGET // NUM_TASKS
    tasks = []

    start_time = time.perf_counter()

    for i in range(NUM_TASKS):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1 if i < NUM_TASKS - 1 else TARGET + 1
        tasks.append(calculate_sum_async(start, end))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    elapsed = time.perf_counter() - start_time

    print(f"Итоговая сумма: {total_sum:,}")
    print(f"Время выполнения (asyncio): {elapsed:.2f} секунд")
    return elapsed

if __name__ == "__main__":
    print(f"sum от 1 до {TARGET:,} с разбиением на {NUM_TASKS} подзадач")

    time_threading = run_threading()
    time_multiprocessing = run_multiprocessing()
    time_async = asyncio.run(run_async())

    print("\nСРАВНЕНИЕ\n")
    print(f"threading: {time_threading:.2f} сек")
    print(f"multiprocessing: {time_multiprocessing:.2f} сек")
    print(f"asyncio: {time_async:.2f} сек")
