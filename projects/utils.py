def activity_todays_feed(activity):
    day_total_live = getattr(activity, 'day_total_live', 0)
    total_weight = day_total_live * activity.single_fish_weight
    return round(total_weight * activity.feed_percentage / 100, 4)


def calculate_feed_n(activity):
    todays_feed = activity_todays_feed(activity)
    undigested_percentage = activity.project.undigested_percentage
    value = float(todays_feed) * 0.90 * float(undigested_percentage / 100) * float(
        activity.feed_protein_percentage / 100) * 0.16
    return round(value, 10)


def calculate_feed_c(activity):
    todays_feed = activity_todays_feed(activity)
    undigested_percentage = activity.project.undigested_percentage
    value = float(todays_feed) * 0.90 * float(undigested_percentage / 100) * 0.5
    return round(value, 10)


def calculate_molas_to_add(activity):
    feed_n = calculate_feed_n(activity)
    feed_c = calculate_feed_c(activity)
    value = (float(feed_n * float(activity.expected_cn)) - float(feed_c)) / 0.28
    return round(value, 2)
