from django import forms
from django.db import transaction
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Reset, Submit
import reversion


class HelperMixin(object):
    form_helper_cls = FormHelper

    def __init__(self, *args, **kwargs):
        super(HelperMixin, self).__init__(*args, **kwargs)
        self.helper = getattr(self, 'helper', self.form_helper_cls(self))


class SingleButtonMixin(HelperMixin):
    form_helper_cls = FormHelper

    @property
    def action_text(self):
        return _('Update') if (hasattr(self, 'instance') and
                               self.instance.pk) else _('Save')

    def __init__(self, *args, **kwargs):
        super(SingleButtonMixin, self).__init__(*args, **kwargs)
        self.helper.add_input(
            Submit('action', self.action_text, css_class="btn-primary"))


class SaveButtonMixin(SingleButtonMixin):

    def __init__(self, *args, **kwargs):
        super(SaveButtonMixin, self).__init__(*args, **kwargs)
        self.helper.add_input(Reset('reset', _('Reset!')))


class FormHorizontalMixin(HelperMixin):

    def __init__(self, *args, **kwargs):
        super(FormHorizontalMixin, self).__init__(*args, **kwargs)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'


class CommitDescriptionMixin(forms.Form):
    commit_desc = forms.CharField(label=_('Description of change'),
                                  max_length=100)

    def save(self, *args, **kwargs):
        with transaction.atomic(), reversion.create_revision():
            obj = super(CommitDescriptionMixin, self).save(*args, **kwargs)
            commit_desc = self.cleaned_data['commit_desc']
            reversion.set_comment(commit_desc)
            return obj