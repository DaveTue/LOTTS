import random
import time
import threading
import queue

class Ex_Pattern:
    PATTERNS = ['FIFO', 'LIFO', 'PQ', 'LVQ', 'BPQ', 'BoC', 'LVoC']

    def __init__(self, type='FIFO', priority_guards: list = []) -> None:
        self.type = type
        self.priority_guards = priority_guards
        self.piority_vals = [i for i in range(1, len(self.priority_guards) + 2)]
        self.prio_LP = 0
        self.batchData = []
        self.exchReady = threading.Event()
        self.exchReady.set()  # Initially, transfer is enabled
        self.queue = self._create_queue(type)
        self.state = 'inactive'

    def _create_queue(self, type):
        if type not in self.PATTERNS:
            raise ValueError('Choose a valid pattern. Valid patterns: FIFO, LIFO, PQ (priority queue), LVQ (Last Value queue), BPQ (batch process Queue), BoC (Batch on Completion), LVoC (Last Value on Completion)')
        
        if type == 'FIFO':
            return queue.Queue()
        elif type == 'LIFO':
            return queue.LifoQueue()
        elif type == 'PQ':
            return queue.PriorityQueue()
        elif type == 'LVQ' or type == 'LVoC':
            return queue.LifoQueue()
        elif type == 'BPQ' or type == 'BoC':
            return queue.Queue()
        else:
            return queue.Queue()

    def __str__(self) -> str:
        return f'Queue type {self.type} with size {self.size()}.'

    def size(self) -> int:
        return self.queue.qsize()

    def PQ_token_gen(self, token: any = 0, last_pos: int = 5) -> tuple:
        index = 0
        priority = self.piority_vals[-1]
        for guard in self.priority_guards:
            if guard.evaluation():
                priority = self.piority_vals[index]
                break
            index += 1
        position = last_pos + 1
        return (priority, position, token)

    def get_last_item_and_clear(self):
        last_item = None
        while not self.queue.empty():
            last_item = self.queue.get()
        return last_item

    def push_thread(self, token) -> None:
        q_thread = threading.Thread(target=self.push, args=(token,), daemon=True)
        q_thread.start()

    def push(self, token: any = 1) -> None:
        self.exchReady.wait()  # Block if exchange is not ready
        if self.type == 'PQ':
            position = self.prio_LP
            token = self.PQ_token_gen(token, position)
            self.prio_LP = token[1]
            self.queue.put(token)
            self.state = 'active'
        elif self.type == 'LVQ':
            if self.size() > 0:
                self.queue.get()
            self.queue.put(token)
            self.state = 'active'
        elif self.type == 'BPQ':
            self.batchData.append(token)
            self.state = 'active'
        elif self.type == 'BoC' or self.type == 'LVoC':
            self.queue.put(token)  # Push directly to the queue
            self.state = 'waiting'
        else:
            self.queue.put(token)
            self.state = 'active'

    def enableTransfer(self):
        self.exchReady.set()

    def disableTransfer(self):
        self.exchReady.clear()

    def pull(self) -> any:
        if self.type == 'LVQ':
            val = self.queue.get()
            self.queue.put(val)
            self.state = 'waiting'
        elif self.type == 'LVoC':
            val = self.get_last_item_and_clear()  # Retrieve and clear the queue
            self.state = 'inactive'
        elif self.type == 'BoC':
            val = self.queue.get()
            self.state = 'inactive'
        elif self.type == 'PQ':
            val = self.queue.get()[2]
            self.state = 'active'
        elif self.type == 'BPQ':
            self.queue.put(self.batchData)
            self.batchData = []
            val = self.queue.get()
            self.state = 'active'
        else:
            val = self.queue.get()
            self.state = 'active'

        return val

# Function to push items to the queue
def push_items(queue_instance, items):
    for item in items:
        queue_instance.push_thread(token=item)
        print(f"Pushed item: {item}")

# Function to pull items from the queue and store them in a variable
def pull_last_item(queue_instance, result_list):
    while queue_instance.size() > 0:
        item = queue_instance.pull()
        result_list.append(item)
        print(f"Pulled item: {item}")

# Example usage
if __name__ == "__main__":
    q = Ex_Pattern(type='LVoC')

    # Generate random items
    items = [random.randint(0, 10) for _ in range(5)]
    print("Generated items:", items)

    # Start pushing items to the queue in a separate thread
    push_thread = threading.Thread(target=push_items, args=(q, items))
    push_thread.start()

    # Ensure the push thread completes before disabling transfer
    push_thread.join()
    print("Finished pushing items.")

    # Disable transfer
    q.disableTransfer()
    print("Transfer disabled.")

    # List to store pulled items
    var = []

    # Wait for a few seconds before enabling transfer
    time.sleep(2)
    q.enableTransfer()
    print("Transfer enabled.")

    # Start pulling the items from the queue in a separate thread and store them in 'var'
    pull_thread = threading.Thread(target=pull_last_item, args=(q, var))
    pull_thread.start()

    # Ensure all threads complete
    pull_thread.join()

    # Print the final result stored in 'var'
    print("Final pulled items:", var)
