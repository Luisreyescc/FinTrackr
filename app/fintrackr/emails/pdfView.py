from django.http import JsonResponse
import threading
import time
from django.core.mail import send_mail

# Store threads and their stop events
threads = {}

# Periodic email task
def periodic_email_task(interval, stop_event, email):
    sleep_interval = 0.5  # Check the stop event every 0.5 seconds
    elapsed_time = 0

    while not stop_event.is_set():
        if elapsed_time >= interval:
            # Send an email
            try:
                send_mail(
                    subject="Hello!",
                    message="Hello, this is a periodic email!",
                    from_email=None,  # Use the default email from settings
                    recipient_list=[email],
                )
                print(f"Email sent to {email}", flush=True)
            except Exception as e:
                print(f"Error sending email to {email}: {e}", flush=True)

            elapsed_time = 0  # Reset elapsed time
        time.sleep(sleep_interval)
        elapsed_time += sleep_interval


# Start a new periodic task
def start_email_task(request):
    interval = int(request.GET.get("interval", 60))  # Default interval: 60 seconds
    email = request.GET.get("email", "default@example.com")  # Default email address

    if email in threads:
        threads[email]["stop_event"].set()
        threads[email]["thread"].join(timeout=1) 
        del threads[email]

    stop_event = threading.Event()
    thread = threading.Thread(target=periodic_email_task, args=(interval, stop_event, email))
    thread.daemon = True  # Ensures thread exits when the main program exits
    thread.start()
    threads[email] = {"thread": thread, "stop_event": stop_event}
    return JsonResponse({"message": "Periodic email task started successfully."})

# Stop a running periodic task
def stop_email_task(request):
    email = request.GET.get("email")
    if email in threads:
        threads[email]["stop_event"].set()
        threads[email]["thread"].join(timeout=1) 
        del threads[email]
        return JsonResponse({"message": "Periodic email task stopped successfully."})
    return JsonResponse({"error": "No running task found for this email."}, status=404)
