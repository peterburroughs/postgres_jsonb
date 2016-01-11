from pyramid.view import view_config

from .models import DBSession, Bargain
from .forms import SearchForm


@view_config(route_name='home', renderer='templates/index.mako')
def index(request):
    display_results = False
    bargains = []
    form = SearchForm(request.POST, meta={'csrf_context': request.session})

    if request.method == 'POST' and form.validate():
        display_results = True
        bargains = DBSession.query(Bargain)
        supplier_id = form.supplier_id.data
        filter_text = form.filter_text.data
        use_contains = form.use_contains.data

        if supplier_id:
            bargains = bargains.filter_by(supplier_id=supplier_id)

        if filter_text:
            # Ex: "color:white" or "animal_info.eye_color:green"
            filter_by, nested_filter_by, filter_value = \
                parse_filter_text(filter_text)

            if use_contains:  # containment operator @> (JSONB only)
                if not nested_filter_by:
                    # WHERE bargains.info @> {"color": "white"}
                    bargains = bargains.filter(
                        Bargain.info.contains({
                            filter_by: filter_value})
                    )
                else:
                    # WHERE bargains.info @> {"animal_info":
                    #                            {"eye_color": "green"}}
                    bargains = bargains.filter(
                        Bargain.info.contains({
                            filter_by: {nested_filter_by: filter_value}})
                    )
            else:  # index operator ->, ->>, #>, #>> (both JSON and JSONB)
                if not nested_filter_by:
                    # WHERE (bargains.info ->> 'color') = 'white'
                    bargains = bargains.filter(
                        Bargain.info[filter_by].astext == filter_value
                    )
                else:
                    # WHERE (bargains.info #>> '{animal_info, eye_color}')
                    #                          = 'green'
                    bargains = bargains.filter(
                        Bargain.info[(filter_by, nested_filter_by)].astext ==
                        filter_value
                    )

    return {
        'display_results': display_results,
        'bargains': list(bargains),
        'form': form,
    }


def parse_filter_text(text):
    filter_by, filter_value = tuple(text.split(':'))
    nested_filter_by = ''
    if '.' in filter_by:
        filter_by, nested_filter_by = tuple(filter_by.split('.'))
    return filter_by, nested_filter_by, filter_value
