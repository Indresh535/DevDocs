import threading
import time

# Define a function to be run by each thread
def print_numbers():
    for i in range(5):
        time.sleep(1)  # Simulate a delay (like I/O operation)
        print(f"Number: {i}")

def print_letters():
    for letter in "abcde":
        time.sleep(1.5)  # Simulate a delay
        print(f"Letter: {letter}")

# Create threads
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Start threads
thread1.start()
thread2.start()

# Wait for threads to finish
thread1.join()
thread2.join()

print("All threads have finished.")
