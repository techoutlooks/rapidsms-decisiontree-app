from django import template
from django.core.urlresolvers import reverse


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


@register.inclusion_tag("tree/partials/tree.html")
def render_tree(tree):
    return {"tree": tree}


@register.inclusion_tag("tree/partials/question.html")
def render_question(question):
    return {"question": question}


@register.inclusion_tag("tree/partials/state.html")
def render_state(state):
    return {"state": state}


@register.simple_tag(takes_context=True)
@register.assignment_tag(takes_context=True, name='assign_tenancy_url')
def tenancy_url(context, url_name, *args, **kwargs):
    if args and kwargs:
        # Emulate error raised by regular {% url %} tag.
        raise ValueError("Don't mix *args and **kwargs in call to reverse!")
    from decisiontree.multitenancy.utils import multitenancy_enabled
    if multitenancy_enabled():
        group_slug = context['request'].group_slug
        tenant_slug = context['request'].tenant_slug
        if args:
            args = (group_slug, tenant_slug) + args
        else:
            kwargs.setdefault('group_slug', group_slug)
            kwargs.setdefault('tenant_slug', tenant_slug)
    return reverse(url_name, args=args, kwargs=kwargs)
