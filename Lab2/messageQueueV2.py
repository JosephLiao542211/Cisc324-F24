from multiprocessing import Process, Queue
import time

"""
This program demonstrates a simple IPC via message queue with multiple child processes.
Student Last name and ID:  Joseph Liao and 20366481
"""

def childProcess(q, num_messages, child_id):
    # Each child process sends multiple messages
    for i in range(num_messages):
        message = f"Message {i+1} from child {child_id}"
        q.put(message)
        time.sleep(0.1)  # Simulate some work

def parentProcess(num_children, messages_per_child):
    # Create a message queue to hold the messages
    q = Queue()

    # Create and start multiple child processes
    processes = []
    for i in range(num_children):
        p = Process(target=childProcess, args=(q, messages_per_child, i+1))
        processes.append(p)
        p.start()

    # Collect messages from all child processes
    total_messages = num_children * messages_per_child
    for _ in range(total_messages):
        print("Received from child:", q.get())

 
    for p in processes:
        p.join()

if __name__ == '__main__':
    # NOTE: Print your name and ID
    print("Hi, this is Joseph Liao and 20366481")

   
    num_children = 3
    messages_per_child = 2

    # Call the parent process with the specified number of children and messages
    parentProcess(num_children, messages_per_child)
