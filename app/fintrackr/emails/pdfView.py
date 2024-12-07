from django.http import JsonResponse
import threading
import time
    

# Store threads and their stop events
threads = {}


# Periodic task
def periodic_task(interval, stop_event):
    while not stop_event.is_set():
        print(f"Task executed", flush=True)  # Replace with actual logic
        time.sleep(interval)

# View to start the thread
def start_thread(request):
    interval = int(request.GET.get("interval", 10))  # Seconds
    task_id = request.GET.get("task_id", "default_task")  # Unique identifier for the task

    # Check if the task already exists
    if task_id in threads:
        return JsonResponse({"status": "Task already running", "task_id": task_id})

    # Create a stop event
    stop_event = threading.Event()

    # Start a new thread
    task_thread = threading.Thread(target=periodic_task, args=(interval, stop_event))
    task_thread.daemon = True
    task_thread.start()

    # Save the thread and stop event
    threads[task_id] = stop_event

    return JsonResponse({"status": "Thread started", "task_id": task_id, "interval": f"{interval} seconds"})

# View to stop the thread
def stop_thread(request):
    task_id = request.GET.get("task_id", "default_task")  # Unique identifier for the task

    # Check if the task exists
    if task_id in threads:
        # Signal the thread to stop
        threads[task_id].set()

        # Remove the task from the dictionary
        del threads[task_id]

        return JsonResponse({"status": "Thread stopped", "task_id": task_id})
    else:
        return JsonResponse({"status": "Task not found", "task_id": task_id})