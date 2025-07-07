from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editor/', views.quill_editor_view, name='quill_editor'),
    path('add-category/', views.add_category, name='add_category'),
    path('create-article/', views.create_article, name='create_article'),
    path('list-article/',views.list_article),
    path('add-category-ajax/', views.add_category_ajax, name='add_category_ajax'),
    path('article_list/', views.article_list, name='article_list'),
    path('submit_post/', views.submit_post, name='submit_post'),
    path('admin/', admin.site.urls),
]

# 👇 This must be *outside* the main list
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
