from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from blog.models import Blog
from blog.services import get_blog_from_cache


class BlogListView(ListView):
    model = Blog
    
    def get_queryset(self):
        return get_blog_from_cache()
    
    
class BlogDetailView(DetailView):
    model = Blog
    
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_views += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = ('name', 'contents_article', 'image')
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('name', 'contents_article', 'image')
    success_url = reverse_lazy('blog:blog_list')
    
    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
