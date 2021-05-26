from django import template


register = template.Library()


@register.filter(is_safe=True)
def addclass(field, css):
    return field.as_widget(attrs={'class': css})
