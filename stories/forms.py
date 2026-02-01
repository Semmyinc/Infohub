from django import forms
from .models import Blog, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'name'}))
    class Meta:
        model = Category
        fields = ['name']

class StoryForm(forms.ModelForm):
    name = forms.CharField(label='', max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Post Title'}))
    summary = forms.CharField(label='', max_length=255, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Post Summary'}))
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Post Body'}))
    # category = forms.ModelChoiceField(queryset=queryset.all())
    class Meta:
        model = Blog
        fields = ('name', 'category', 'summary', 'body', 'status', 'is_featured', 'image', 'image_pg' )

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'