from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    path('', ArticlesHome.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('addpage/', AddPage.as_view(), name='addpage'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ArticlesCategory.as_view(), name='category'),
    path('graph/', Graph.as_view(), name='graph'),
]