# from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post

class PostListView(generic.ListView):
    # model = Post         #Post.objects.all()
    template_name = 'blogs/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(status = 'pub').order_by('-date_time_modified')

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'
    context_object_name = 'post'

class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = 'blogs/post_create.html'

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/post_create.html'

class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blogs/post_delete.html'
    success_url = reverse_lazy('post_list')
#---------------------------------------------------------------------------------
# def post_list_view(request):
#     # posts = Post.objects.all()
#     posts = Post.objects.filter(status = 'pub').order_by('-date_time_modified')
#     return render(request, 'blogs/post_list.html', {'post_list': posts})
#----------------------------------------------------------------------------------------
# def post_detail_view(request, pk):

#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blogs/post_detail.html', {'post_detail': post})
#----------------------------------------------------------------------------------------
# def post_create_view(request):

#     if request.method == 'POST':
#         form = PostForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
        
#     else:
#         form = PostForm()

#     return render(request, 'blogs/post_create.html', context={'form': form})
#------------------------------------------------------------------------------------------
# def post_update_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     form = PostForm(request.POST or None, instance=post)
#     if form.is_valid():
#         form.save()
#         return redirect('post_list')
    
    # return render(request, 'blogs/post_create.html', context={'form':form})
#-----------------------------------------------------------------------------------------
# def post_delete_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     if request.method == 'POST':
#         post.delete()
#         return redirect('post_list')

#     return render(request, 'blogs/post_delete.html', context={'post_delete': post})