from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView

from foodrecipe.forms import AddPost
from foodrecipe.models import Post


class PostsList(ListView):
    model = Post
    template_name = 'foodrecipe/index.html'
    context_object_name = 'foodrecipe_post_posts'
    queryset = Post.objects.filter(is_published = True, moderated = True).order_by('-date_created')

    #def get_queryset(self):
    #    user = get_object_or_404(User, username = self.kwargs.get('username'))
    #    return Post.objects.filter(author = user).order_by('-date_created')

class CreatePost(CreateView):
    form_class = AddPost
    template_name = 'foodrecipe/addpage.html'



# def addpage(request):
#     if request.method == 'POST':
#         form = AddPost(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('posts')
#     else:
#         form =AddPost()
#     return render(request, 'foodrecipe/addpage.html', {'form' : form, 'title': 'Добавление статьи'})