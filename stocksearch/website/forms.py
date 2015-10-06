from django import forms
from haystack.forms import SearchForm
from crawlers.origins import origins

class ImageSearchForm(SearchForm):
    origin = forms.MultipleChoiceField(choices=origins, widget=forms.CheckboxSelectMultiple())

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DateRangeSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        return sqs