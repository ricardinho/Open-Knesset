from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import ICON_CHOICES, Tidbit, Feedback
from suggestions.forms import InstanceCreateSuggestionForm


class SearchForm(forms.Form):
    q = forms.CharField()


class TidbitSuggestionForm(InstanceCreateSuggestionForm):
    title = forms.CharField(label=_('Title'), max_length=40,
                            initial=_('Did you know ?'))
    icon = forms.ChoiceField(label=_('Icon'), choices=ICON_CHOICES)
    content = forms.CharField(label=_('Content'),
                              widget=forms.Textarea(attrs={'rows': 3}))
    button_text = forms.CharField(label=_('Button text'), max_length=100)
    button_link = forms.CharField(label=_('Button link'), max_length=255)

    class Meta:
        model = Tidbit
        caption = _('Suggest Tidbit')

    def get_data(self, request):
        "Add suggested_by for the tidbit to the action data"

        data = super(TidbitSuggestionForm, self).get_data(request)
        data['suggested_by'] = request.user

        return data


class FeedbackSuggestionForm(InstanceCreateSuggestionForm):

    content = forms.CharField(label=_('Content'),
                              widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Feedback
        caption = _('Send Feedback')

    def __init__(self, *args, **kwargs):
        super(FeedbackSuggestionForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'feedback-post'

    def get_data(self, request):
        "Add suggested_by for the tidbit to the action data"

        data = super(FeedbackSuggestionForm, self).get_data(request)

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        data.update({
            'suggested_by': request.user,
            'ip_address': ip,
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'url': request.get_full_path(),
        })

        return data
