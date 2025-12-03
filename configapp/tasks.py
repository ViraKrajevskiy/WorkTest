from celery import shared_task
import time
import logging
from django.db import transaction
from .models import Payout

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_payout_task(self, payout_id: str):
    try:
        payout = Payout.objects.get(id=payout_id)
    except Payout.DoesNotExist:
        logger.error("Payout not found: %s", payout_id)
        return {'status': 'not_found'}

    # Простейшее переключение статусов
    with transaction.atomic():
        payout.status = Payout.Status.PROCESSING
        payout.save(update_fields=['status', 'updated_at'])

    logger.info("Processing payout %s", payout_id)

    time.sleep(2)

    try:
        if payout.amount > 10000:
            payout.status = Payout.Status.FAILED
            reason = 'amount_exceeds_limit'
        else:
            payout.status = Payout.Status.COMPLETED
            reason = 'ok'
        with transaction.atomic():
            payout.save(update_fields=['status', 'updated_at'])
        logger.info("Finished processing %s -> %s (%s)", payout_id, payout.status, reason)
        return {'status': payout.status, 'reason': reason}
    except Exception as e:
        logger.exception("Error processing payout %s", payout_id)
        with transaction.atomic():
            payout.status = Payout.Status.FAILED
            payout.save(update_fields=['status', 'updated_at'])
        raise self.retry(exc=e, countdown=10, max_retries=3)
