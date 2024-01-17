from django import template
from django.conf import settings

register = template.Library()


@register.filter('field_label')
def field_label(field, classes=''):
    """
    Returns the label of a form field.
    """
    return field.label_tag(attrs={'class': classes})


@register.filter('field_input')
def field_input(field, classes=''):
    field_type = field.field.widget.__class__.__name__.lower()
    # print(field_type)
    # default_class = ('text-gray-700 dark:text-gray-400 dark:bg-gray-800 dark:border-gray-600 border-gray-300'
    #                  ' focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 '
    #                  'shadow-sm')
    if field_type == 'select':
        classes += ' select'
    elif field_type == 'textarea':
        classes += ' textarea'
    elif field_type == 'textinput':
        classes += ' input'
    elif field_type == 'select':
        classes += ' select'
    updated_field = field.as_widget(attrs={'class': classes})
    return updated_field
