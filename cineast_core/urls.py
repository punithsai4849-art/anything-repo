from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .api import api

from apps.entities.views import (
    home_view,
    entity_list_view,
    entity_detail_view,
    entity_create_view,
    entity_edit_view,
    universal_search_view,
)
from apps.accounts.views import (
    login_view,
    register_view,
    logout_view,
    user_profile_view,
    edit_profile_view,
)
from apps.ratings.views import (
    rate_entity_view,
    delete_rating_view,
)
from apps.reviews.views import (
    create_or_update_review_view,
    delete_review_view,
)
from apps.sharing.views import share_card_view, share_entity_card_view, entity_image_proxy_view
from apps.moderation.views import report_content_view

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Typed REST API (django-ninja)
    path('api/', api.urls),

    # Core Web Pages
    path('', home_view, name='home'),
    path('discover/', entity_list_view, name='entity_list'),
    path('entities/', entity_list_view, name='entity_list_alt'),
    path('entities/add/', entity_create_view, name='entity_add'),
    path('entities/<slug:slug>/share/', share_entity_card_view, name='share_entity_card'),
    path('entities/<slug:slug>/', entity_detail_view, name='entity_detail'),
    path('entities/<slug:slug>/edit/', entity_edit_view, name='entity_edit'),
    
    # Search
    path('search/', universal_search_view, name='search'),

    # Ratings & Reviews Actions
    path('entities/<int:entity_id>/rate/', rate_entity_view, name='rate_entity'),
    path('entities/<int:entity_id>/rate/delete/', delete_rating_view, name='delete_rating'),
    path('entities/<int:entity_id>/review/', create_or_update_review_view, name='create_review'),
    path('reviews/<int:review_id>/delete/', delete_review_view, name='delete_review'),
    
    # Moderation Reporting
    path('report/', report_content_view, name='report_content'),

    # Social Share Card Studio & Image Proxy
    path('reviews/<int:review_id>/share/', share_card_view, name='share_review_card'),
    path('sharing/entity-image/<slug:slug>/', entity_image_proxy_view, name='share_entity_image'),

    # Auth & Profile
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('user/<str:username>/', user_profile_view, name='user_profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    
    # Compatibility aliases
    path('movies/', entity_list_view, name='movie_list'),
    path('movies/add/', entity_create_view, name='movie_add'),
]

from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

