from django import template
import random


register = template.Library()

@register.filter(name='random_entry')
def random_entry(entries):
    return random.choice(entries)