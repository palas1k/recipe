from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView


from foodrecipe.forms import *
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
    model = Post
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        if self.request.POST:
            context['post_content_formset'] = PostContentFormset(self.request.POST, self.request.FILES)
        else:
            context['post_content_formset'] = PostContentFormset()
        return context
    template_name = 'foodrecipe/addpage.html'
    # form_class = PostFormset
    # template_name = 'foodrecipe/addpage.html'
    # success_url = 'home'



# def addpage(request):
#     if request.method == 'POST':
#         form = AddPost(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('posts')
#     else:
#         form =AddPost()
#     return render(request, 'foodrecipe/addpage.html', {'form' : form, 'title': 'Добавление статьи'})

class ViewPost(DetailView):
    model = Post
    template_name = 'foodrecipe/postdetail.html'
    context_object_name = 'foodrecipe_post_viewpost'

def get_formset(request):
    PostFormset = modelformset_factory(model=PostContent, form=AddContent, extra=10, fields=('text', 'image'))
    formset = ''
    if request.method == 'POST':
        formset = PostFormset(request.POST, request.FILES)
        if formset.is_valid():
            # formset = PostFormset.save(commit=False)
            formset = PostFormset.save()
        else:
            formset = PostFormset()
    return render(request, 'foodrecipe/addpage.html', {'formset': formset, 'PostContent': PostContent})




