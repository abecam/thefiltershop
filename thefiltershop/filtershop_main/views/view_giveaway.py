from django.shortcuts import render, redirect
from django.utils import timezone

from ..models import Videogame_common, Studio, Publisher, EmailForGiveAway
from django.db.models import Count, Q


def giveaway(request):
    """Display three random artisan games with no negative filters and
    allow the visitor to register an email for the daily Steam key giveaway.

    The email is stored in a cookie with a one‑month expiration. Submitting
    the form when the cookie already exists simply refreshes the expiry and
    re‑records the address for today's entry.
    """
    # pick up to three random artisan games that have zero negative filters
    qs = (
        Videogame_common.objects
        .annotate(number_of_filters=Count('valueforfilter', filter=Q(valueforfilter__filter__is_positive=False)))
        .filter(
            studios__size_of_studio=Studio.SizeInPersons.ARTISAN,
            publishers__size_of_publisher=Publisher.SizeInPersons.ARTISAN,
            number_of_filters=0,
        )
        .distinct()
    )
    games = list(qs.order_by('?')[:3])

    email_cookie = request.COOKIES.get('giveaway_email')
    today = timezone.now().date()
    message = ''
    already_participated_today = False
    has_expired_cookie = False  # cookie exists but from a previous day

    if request.method == 'POST':
        # prefer the posted email, fall back to cookie if the field is empty
        email = request.POST.get('email') or email_cookie
        if email:
            # store/refresh the cookie and record today's entry
            response = redirect('filtershop_games:giveaway')
            response.set_cookie('giveaway_email', email, max_age=30 * 24 * 60 * 60)
            entry, created = EmailForGiveAway.objects.get_or_create(
                current_day=today,
                defaults={'email': email},
            )
            if not created and entry.email != email:
                entry.email = email
                entry.save(update_fields=['email'])
            # a small message will be shown after redirection
            request.session['giveaway_message'] = 'Thanks for participating today!'
            return response
        else:
            message = 'Please provide a valid email address.'
    else:
        # GET request: check if already participated today
        if email_cookie:
            try:
                entry = EmailForGiveAway.objects.get(email=email_cookie, current_day=today)
                already_participated_today = True
            except EmailForGiveAway.DoesNotExist:
                # cookie exists but no entry for today, so the day has changed
                has_expired_cookie = True

    # if we were redirected after form submission, a message may exist
    message = message or request.session.pop('giveaway_message', '')

    context = {
        'games': games,
        'email_cookie': email_cookie,
        'message': message,
        'already_participated_today': already_participated_today,
        'has_expired_cookie': has_expired_cookie,
    }
    return render(request, 'thefiltershop/giveaway.html', context)


def check_if_counter_reset() :
    today = datetime.now(timezone.utc).date()
    # giveaway_day, created = GiveawayDay.objects.get_or_create(current_day=today)
    # if created :
    #     # New day, reset the counter and select a new random number between min and max views for giveaway
    #     giveaway_day.page_counter = random.randint(100, 1000)
    #     giveaway_day.was_awarded = False
    #     giveaway_day.save(update_fields=['page_counter', 'was_awarded'])

def check_if_winner(request) :
    today = datetime.now(timezone.utc).date()
    # giveaway_day = GiveawayDay.objects.get(current_day=today)
    # if not giveaway_day.was_awarded :
    #     if giveaway_day.page_counter <= 0 :
    #         # We have a winner, but we need to check if the cookie is already set for this user, to avoid giving multiple times the game to the same user
    #         if not request.COOKIES.get('giveaway_winner') :
    #             # Give the game and set the cookie
    #             steam_key_to_give = SteamKey.objects.filter(is_used=False).first()
    #             if steam_key_to_give != None :
    #                 steam_key_to_give.is_used = True
    #                 steam_key_to_give.awarded_to_hash = str(random.getrandbits(128))
    #                 steam_key_to_give.awarded_at = datetime.now(timezone.utc)
    #                 steam_key_to_give.save(update_fields=['is_used', 'awarded_to_hash', 'awarded_at'])
    #                 giveaway_day.was_awarded = True
    #                 giveaway_day.save(update_fields=['was_awarded'])
    #                 # Set the cookie with the hash of the awarded key, to prevent giving multiple times to the same user
    #                 request.session['giveaway_winner'] = steam_key_to_give.awarded_to_hash

    #                 return True
    #     else :
    #         # Increment the counter
    #         giveaway_day.page_counter -= 1
    #         giveaway_day.save(update_fields=['page_counter'])
    # return False
