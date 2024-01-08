from django import template
from django.conf import settings
from django.template import Context
from django.forms import boundfield
from crispy_forms.exceptions import CrispyError
from crispy_forms.utils import TEMPLATE_PACK, flatatt
from django.template.loader import get_template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="crispy_form_field")
def crispy_form_field(field, label_class="", field_class=""):
    if not isinstance(field, boundfield.BoundField) and settings.DEBUG:
        raise CrispyError("|crispy_form_field got passed an invalid or inexistent field")

    attributes = {
        "field": field,
        "form_show_errors": True,
        "form_show_labels": False,
        "label_class": label_class,
        "field_class": field_class,
    }
    helper = getattr(field.form, "helper", None)

    template_path = None
    if helper is not None:
        attributes.update(helper.get_attributes(TEMPLATE_PACK))
        template_path = helper.field_template
    if not template_path:
        template_path = "%s/field.html" % TEMPLATE_PACK

    html_template = get_template(template_path)

    c = Context(attributes).flatten()
    return html_template.render(c)


@register.filter(name="label_with_classes", is_safe=True)
def label_with_classes(field, label_class, label_suffix=""):
    if field.field.required:
        label_suffix += '*'
    label_tag = field.label_tag(attrs={"class": label_class}, label_suffix=label_suffix)
    return mark_safe(label_tag)
