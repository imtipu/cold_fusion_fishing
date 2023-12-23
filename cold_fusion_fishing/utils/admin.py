from django.template.loader import render_to_string
from django.utils.html import format_html


def html_image_logo():
    html = render_to_string('admin/html_admin_logo.html')
    return format_html(html)
