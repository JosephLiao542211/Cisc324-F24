import threading
import time
import random

# Constants for the number of writers, editors, and available review slots
NUM_WRITERS = 20  # Number of writers to simulate
NUM_EDITORS = 2  # Number of editors to simulate
NUM_SLOTS = 1  # Maximum simultaneous reviews

# Semaphore to manage available review slots
review_slots = threading.Semaphore(NUM_SLOTS)

# Lock to ensure one editor reviews an article at a time
editor_lock = threading.Lock()

# Lock to prevent overlapping print output
print_lock = threading.Lock()

# Shared variables to track the submission and review process
articles_submitted = 0  # Number of articles submitted
TOTAL_ARTICLES = NUM_WRITERS  # Total articles expected

# Event to signal that all articles are reviewed
stop_editors = threading.Event()

articles_submitted_lock = threading.Lock()

def writer_task(writer_id):
    """Simulates a writer drafting and submitting an article."""
    with print_lock:
        print(f"Writer {writer_id} is drafting an article.")

    # Simulate drafting time
    time.sleep(random.uniform(1, 2))

    with print_lock:  # console is a shared resource, so we need to lock it
        print(f"Writer {writer_id} is waiting for a review slot.")

    # TODO 1: Acquire the review slot before submission
    
    review_slots.acquire()

    with print_lock:  # console is a shared resource, so we need to lock it
        print(f"Writer {writer_id} has submitted an article for review.")



    with articles_submitted_lock:
        global articles_submitted
        articles_submitted += 1

    review_slots.release()

    # TODO 2: Safely update the shared variable `articles_submitted` tracking the number of submitted articles

    # TODO 3: Release the review slot after submission
    review_slots.release()


def editor_task(editor_id):
    """Simulates an editor reviewing articles."""
    while not stop_editors.is_set():
        # Simulate the time before checking for an article
        time.sleep(random.uniform(0.5, 1.5))

        with print_lock:  
            print(f"Editor {editor_id} is checking for an article to review.")

        editor_lock.acquire(timeout=4)
        # TODO 4: Acquire the editor lock with a timeout to avoid deadlock

        try:
            with articles_submitted_lock:
                global articles_submitted
                if  articles_submitted > 0:
                    
                    # TODO 5: Check if there are articles to review
                    with print_lock:  # console is a shared resource, so we need to lock it
                        print(f"Editor {editor_id} is reviewing an article.")
                    time.sleep(random.uniform(1, 3))  # Simulate review time

                    with print_lock:  # console is a shared resource, so we need to lock it
                        print(f"Editor {editor_id} has finished reviewing an article.")

                    # TODO 7: Safely decrement the number of submitted articles
                    articles_submitted -= 1

                    if articles_submitted == 0 and TOTAL_ARTICLES == NUM_WRITERS:
                            stop_editors.set()


                # TODO 8: Stop editors if all articles are reviewed

        finally:
            editor_lock.release()
            # TODO 9: Ensure the editor lock is released
            # TODO 10: Remove this line after adding the code

    with print_lock:
        print(f"Editor {editor_id} is stopping as all reviews are complete.")


def main():
    """Main function to initialize the simulation."""
    writer_threads = []
    for i in range(NUM_WRITERS):
        t = threading.Thread(target=writer_task, args=(i,))
        writer_threads.append(t)
        t.start()

    editor_threads = []
    for i in range(NUM_EDITORS):
        t = threading.Thread(target=editor_task, args=(i,))
        editor_threads.append(t)
        t.start()

    for t in writer_threads:
        t.join()

    for t in editor_threads:
        t.join()

    print("All articles have been submitted and reviewed.")


if __name__ == "__main__":
    main()
