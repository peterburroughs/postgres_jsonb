from django.shortcuts import render

from .models import Bargain
from .forms import SearchForm


def index(request):
    display_results = False
    bargains = []

    supplier_id = None
    filter_text = None

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            display_results = True
            bargains = Bargain.objects.all()
            supplier_id = int(form.cleaned_data['supplier_id'])
            filter_text = form.cleaned_data['filter_text']
            use_contains = form.cleaned_data['use_contains']

            if supplier_id:
                bargains = bargains.filter(supplier_id=supplier_id)

            if filter_text:
                # Ex: "color:white" or "animal_info.eye_color:green"
                filter_by, nested_filter_by, filter_value =\
                    parse_filter_text(filter_text)

                if use_contains:  # containment operator @> (JSONB only)
                    if not nested_filter_by:
                        # WHERE emporium_bargain.info @> {"color": "white"}
                        bargains = bargains.filter(info__contains={
                            filter_by: filter_value
                        })
                    else:
                        # WHERE emporium_bargain.info @> {"animal_info":
                        #    {"eye_color": "green"}}
                        bargains = bargains.filter(info__contains={
                            filter_by: {
                                nested_filter_by: filter_value
                            }
                        })
                else:  # index operator ->, ->>, #>, #>> (both JSON and JSONB)
                    if not nested_filter_by:
                        # WHERE emporium_bargain.info -> 'color' = 'white'
                        filter_keyword = 'info__' + filter_by
                        kwargs = {filter_keyword: filter_value}
                        bargains = bargains.filter(**kwargs)
                    else:
                        # WHERE emporium_bargain.info #> ARRAY['animal_info',
                        #                                      'eye_color']
                        #                                = 'green'
                        filter_keyword = ('info__' + filter_by +
                                          '__' + nested_filter_by)
                        kwargs = {filter_keyword: filter_value}
                        bargains = bargains.filter(**kwargs)

    else:
        form = SearchForm()

    return render(request, 'index.html', {
        'display_results': display_results,
        'bargains': list(bargains),
        'form': form,
    })


def parse_filter_text(text):
    filter_by, filter_value = tuple(text.split(':'))
    nested_filter_by = ''
    if '.' in filter_by:
        filter_by, nested_filter_by = tuple(filter_by.split('.'))
    return filter_by, nested_filter_by, filter_value
