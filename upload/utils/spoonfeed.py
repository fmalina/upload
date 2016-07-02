def spoonfeed(qs, func, chunk=1000, start=0):
    """ Chunk up a large queryset and run func on each item.

    Works with automatic primary key fields.

    chunk -- how many objects to take on at once
    start -- PK to start from

    >>> spoonfeed(Spam.objects.all(), nom_nom)
    """
    while start < qs.order_by('pk').last().pk:
        for o in qs.filter(pk__gt=start, pk__lte=start+chunk):
            func(o)
        start += chunk
