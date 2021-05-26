from django import template

# from recipes.models import Ingredient


register = template.Library()


@register.filter(is_safe=True)
def addclass(field, css):
    return field.as_widget(attrs={'class': css})
