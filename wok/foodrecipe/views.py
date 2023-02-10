from django.views.generic import ListView

from foodrecipe.models import Post


class PostsList(ListView):
    model = Post
    template_name = 'foodrecipe/index.html'
    context_object_name = 'foodrecipe_post_posts'
    queryset = Post.objects.filter(is_published = True, moderated = True).order_by('-date_created')

    #def get_queryset(self):
    #    user = get_object_or_404(User, username = self.kwargs.get('username'))
    #    return Post.objects.filter(author = user).order_by('-date_created')