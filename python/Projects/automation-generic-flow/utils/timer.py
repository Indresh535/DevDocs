 # Timer for tracking page load times

from contextlib import contextmanager
import time

class Timer:
    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        return self.end_time - self.start_time
    
    
    @contextmanager
    def measure_time():
        start_time = time.time()
        yield  # No value is yielded here
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Elapsed time: {total_time:.2f} seconds")
        return total_time  # Yield the total_time value
