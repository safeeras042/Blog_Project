from django.urls import path
from . views import *

app_name = 'home'

urlpatterns = [
    path('', main, name='main'),
    path('content/<int:blog_id>/', blog_content, name='content'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create-blog/', create_blog, name='create_blog'),
    path('my-blogs/', my_blogs, name='my_blogs'),
    path('edit_blog/<int:blog_id>/', edit_blog, name='edit_blog'),
    path('delete_blog/', delete_blog, name='delete_blog'),
]