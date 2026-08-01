from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class HomePageContent(models.Model):
    """Singleton editable copy for the Home page hero — same pattern as
    apps.common.models.SiteSetting (always saves to/loads from pk=1)."""

    hero_heading = models.CharField(
        max_length=200,
        default="Great coffee, honest food, good company.",
    )
    hero_subheading = models.TextField(
        default=(
            "A neighbourhood café serving breakfast, brunch, and coffee "
            "done properly."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"

    def __str__(self) -> str:
        return "Home Page Content"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> "HomePageContent":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroImage(models.Model):
    """One or more images shown in the Home page hero — rotates
    automatically if more than one is active."""

    image = models.ImageField(upload_to="hero/")
    alt_text = models.CharField(
        max_length=255,
        help_text="Required for accessibility and SEO — describe the photo.",
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "created_at"]
        verbose_name = "Hero Image"
        verbose_name_plural = "Hero Images"

    def __str__(self) -> str:
        return self.alt_text


class Review(models.Model):
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField()
    source = models.CharField(
        max_length=50, blank=True, help_text="e.g. Google, Manual"
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self) -> str:
        return f"{self.author_name} ({self.rating}★)"

    @property
    def stars(self) -> str:
        return "★" * self.rating + "☆" * (5 - self.rating)


class FAQItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order"]
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"

    def __str__(self) -> str:
        return self.question
