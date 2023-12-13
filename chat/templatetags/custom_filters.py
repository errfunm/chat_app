from django import template

register = template.Library()

@register.filter
def get_other_user(chat, user):
    return chat.get_other_user(user)
