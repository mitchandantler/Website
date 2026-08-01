from datetime import time

from .models import OpeningHours


def opening_hours(request):
    """Makes the weekly OpeningHours queryset available in every template."""
    return {"opening_hours": OpeningHours.objects.all()}


def _format_time_label(value: time) -> str:
    hour = value.hour % 12 or 12
    period = "AM" if value.hour < 12 else "PM"
    if value.minute == 0:
        return f"{hour} {period}"
    return f"{hour}:{value.minute:02d} {period}"


def service_hours_summary(request):
    """A condensed "Mon-Sun 6:30 AM - 2 PM"-style summary for the footer,
    shown only when every day shares identical open/close hours (the
    common case for this business). Falls back to None — meaning the
    footer should render the full per-day table instead — the moment any
    day is closed or has different hours, so a real difference is never
    silently hidden behind a stale summary.
    """
    days = list(OpeningHours.objects.all())
    if not days or any(
        day.is_closed or not day.open_time or not day.close_time for day in days
    ):
        return {"service_hours_summary": None}

    first = days[0]
    if all(
        day.open_time == first.open_time and day.close_time == first.close_time
        for day in days
    ):
        summary = (
            f"Mon-Sun {_format_time_label(first.open_time)} - "
            f"{_format_time_label(first.close_time)}"
        )
        return {"service_hours_summary": summary}

    return {"service_hours_summary": None}
