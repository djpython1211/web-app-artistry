from django import template
from app.models import *
 

register = template.Library()

@register.filter(name="split")
def split(value,key):
    return value.split(key)

