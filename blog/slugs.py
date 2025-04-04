import random
import string

from django.utils.text import slugify


def generate_unique_slug(instance, base_title, update=False):
    max_slug_length = 255  # Maximum length for the slug
    slug = slugify(base_title)

    # Truncate the initial slug if it's too long
    if len(slug) > max_slug_length:
        slug = slug[:max_slug_length]

    model = instance.__class__

    if update:
        slug_exists = model.objects.filter(
            slug__icontains=slug
        ).exclude(pk=instance.pk).exists()

    else:
        slug_exists = model.objects.filter(
            slug__icontains=slug
        ).exists()

    if slug_exists:
        random_string_length = 4
        while True:
            random_string = "".join(random.choices(string.ascii_lowercase, k=random_string_length))
            new_slug = f"{slug}-{random_string}"

            # Check if the new slug is too long
            if len(new_slug) <= max_slug_length:
                if update:
                    if not model.objects.filter(slug=new_slug).exclude(pk=instance.pk).exists():
                        return new_slug
                else:
                    if not model.objects.filter(slug=new_slug).exists():
                        return new_slug
            # If the new slug is too long, reduce the length of the base slug
            else:
                slug = slug[:max_slug_length - random_string_length - 1]
                new_slug = f"{slug}-{random_string}"
                if update:
                    if not model.objects.filter(slug=new_slug).exclude(pk=instance.pk).exists():
                        return new_slug
                else:
                    if not model.objects.filter(slug=new_slug).exists():
                        return new_slug

    return slug
