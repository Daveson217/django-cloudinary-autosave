from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""        
        self.object = form.save() 
        return redirect('login') 
    
    def get_form_kwargs(self):
        """ Passes the request object to the form class."""
        kwargs = super(SignUpView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs