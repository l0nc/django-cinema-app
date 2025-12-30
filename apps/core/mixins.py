from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.text import slugify
from unidecode import unidecode

class AutoSlugMixin:
    """
    Mixin to automatics create unique slug.
    """
    def save(self, *args, **kwargs):
        if not self.slug:
            value = getattr(self, 'name')
            if value:
                self.slug = slugify(unidecode(value))
        super().save(*args, **kwargs)
            
