from django.shortcuts import get_object_or_404, redirect

from ..models import ShortUrl


def redirect_short_url(request, short_code):
    short_url = get_object_or_404(ShortUrl, short_code__iexact=short_code)
    return redirect(short_url.target_url)
