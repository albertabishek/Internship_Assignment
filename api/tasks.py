from celery import shared_task
import time


@shared_task
def send_mock_email_task(user_email: str) -> str:
    """
    A mock background  task that simulates sending an email.
    """
    print(f"Starting to send a welcome email to {user_email}...")
    # Simulate a network-bound task
    time.sleep(8)
    print(f"Successfully sent a welcome email to{user_email}.")
    return f"Email sent to {user_email}"
