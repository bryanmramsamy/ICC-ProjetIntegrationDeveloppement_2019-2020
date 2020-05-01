from django.db import models
from django.utils.text import slugify

import itertools

from app.models.location import Location


class Show(models.Model):
    """Model definition for Show."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=60, unique=True)
    poster = models.URLField(max_length=255, null=True, blank=True)
    bookable = models.BooleanField(default=True)
    price = models.FloatField()
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        """Meta definition for Show."""

        verbose_name = 'Spectacle'
        verbose_name_plural = 'Spectacles'
        ordering = ['-date_created']

    def __str__(self):
        """Unicode representation of Show."""

        return "[{}] {}".format(self.pk, self.title)

    def save(self, *args, **kwargs):
        """Save method for Show.

        Generate a slug based on the title if the show doesn't exist yet.
        Rounds the price to 2 decimals.
        """

        if not self.pk:
            self._generate_slug()

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Show."""

        return ('')  # TODO: Define absolute url + url name

    def _generate_slug(self):
        """Generate a slug based on the title of the show

        If the slug is already taken, one or two digits will be added at the
        end of the slug and will increment as long as the slug already exist
        until reaching a non-existant result.
        The slug is truncated to 57 character in order to add the unique digits
        at the end of it.
        """

        max_length = self._meta.get_field('slug').max_length - 3
        value = self.title
        slug_result = slug_original = \
            slugify(value, allow_unicode=True)[:max_length]

        for i in itertools.count(1):
            if not Show.objects.filter(slug=slug_result).exists():
                break
            slug_result = '{}-{}'.format(slug_original, i)

        self.slug = slug_result


class Representation(models.Model):
    """Model definition for Representation."""

    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    class Meta:
        """Meta definition for Representation."""

        verbose_name = 'Représentation'
        verbose_name_plural = 'Représentations'
        ordering = ['time', 'show']

    def __str__(self):
        """Unicode representation of Representation."""

        return "[{}] {} le {} à {}".format(self.pk, self.show.title, self.time,
                                           self.location.designation)

    def get_absolute_url(self):
        """Return absolute url for Representation."""

        return ('')  # TODO: Define absolute url + url name

    # TODO: Define custom methods here