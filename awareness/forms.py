from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label="Ваше ім'я", max_length=100)


class TFForm(forms.Form):
    CHOICES = (
        ('True', 'True'),
        ('False', 'False'),
    )
    choice = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="Оберіть відповідь"
    )


class MCQForm(forms.Form):
    choice = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        # передаємо choices через параметр choices_list
        choices_list = kwargs.pop('choices_list', [])
        super().__init__(*args, **kwargs)
        self.fields['choice'].choices = choices_list
