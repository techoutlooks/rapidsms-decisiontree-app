from django import template

from decisiontree.multitenancy.utils import tenancy_reverse


register = template.Library()


@register.filter
def mean(values):
    try:
        integers = [int(v) for v in values]
    except (TypeError, ValueError):
        return 'n/a'
    return sum(integers)/len(integers)*1.0


@register.filter
def median(values):
    try:
        values = [int(v) for v in values]
    except (TypeError, ValueError):
        pass
    values = sorted(values)
    size = len(values)
    try:
        if size % 2 == 1:
            return values[(size - 1) / 2]
        else:
            values = [int(v) for v in values]
            return (values[size/2 - 1] + values[size/2]) / 2
    except (TypeError, ValueError):
        return 'n/a'


@register.filter
def mode(values):
    copy = sorted(values)
    counts = {}
    for x in set(copy):
        count = copy.count(x)
        if count not in counts:
            counts[count] = []
        counts[count].append(x)
    return counts[max(counts.keys())]


@register.simple_tag(takes_context=True)
@register.assignment_tag(takes_context=True, name='assign_tenancy_url')
def tenancy_url(context, url_name, *args, **kwargs):
    return tenancy_reverse(context['request'], url_name, *args, **kwargs)


@register.filter
def verbose_name(model):
    """Workaround for Django disallowing access to _meta attribute."""
    return model._meta.verbose_name


@register.filter
def verbose_name_plural(model):
    """Workaround for Django disallowing access to _meta attribute."""
    return model._meta.verbose_name_plural
