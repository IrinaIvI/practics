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
        return number
    return None

def process_number_with_queue(input_queue, output_queue):
    while True:
        try:
            number = input_queue.get(timeout=1)
            result = process_number(number)
            output_queue.put(result)
        except:
            break 

if __name__ == '__main__':
    num_cores = os.cpu_count()
    n = 500
    list_of_num = generate_data(n)

    # Вариант А: Пул потоков
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        results_a = list(executor.map(process_number, list_of_num))
    end_time = time.time()
    print(f"Время выполнения способа А (Пул потоков): {end_time - start_time:.6f} секунд")

    # Вариант Б: Пул процессов
    start_time = time.time()
    with Pool(processes=num_cores) as pool:
        results_b = pool.map(process_number, list_of_num)
    end_time = time.time()
    print(f"Время выполнения способа Б (Пул процессов): {end_time - start_time:.6f} секунд")

    # Однопоточное выполнение
    start_time = time.time()
    results_single = []
    for i in list_of_num:
        results_single.append(process_number(i))
    end_time = time.time()
    print(f"Время выполнения способа однопоточного: {end_time - start_time:.6f} секунд")

    # Вариант В: Отдельные процессы с очередью
    input_queue = Queue()
    output_queue = Queue()

    for number in list_of_num:
        input_queue.put(number)

    processes = []
    start_time = time.time()
    for _ in range(num_cores):
        p = Process(target=process_number_with_queue, args=(input_queue, output_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results_v = []
    while not output_queue.empty():
        results_v.append(output_queue.get())

    end_time = time.time()
    total_time_v = end_time - start_time
    print(f"Время выполнения способа В (Отдельные процессы с очередью): {total_time_v:.6f} секунд")

    with open('./results.json', 'w') as f:
        json.dump({
            "results_a": results_a,
            "results_b": results_b,
            "results_single": results_single,
            "results_v": results_v,
        }, f)

