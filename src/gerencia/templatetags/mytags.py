from django import template

register = template.Library()

@register.filter
def checktype(obj):
	return obj#.__class__.__name__
@register.filter
def replace(value,cherche,replacement):
	return value.replace(cherche,replacement)
