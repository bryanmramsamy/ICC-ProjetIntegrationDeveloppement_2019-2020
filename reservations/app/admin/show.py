from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from app.models import Representation, Show, Comment


class ShowResource(resources.ModelResource):
    """Describe how Type resources can be imported or exported"""

    class Meta:
        """Meta definition for ShowResource."""

        model = Show
        skip_unchanged = True


class ShowAdmin(ImportExportModelAdmin):
    """Show admin register class

    Custom administration form and list.
    Add the import/export buttom on the top of the entry.
    """

    list_display = ('title', 'date_created', 'price', 'bookable')
    readonly_fields = ['slug', 'date_created']
    ordering = ('-date_created', 'title')
    date_hierarchy = 'date_created'

    list_filter = ('bookable', 'title')
    search_fields = ('title',)

    fieldsets = (
        ('Information générales', {
            'description': 'Informations générales concernant le spectacle',
            'fields': ('title', 'slug', 'description', 'poster', 'bookable',
                       'price', 'date_created')
        }),
    )

    resource_class = ShowResource


admin.site.register(Show, ShowAdmin)


class RepresentationResource(resources.ModelResource):
    """Describe how Representation resources can be imported or exported"""

    class Meta:
        """Meta definition for RepresentationResource."""

        model = Representation
        skip_unchanged = True


class RepresentationAdmin(ImportExportModelAdmin):
    """Representation admin register class

    Custom administration form and list.
    Add the import/export buttom on the top of the entry.
    """

    list_display = ('show_title', 'location_designation', 'time',
                    'total_seats', 'available_seats')
    readonly_fields = ['available_seats']
    ordering = ('-time',)
    date_hierarchy = 'time'

    list_filter = ('location', 'show')

    fieldsets = (
        ('Information générales', {
            'description': 'Informations générales concernant la \
                représentation',
            'fields': ('show', 'location', 'time', 'total_seats',
                       'available_seats')
        }),
    )

    def show_title(self, representation):
        """Display the name of the show"""

        return representation.show.title

    show_title.short_description = 'Spectacle'

    def location_designation(self, representation):
        """Display the name of the location"""

        return representation.location.designation

    location_designation.short_description = 'Emplacement'

    resource_class = RepresentationResource


admin.site.register(Representation, RepresentationAdmin)

admin.site.register(Comment)