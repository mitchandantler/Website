from django.db import models


class OpeningHours(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    day_of_week = models.PositiveSmallIntegerField(
        choices=Weekday.choices, unique=True
    )
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(
        default=False,
        help_text=(
            "Overrides Open/Close times below — check this to show "
            "'Closed' on the website for this day, even if times are set."
        ),
    )

    class Meta:
        ordering = ["day_of_week"]
        verbose_name = "Opening Hours"
        verbose_name_plural = "Opening Hours"

    def __str__(self) -> str:
        return self.get_day_of_week_display()

    @property
    def day_name(self) -> str:
        return self.get_day_of_week_display()


class SpecialHoursOverride(models.Model):
    """One-off overrides (public holidays, special events) for a specific date."""

    date = models.DateField(unique=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["date"]
        verbose_name = "Special Hours Override"
        verbose_name_plural = "Special Hours Overrides"

    def __str__(self) -> str:
        status = "Closed" if self.is_closed else "Open"
        return f"{self.date} ({status})"


class ContactSubmission(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self) -> str:
        return f"{self.name} ({self.submitted_at:%Y-%m-%d})"
