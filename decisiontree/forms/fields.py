from django.forms import CharField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ..models import Tag
from ..utils import parse_tags
from .widgets import TagWidget


class TagField(CharField):
    widget = TagWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', 'Tags with spaces must be quoted, for '
                          'example: apple "ball cat" dog, will '
                          'result in "apple", "ball cat", and "dog" tags')
        super(TagField, self).__init__(*args, **kwargs)

    def clean(self, value):
        try:
            tag_names = parse_tags(value)
        except ValueError:
            raise ValidationError(_("Please provide a comma-separated list of tags."))
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        return tags
