import threading
import queue
import random
import time

# Shared queue to hold produced data
data_queue = queue.Queue(maxsize=10)

# Lock for synchronizing thread access to shared resources
lock = threading.Lock()

# Producer function that generates random numbers
def producer(producer_id):
    while True:
        item = random.randint(1, 100)  # Generate a random item (task)
        time.sleep(random.uniform(0.1, 1))  # Simulate work (e.g., network or I/O)
        data_queue.put(item)  # Put the item into the shared queue
        print(f"Producer-{producer_id} produced: {item}")

# Consumer function that processes the data
def consumer(consumer_id):
    while True:
        # Get item from the queue (will block until an item is available)
        item = data_queue.get()
        time.sleep(random.uniform(0.5, 2))  # Simulate work (e.g., processing time)
        print(f"Consumer-{consumer_id} consumed: {item}")
        data_queue.task_done()  # Mark the task as done

# Function to start the producer-consumer system
def start_producer_consumer_system(num_producers, num_consumers):
    producer_threads = []
    consumer_threads = []

    # Start producer threads
    for i in range(num_producers):
        producer_thread = threading.Thread(target=producer, args=(i+1,))
        producer_threads.append(producer_thread)
        producer_thread.daemon = True  # Allow thread to exit when the program ends
        producer_thread.start()

    # Start consumer threads
    for i in range(num_consumers):
        consumer_thread = threading.Thread(target=consumer, args=(i+1,))
        consumer_threads.append(consumer_thread)
        consumer_thread.daemon = True  # Allow thread to exit when the program ends
        consumer_thread.start()

    # Wait for threads to finish (This will never return because of daemon threads)
    for t in producer_threads + consumer_threads:
        t.join()

# Main driver function
if __name__ == "__main__":
    # Number of producers and consumers
    num_producers = 3
    num_consumers = 4

    print("Starting Producer-Consumer system...")
    start_producer_consumer_system(num_producers, num_consumers)
