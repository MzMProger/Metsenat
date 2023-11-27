import logging

from celery import shared_task
from apps.sponsors.models import Sponsor
from apps.students.models import StudentSponsor

logger = logging.getLogger("metsenat")


@shared_task
def send_students_info():
    sponsors = Sponsor.objects.all()
    for sponsor in sponsors:
        logger.info(f"Sponsor: {sponsor.full_name}")
        logger.info(StudentSponsor.objects.filter(sponsor=sponsor).values("student"))
