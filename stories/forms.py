from django import forms
from .models import Blog, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'name'}))
    class Meta:
        model = Category
        fields = ['name']

STATUS = (
    ('Select Status', 'Select Status'),
    ('draft', 'draft'),
    ('published', 'published')
)

class StoryForm(forms.ModelForm):
    name = forms.CharField(label='', max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Post Title'}))
    summary = forms.CharField(label='', max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Post Summary'}))
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Post Body'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class':'form-select'}), empty_label='Select Category')
    # category = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class':'form-select'}))
    is_featured = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}), required=False)
    status = forms.ChoiceField(choices=STATUS, widget=forms.Select(attrs={'class':'form-select'}), label='Status')
    class Meta:
        model = Blog
        fields = ('name', 'category', 'summary', 'body', 'status', 'is_featured', 'image', 'image_pg', 'featured_image')

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)

        
        # self.fields['category'].choices = [
        #     (item.id, item.name) for item in Category.objects.all()
            
        # ]

        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['image_pg'].widget.attrs.update({'class': 'form-control'})
        self.fields['featured_image'].widget.attrs.update({'class': 'form-control'})
        # self.fields['status'].choices = [
        #     (item.id, item.name) for
        # ]
        # for field in self.fields:
        #     self.fields[field].widget.attrs['class'] = 'form-control'