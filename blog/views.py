
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import post
from django import template
from django.template.defaultfilters import stringfilter

from django.core.mail import EmailMultiAlternatives
from login_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mass_mail
from django.core.mail import  send_mail
from django.core.mail import EmailMessage
from .models import Email
from django.core import mail



def home(request):
    context = {
        'posts': post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = post
    template_user = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['date']
    paginate_by = 6


class UserPostListView(ListView):
    model = post
    template_name = 'blog/post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('date')


class PostDetailView(DetailView):
    model = post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# def latest_posts(request):
#     latests = Post.objects.filter(published_date__lte=timezone.now()).reverse()[:3]
#     return render(request, 'blog/post_list.html', {'latests': latests})


def about(request):
    return render(request, 'blog/about.html')



def email(request):
# fetch data
    if request.method == 'POST':
        
        subject = "Subscribed to newsletter"
        message = "You subscribed to THEBLOGGERS newsletter. Get daily notifications from the bloggers"
        email= request.POST.get('email')

        print('subject',subject )
        print('message',message )
        print('email',email )


        msg = EmailMultiAlternatives((subject), (message), EMAIL_HOST_USER, email)
        msg.send()

    return render(request, 'post_detail.html')