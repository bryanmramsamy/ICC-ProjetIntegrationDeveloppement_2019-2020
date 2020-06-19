import itertools

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from app.models.location import Location




class Show(models.Model):
    """Model definition for Show."""

    title = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField(verbose_name="Déscription")
    poster = models.URLField(max_length=255, null=True, blank=True,
                             verbose_name="URL du poster")
    bookable = models.BooleanField(default=True, verbose_name="Réservable")
    price = models.FloatField(verbose_name="Prix d'une place (EUR)")
    date_created = models.DateField(auto_now_add=True, null=True, blank=True,
                                    verbose_name="Date de création")

    class Meta:
        """Meta definition for Show."""

        verbose_name = 'Spectacle'
        verbose_name_plural = 'Spectacles'
        ordering = ['-date_created']

    def __str__(self):
        """Unicode representation of Show."""

        return "{}".format(self.title)

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

        return reverse('show_detail_slug', kwargs={'slug': self.slug})

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
            slugify(value, allow_unicode=False)[:max_length]

        for i in itertools.count(1):
            if not Show.objects.filter(slug=slug_result).exists():
                break
            slug_result = '{}-{}'.format(slug_original, i)

        self.slug = slug_result


class Representation(models.Model):
    """Model definition for Representation."""

    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="Début de la réprésentation")
    total_seats = models.PositiveIntegerField(verbose_name="Nombre total \
        de sièges")
    available_seats = models.PositiveIntegerField(verbose_name="Nombre de \
        sièges libres")

    class Meta:
        """Meta definition for Representation."""

        verbose_name = 'Représentation'
        verbose_name_plural = 'Représentations'
        ordering = ['time', 'show']

    def __str__(self):
        """Unicode representation of Representation."""

        return "[{}] {} le {} à {}".format(self.pk, self.show.title, self.time,
                                           self.location.designation)

    def save(self, *args, **kwargs):
        """Save method for Representation.

        Calculate the number of available seats by taking the total amount and
        substract the already booked seats off all the completed reservations
        related to this representation.
        """

        available_seats = self.total_seats
        reservations = self.reservation_set.all()

        for reservation in reservations:
            if reservation.status == "Completed":
                available_seats -= reservation.seats

        self.available_seats = available_seats

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Representation."""

        return reverse('representation_detail', kwargs={'pk': self.pk})


class Comment(models.Model):

    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    # class Meta:
    #     verbose_name = _("comment")
    #     verbose_name_plural = _("comments")

    # def __str__(self):
    #     return self.name

    # def get_absolute_url(self):
    #     return reverse("comment_detail", kwargs={"pk": self.pk})