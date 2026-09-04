import logging
import time
from datetime import datetime
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_booking_notifications(self, booking_id, user_email, phone_number, source, dest, fare):
    """
    Asynchronous Celery task to handle post-booking workflows:
    1. Simulates dynamic PDF e-ticket compilation/rendering.
    2. Simulates transactional email (SendGrid) and SMS (Twilio) dispatch.
    
    Returns a comprehensive status dictionary upon completion.
    """
    start_time = datetime.now()
    logger.info(
        f"[Celery Task: {self.request.id}] Notification pipeline triggered for Booking ID: {booking_id} | "
        f"Recipient: {user_email} ({phone_number}) | Route: {source} -> {dest} | Fare: ₹{fare}"
    )

    try:
        # Step 1: Simulate e-ticket PDF generation & binary compilation
        logger.info(f"[Booking {booking_id}] Compiling PDF e-ticket with QR security payload...")
        time.sleep(2)
        pdf_artifact_id = f"PDF-TKT-{booking_id}-{int(time.time())}.pdf"
        logger.info(f"[Booking {booking_id}] PDF ticket successfully generated: {pdf_artifact_id}")

        # Step 2: Simulate multi-channel delivery (SendGrid Email + Twilio SMS)
        logger.info(f"[Booking {booking_id}] Dispatching email to {user_email} and SMS to {phone_number}...")
        time.sleep(1)
        email_message_id = f"sg_msg_{int(time.time())}_{booking_id}"
        sms_sid = f"SM_{int(time.time())}_{booking_id}"
        logger.info(f"[Booking {booking_id}] Dispatched SendGrid ID: {email_message_id} | Twilio SID: {sms_sid}")

        duration_seconds = round((datetime.now() - start_time).total_seconds(), 2)
        logger.info(f"[Booking {booking_id}] Notification workflow completed in {duration_seconds}s.")

        return {
            "status": "SUCCESS",
            "task_id": self.request.id,
            "booking_id": booking_id,
            "recipient_email": user_email,
            "recipient_phone": phone_number,
            "route": f"{source} -> {dest}",
            "fare_paid": fare,
            "artifacts": {
                "pdf_filename": pdf_artifact_id,
                "email_receipt_id": email_message_id,
                "sms_sid": sms_sid,
            },
            "duration_seconds": duration_seconds,
            "completed_at": datetime.now().isoformat(),
        }

    except Exception as exc:
        logger.error(f"[Booking {booking_id}] Error in notification pipeline: {exc}", exc_info=True)
        # Retry with exponential backoff on transient network or external API errors
        raise self.retry(exc=exc)
