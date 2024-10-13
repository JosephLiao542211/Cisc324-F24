from multiprocessing import Process, Queue
import time

"""
This program demonstrates a simple IPC via message queue.
Student Last name and ID:  
"""
def childProcess(q):
    # A Child process puts a message in the message queue, q
    q.put("Msg from the child process!")

def parentProcess():
    # Creating a message queue to hold the message
    q = Queue()

    # Now create a child process and start that process
    p_child = Process(target=childProcess, args=(q,))
    p_child.start()

    # Get a message from the message queue
    print("Received from child:", q.get())

    # Wait for the child process to finish
    p_child.join()

if __name__ == '__main__':
    #NOTE: Print your name and ID
    print("Hi, this is <Put your name and ID>")
    parentProcess()
