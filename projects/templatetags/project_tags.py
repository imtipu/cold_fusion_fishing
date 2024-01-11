from django import template
from django.conf import settings
from django.template import Context
from django.utils.safestring import mark_safe

from projects.utils import calculate_feed_n, calculate_feed_c

register = template.Library()


@register.simple_tag
def day_total_live(activity):
    if getattr(activity, 'day_total_live', None):
        return activity.day_total_live
    return 0


@register.filter(name='day_total_weight')
def day_total_weight(activity):
    day_total_live = getattr(activity, 'day_total_live', 0)
    total_weight = day_total_live * activity.single_fish_weight
    return total_weight


@register.filter(name='activity_todays_feed')
def activity_todays_feed(activity):
    day_total_live = getattr(activity, 'day_total_live', 0)
    total_weight = day_total_live * activity.single_fish_weight
    return round(total_weight * activity.feed_percentage / 100, 4)


@register.filter(name='activity_feed_n')
def activity_feed_n(activity):
    undigested_percentage = activity.project.undigested_percentage
    value = float(activity.todays_feed) * 0.90 * float(undigested_percentage / 100) * float(
        activity.feed_protein_percentage / 100) * 0.16
    return round(value, 10)


@register.filter(name='activity_molas_to_add')
def activity_molas_to_add(activity):
    feed_n = calculate_feed_n(activity)
    feed_c = calculate_feed_c(activity)
    value = (float(feed_n * float(activity.expected_cn)) - float(feed_c)) / 0.28
    return round(value, 2)
