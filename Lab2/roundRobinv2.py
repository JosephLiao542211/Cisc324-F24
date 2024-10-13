def round_robin_scheduling(processes, quantum):
    """This code implements round robin scheduling algorithm
    Modified by: Joseph Liao and 20366481
    """

    n = len(processes)
    rem_burst_times = [p[1] for p in processes]
    waiting_time = [0] * n
    turnaround_time = [0] * n
    t = 0  # Current time
    order = []  # To track the order of execution
    context_switches = 0
    while any(rem_burst_times[i] > 0 for i in range(n)):
        for i in range(n):
            if rem_burst_times[i] > 0:
                process_executed = False
                if rem_burst_times[i] > quantum:
                    # Execution order tracking
                    t += quantum
                    rem_burst_times[i] -= quantum
                    order.append((processes[i][0], quantum))
                    process_executed = True
                else:
                    # Appends to order list the process id and the remaining burst time
                    t += rem_burst_times[i]
                    order.append((processes[i][0], rem_burst_times[i]))
                    waiting_time[i] = t - processes[i][1]
                    rem_burst_times[i] = 0
                    process_executed = True

                if process_executed:
                    context_switches += 1 #cotext switch total count
                    print(f"Process {processes[i][0]} executed for {order[-1][1]} units")

    # Calculate turnaround time
    for i in range(n):
        turnaround_time[i] = processes[i][1] + waiting_time[i]

    # Calculate average times
    avg_waiting = sum(waiting_time) / n
    avg_turnaround = sum(turnaround_time) / n

    # Display results
    print("\nProcess ID\tBurst Time\tWaiting Time\tTurnaround Time")
    for i in range(n):
        print(f"{processes[i][0]}\t\t{processes[i][1]}\t\t{waiting_time[i]}\t\t{turnaround_time[i]}")
    print(f"\nAverage Waiting Time: {avg_waiting}")
    print(f"Average Turnaround Time: {avg_turnaround}")

    # Print execution order
    print("\nExecution Order (Process ID, Time Units):")
    for process_id, units in order:
        print(f"Process {process_id} executed for {units} units")

    # Print context switch count
    print(f"\ncontext switches: {context_switches}")


if __name__ == '__main__':
    while True:
        # Ask user for a new quantum value
        quantum = int(input("time quantum: "))

        # List of processes [process_id, burst_time]
        # Assuming same initial arrival time for all processes
        processes = [[1, 10], [2, 1], [3, 2], [4, 1], [5, 5]]
        
        round_robin_scheduling(processes, quantum)

        # Ask the user if they want to continue
        continue_choice = input("\ndifferent quantum? (Y): ").upper()
        if continue_choice != 'Y':
            break
