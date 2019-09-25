from django import template
from django.template.defaultfilters import stringfilter
import re
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


register = template.Library()


@register.filter()
def class_name(value):
    return value.__class__.__name__

@register.filter()
def notification_class_name(value):
    model = None
    if value.action_object_content_type == None:
        model = 'profile'
    else:
        model = value.action_object_content_type.model
    return model

@register.filter()
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]


upto.is_safe = True


def create_hashtag_link(tag):
    url = "/hashtag/{}/".format(tag)
    return '<a href="{}">#{}</a>'.format(url, tag)

@register.filter()
def hashtag_links(value):
    return mark_safe(
        re.sub(r"#(\w+)", lambda m: create_hashtag_link(m.group(1)),
               (value)))

def create_mention_link(mention):
    user_name = mention.replace('@','')
    try:
        if User.objects.get(username__iexact=user_name):
                link = "/mention/{}/".format(user_name)
                return '<a href="{}">{}</a>'.format(link, mention)
    except User.DoesNotExist:
        return mention
#     link = "/mention/{}/".format(user_name)
#     return '<a href="{}">{}</a>'.format(link, mention)

@register.filter()
def mention_link(value):
    return mark_safe(
        re.sub(r"@(\w+)", lambda x: create_mention_link(x.group(0)),
               (value)))

@register.filter
def so_bracket(value):
    return value.replace("[","")

@register.filter
def sc_bracket(value):
        return value.replace("]","")

@register.filter
def colon(value):
        return value.replace("'","")