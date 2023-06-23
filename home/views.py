from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import wordcount
from .models import newBlog, Comments
from .forms import RegistrationForm
from django.contrib.auth import logout,authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def main(request):
    blogs = newBlog.objects.all().order_by('-id')  # Reverses the order by the 'id' field
    return render(request, 'home/main.html', {'blogs': blogs})

@login_required(login_url='home:login')
def blog_content(request, blog_id):
    blog = get_object_or_404(newBlog, id=blog_id)
    comments = Comments.objects.filter(blog=blog)

    if request.method == 'POST':
        description = request.POST['description']
        
        comment = Comments(blog=blog, author=request.user, description=description)
        comment.save()
        
        return redirect('home:content', blog_id=blog_id)  # Redirect to the same blog content page after creating the comment

    return render(request, 'home/content.html', {'blog': blog, 'comments': comments})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:login') # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'home/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home:main')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home:main')
        else:
            messages.error(request, 'Username or password is incorrect !')

    return render(request, 'home/login.html')


@login_required(login_url='home:login')
def create_blog(request):
    error_message = ""
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        
        
        word_count = len(content.split())
        if word_count < 55:
            error_message = "Content should be a minimum of 55 words."
        else:
            new_blog = newBlog.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            return redirect('home:main')  # Redirect to the blog list page after creating the blog
    
    return render(request, 'home/create_blog.html', {'error_message': error_message})


@login_required(login_url='home:login')
def my_blogs(request):
    user = request.user
    blogs = newBlog.objects.filter(author=user)
    return render(request, 'home/my_blogs.html', {'blogs': blogs})


@login_required(login_url='home:login')
def edit_blog(request, blog_id):
    blog = get_object_or_404(newBlog, id=blog_id, author=request.user)

    if request.method == 'POST':
        # Update the existing blog entry with the new data
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        blog.save()
        return redirect('home:my_blogs')  # Redirect to the blog list page after editing the blog

    return render(request, 'home/edit_blog.html', {'blog': blog})

@login_required(login_url='home:login')
def delete_blog(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(newBlog, id=blog_id, author=request.user)
        blog.delete()
    
    return redirect('home:my_blogs')  # Redirect to the blog list page after deleting the blog
