from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PromotionQuerySet(models.QuerySet):
    def currently_active(self) -> "PromotionQuerySet":
        today = timezone.localdate()
        return (
            self.filter(is_active=True)
            .filter(models.Q(start_date__isnull=True) | models.Q(start_date__lte=today))
            .filter(models.Q(end_date__isnull=True) | models.Q(end_date__gte=today))
        )


class Promotion(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="promotions/", blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PromotionQuerySet.as_manager()

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"

    def __str__(self) -> str:
        return self.title

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(
                {"end_date": "End date must be on or after the start date."}
            )

    @property
    def is_currently_active(self) -> bool:
        if not self.is_active:
            return False
        today = timezone.localdate()
        if self.start_date and self.start_date > today:
            return False
        if self.end_date and self.end_date < today:
            return False
        return True
