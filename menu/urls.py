from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from users.views import (
    menu_list, restaurants_view, edit_menu_item, delete_menu_item, add_order_to_menu,
    add_restaurant, delete_restaurant, edit_restaurant, add_review_view,
    delete_review
)


urlpatterns = [
    path('menu/<int:restaurant_id>/', menu_list, name='menu_list'),
    path('restaurants/', restaurants_view, name='restaurants'),
    path('menu/edit/<int:menu_item_id>/', edit_menu_item, name='edit_menu_item'),
    path('menu/delete/<int:menu_item_id>/', delete_menu_item, name='delete_menu_item'),
    path('menu/add/<int:restaurant_id>', add_order_to_menu, name='add_order_to_menu'),
    path('menu/delete/<int:restaurant_id>', delete_restaurant, name='confirm_restaurant_delete'),
    path('add_restaurant/', add_restaurant, name='add_restaurant'),
    path('menu/edit_restaurant/<int:restaurant_id>/', edit_restaurant, name='edit_restaurant'),
    path('add_review/<int:restaurant_id>/', add_review_view, name='add_review'),
    path('menu/delete_review/<int:review_id>', delete_review, name='confirm_review_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
