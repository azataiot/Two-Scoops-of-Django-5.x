# promos/views.py
from .models import Promo
from django.db.models import Q


def fun_function(name=None):
    """Find working ice cream promo"""
    qs = (
        Promo
        .objects
        .active()
        .filter(
            Q(name__startswith=name) |
            Q(description__icontains=name)
        )
        .exclude(status='melted')
        .select_related('flavors')
    )
    return qs
