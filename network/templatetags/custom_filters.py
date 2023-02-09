from django import template

register = template.Library()

@register.filter()
def c(value):
    return value.capitalize()


@register.filter()
def get_comments(post):
    return post.post_comments.order_by('-created').all()