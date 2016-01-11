from django import forms
from django.core.validators import RegexValidator

from .models import Supplier

FILTER_TEXT_RE = '^[A-Za-z0-9_]+\.?[A-Za-z0-9_]*:[A-Za-z0-9_]+$'


class SearchForm(forms.Form):
    suppliers = [(s.id, s.name) for s in Supplier.objects.all()]
    suppliers.insert(0, (0, '-- ALL --'))
    supplier_id = forms.ChoiceField(choices=suppliers, label='Supplier',
                                    widget=forms.widgets.Select)
    filter_text = forms.CharField(required=False, label='Filter text',
                                  validators=[RegexValidator(FILTER_TEXT_RE)])
    use_contains = forms.BooleanField(required=False, label='Use contains')
