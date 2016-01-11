from wtforms import Form, BooleanField, SelectField, SubmitField, StringField
from wtforms.validators import Optional, Regexp

from .models import DBSession, Supplier

FILTER_TEXT_RE = '^[A-Za-z0-9_]+\.?[A-Za-z0-9_]*:[A-Za-z0-9_]+$'


class SearchForm(Form):
    suppliers = [(s.id, s.name) for s in DBSession.query(Supplier).all()]
    suppliers.insert(0, (0, '-- ALL --'))
    supplier_id = SelectField('Supplier', coerce=int, choices=suppliers)
    filter_text = StringField('Filter text', [Optional(),
                                              Regexp(FILTER_TEXT_RE)])
    use_contains = BooleanField('Use contains')
    submit = SubmitField('Search')
