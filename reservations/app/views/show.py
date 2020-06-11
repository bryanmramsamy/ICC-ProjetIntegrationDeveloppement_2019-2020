import requests

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, TemplateView
from django.urls import reverse

from app.models.show import Show, Representation
from app.permissions.group import group_required


def show_list(request):
    """Render list of shows"""

    query = request.GET.get("query", None)  # use get GET.get to prevent error
    shows = Show.objects.filter(bookable=True)

    if query is not None:  # if my query is not empty i change the way how the queryset is set
        shows = Show.objects.filter(title__icontains=query)

    # function about pagination i chose to put a default value directly with GEt.get method
    paginator = Paginator(shows, 16)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    context = {'shows': page}
    return render(request, 'app/show_list.html', context)


def show_detail(request, pk):
    """ Display details of one selected show based on its pk"""

    show = get_object_or_404(Show, pk=pk)
    representations = Representation.objects.filter(show=pk)

    context = {
        'show': show,
        'representations': representations
    }
    return render(request, 'app/show_detail.html', context)


def show_detail_slug(request, slug):
    """Display details of one selected show based on its slug"""
    # TODO: Function has been duplicated for slug support, must be merged

    show = get_object_or_404(Show, slug=slug)
    representations = Representation.objects.filter(show=show.pk)

    context = {
        'show': show,
        'representations': representations
    }
    return render(request, 'app/show_detail.html', context)


@group_required('Administrateur', 'Moderateur')
def show_external_api(request):
    """ show external api function """

    show_external = reverse('ext-api-show')
    host = request.get_host()
    api_url = "http://{}{}".format(host, show_external)
    response = requests.get(api_url, timeout=10)
    data = response.json()

    context = {'data': data}
    return render(request, 'app/external_api_show.html', context)


@group_required('Administrateur', 'Moderateur')
def update_show_external_api(request):
    """ update show external api function """

    show_external = reverse('ext-api-show')
    host = request.get_host()
    api_url = "http://{}{}".format(host, show_external)
    response = requests.get(api_url, timeout=10)
    data = response.json()
    new_data = {}
    nb_to_create = 0
    nb_to_update = 0

    for show in data:
        if show['description'] is None:
            show['description'] = 'N/D'

        if show['price'] == 0:
            show['bookable'] = False

        new_show = Show(
            title=show['title'],
            description=show['description'],
            poster=show['poster'],
            bookable=show['bookable'],
            price=show['price'],
        )

        if not Show.objects.filter(title=show['title']):
            is_new = True
            new_data[show['title']] = {
                'show' : show,
                'is_new' : is_new
            }
            new_show.save()
            nb_to_create += 1
        else:
            is_new = False
            new_data[show['title']] = {
                'show' : show,
                'is_new' : is_new
            }
            Show.objects.filter(title=show['title']).update(
                title=show['title'],
                description=show['description'],
                poster=show['poster'],
                bookable=show['bookable'],
                price=show['price'],
            )
            nb_to_update += 1

    context = {
        'data_dico' : new_data.values(),
        'nb_to_create' : nb_to_create,
        'nb_to_update' : nb_to_update,
    }
    return render(request, 'app/update_show.html', context)
