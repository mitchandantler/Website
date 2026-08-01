from django.db import models


class GalleryImage(models.Model):
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(
        max_length=255,
        help_text="Required for accessibility and SEO — describe what's in the photo.",
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "created_at"]
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self) -> str:
        return self.caption or self.alt_text
