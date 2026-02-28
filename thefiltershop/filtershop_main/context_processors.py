from django.utils import timezone
from .models import EmailForGiveAway


def giveaway_context(request):
    """Add giveaway participation status to template context."""
    email_cookie = request.COOKIES.get('giveaway_email')
    already_participated_today = False

    if email_cookie:
        today = timezone.now().date()
        already_participated_today = EmailForGiveAway.objects.filter(
            email=email_cookie, current_day=today
        ).exists()

    return {
        'giveaway_already_participated_today': already_participated_today,
    }
