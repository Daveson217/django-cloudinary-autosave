from django import forms  
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CustomUser    
from cloudinary.forms import CloudinaryFileField
from cloudinary.uploader import upload_resource # new


class CustomUserCreationForm (UserCreationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=254, 
        help_text='Enter anything except "admin", "user", or "superuser"')  
    picture = CloudinaryFileField(options = {
            'crop': 'limit',            
            'zoom': 0.75,
            'width': 200,
            'height': 200,
            'folder': 'picture',            
       }, autosave=False, required=False, help_text="Upload a profile picture") # new

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('picture',)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)        
        super().__init__(*args, **kwargs)
    
    def clean_username(self):
        # I just added a simple validation so we can test the problem
        blacklisted_usernames = ['admin', 'user', 'superuser']
        username = self.cleaned_data.get('username')

        if username in blacklisted_usernames:
            raise forms.ValidationError('You cannot use this username')
        return username
    
    # new
    @transaction.atomic
    def save(self, commit=True):
        # At this point, all validation has been passed
        user = super(CustomUserCreationForm, self).save(commit=False)

        user_picture = self.request.FILES.get('picture', None)
        if user_picture:
            # Also simply writing autosave=True would...
            user.picture = upload_resource(user_picture, **self.fields['picture'].options)            
        else:
            user.picture = None            
        
        if commit:
            user.save()            