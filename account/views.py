from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .mixins import (
    FieldMixin,
    FormValidMixin,
    AuthorAccessMixin,
    SuperUserAccessMixin,
    AuthorsAccessMixin
)
from .models import User
from .forms import ProfileForm, SignupForm
from .tokens import account_activation_token
from blog.models import Article


# Create your views here.
class ArticleList(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldMixin, FormValidMixin, CreateView):
    model = Article
    template_name = 'registration/article_create_update.html'


class ArticleUpdate(AuthorAccessMixin, FieldMixin, FormValidMixin, UpdateView):
    model = Article
    template_name = 'registration/article_create_update.html'


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_delete.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')


class SignUp(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی حساب کاربری شما.'
        message = render_to_string('registration/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.content_subtype = 'html'
        email.send()
        return render(self.request, 'registration/signing_success_page.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activate_success_page.html')
    else:
        return HttpResponse(
            '<div dir="rtl" style="text-align: center;">'
            '<h1>لینک فعال سازی نامعتبر است!</h1>'
            '<a href="/signup" style="text-decoration: none;">ثبت نام</a>'
            '</div>'
        )


class UserList(SuperUserAccessMixin, ListView):
    model = User
    template_name = 'registration/user_table.html'
    context_object_name = 'user'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.values()

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

