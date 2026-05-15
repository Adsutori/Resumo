from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def timesince_pl(value):
    """Polska wersja timesince."""
    if not value:
        return ''

    try:
        now  = timezone.now()
        diff = now - value
    except TypeError:
        return ''

    seconds = int(diff.total_seconds())
    if seconds < 0:
        return 'przed chwilą'

    minutes = seconds // 60
    hours   = minutes // 60
    days    = diff.days
    weeks   = days   // 7
    months  = days   // 30
    years   = days   // 365

    def pl(n, singular, few, many):
        if n == 1:
            return f'{n} {singular}'
        elif 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
            return f'{n} {few}'
        else:
            return f'{n} {many}'

    if seconds < 60:
        return 'przed chwilą'
    elif minutes < 60:
        return pl(minutes, 'minutę',  'minuty',   'minut')
    elif hours < 24:
        return pl(hours,   'godzinę', 'godziny',  'godzin')
    elif days < 7:
        return pl(days,    'dzień',   'dni',      'dni')
    elif weeks < 5:
        return pl(weeks,   'tydzień', 'tygodnie', 'tygodni')
    elif months < 12:
        return pl(months,  'miesiąc', 'miesiące', 'miesięcy')
    else:
        return pl(years,   'rok',     'lata',     'lat')
