import random
import time
import os
import json
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Queue, Pool

def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]

def process_number(number):
    if number % 2 == 0:
        return True
    return False

def process_with_thread_pool(data):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(process_number, data))

def process_with_pool(data):
    num_cores = os.cpu_count()
    with Pool(processes=num_cores) as pool:
        return pool.map(process_number, data)
    
def process_num_with_queue(input_queue, output_queue):
    while True:
        try:
            number = input_queue.get_nowait() 
            result = process_number(number)
            output_queue.put(result)
        except Exception:
            break

def process_with_queue(data):
    output_queue = Queue()
    p = Process(target=process_num_with_queue, args=(data, output_queue))
    p.start()
    p.join()

    results = []
    while not output_queue.empty():
        results.append(output_queue.get())

    return results

if __name__ == '__main__':
    n = 10_000_000
    data = generate_data(n)

    # Однопоточное выполнение
    start_time = time.time()
    results_single = [process_number(num) for num in data]
    end_time = time.time()
    time_single = end_time - start_time
    print(f"Время выполнения однопоточного: {time_single:.6f} секунд")

    # Вариант А: Пул потоков
    start_time = time.time()
    results_a = process_with_thread_pool(data)
    end_time = time.time()
    time_a = end_time - start_time
    print(f"Время выполнения способа А (Пул потоков): {time_a:.6f} секунд")

    # Вариант Б: Пул процессов
    start_time = time.time()
    results_b = process_with_pool(data)
    end_time = time.time()
    time_b = end_time - start_time
    print(f"Время выполнения способа Б (Пул процессов): {time_b:.6f} секунд")

    # Вариант В: Отдельный процесс с очередью
    start_time = time.time()
    results_v = process_with_queue(data)
    end_time = time.time()
    time_c = end_time - start_time
    print(f"Время выполнения способа В (Отдельный процесс с очередью): {time_c:.6f} секунд")

    results = {
        "results_single": results_single,
        "results_a": results_a,
        "results_b": results_b,
        "results_v": results_v,
    }
    with open('./results.json', 'w') as f:
        json.dump(results, f)