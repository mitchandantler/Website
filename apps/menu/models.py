from django.db import models
from django.utils.text import slugify


class DietaryTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Dietary Tag"
        verbose_name_plural = "Dietary Tags"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MenuCategory(models.Model):
    class MenuType(models.TextChoices):
        FOOD = "food", "Food"
        DRINK = "drink", "Drink"

    name = models.CharField(max_length=100)
    menu_type = models.CharField(max_length=10, choices=MenuType.choices)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["menu_type", "display_order", "name"]
        verbose_name = "Menu Category"
        verbose_name_plural = "Menu Categories"

    def __str__(self) -> str:
        return f"{self.name} ({self.get_menu_type_display()})"


def menu_item_image_path(instance: "MenuItem", filename: str) -> str:
    return f"menu/{instance.category.menu_type}/{filename}"


class MenuItem(models.Model):
    category = models.ForeignKey(
        MenuCategory, on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to=menu_item_image_path, blank=True, null=True)
    dietary_tags = models.ManyToManyField(
        DietaryTag, blank=True, related_name="menu_items"
    )
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(
        default=True,
        help_text=(
            "Only approved items show on the public website. Items created "
            "via CSV import are unapproved by default until reviewed here."
        ),
    )
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "display_order", "name"]
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="menu_item_price_non_negative",
            ),
        ]

    def __str__(self) -> str:
        return self.name
