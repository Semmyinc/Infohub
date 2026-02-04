from django import forms
from .models import Users, Profile
class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    phone = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    confirm_password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))
    

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'username', 'phone']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        # self.fields['password'].widget.attrs['class'] = 'form-control'
        # self.fields['password'].widget.attrs['placeholder'] = 'Password'
        # self.fields['password'].label = ''
        self.fields['password'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        # self.fields['confirm_password'].widget.attrs['class'] = 'form-control'
        # self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Password'
        # self.fields['confirm_password'].label = ''
        self.fields['confirm_password'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class ProfileForm(forms.ModelForm):
    address = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))
    city = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
    state = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))
    country = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))
    # first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    
    class Meta:
        model = Profile
        fields = ('address', 'city', 'state', 'country', 'image')

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    username = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    phone = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}))
    
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'username', 'phone')