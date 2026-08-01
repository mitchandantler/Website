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


class AboutPageContent(models.Model):
    """Singleton editable copy for the About page — same pattern as
    HomePageContent. `story` holds the full text as plain paragraphs
    separated by blank lines; rendered with the `linebreaks` template
    filter so each becomes its own <p>."""

    heading = models.CharField(max_length=200, default="Our Story")
    story = models.TextField(
        default=(
            "At Mitch & Antler, we believe a great café is about more than "
            "just coffee—it's about creating a place where people feel "
            "welcome, connected, and at home.\n\n"
            "Nestled in the heart of Mitchelton, we've created a space "
            "where neighbours become friends, families gather, and "
            "visitors can slow down and enjoy exceptional food, specialty "
            "coffee, and genuine hospitality. Whether you're stopping by "
            "for your morning coffee, catching up with friends over "
            "brunch, or enjoying a relaxed lunch, every visit is an "
            "opportunity to create memorable moments.\n\n"
            "Our menu is thoughtfully crafted using quality ingredients, "
            "combining familiar favourites with fresh, modern flavours. "
            "Every dish and every cup of coffee is prepared with care, "
            "because we believe the little details make all the "
            "difference.\n\n"
            "More than anything, Mitch & Antler is built on the values of "
            "warmth, kindness, and community. We take pride in knowing our "
            "regulars by name while making every first-time guest feel "
            "like they've been here before. We're also proudly "
            "dog-friendly, so your four-legged companions are always "
            "welcome to join you.\n\n"
            "Thank you for making Mitch & Antler part of your day. We "
            "look forward to welcoming you through our doors and sharing "
            "many more coffees, conversations, and celebrations together."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self) -> str:
        return "About Page Content"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> "AboutPageContent":
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
