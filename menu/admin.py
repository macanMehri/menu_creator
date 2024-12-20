from django.contrib import admin
from .models import Restaurant, Category, Order, RestaurantMenu, Review


# My actions
@admin.action(description='فعال سازی گزینه های انتخاب شده')
def activate_selected_items(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='غیر فعال کردن گزینه های انتخاب شده')
def deactivate_selected_items(modeladmin, request, queryset):
    queryset.update(is_active=False)


class BaseAdmin(admin.ModelAdmin):

    # Actions
    actions = (
        activate_selected_items,
        deactivate_selected_items,
    )


@admin.register(Restaurant)
class AdminRestaurant(BaseAdmin):
    list_display = (
        'id',
        'name',
        'address',
        'phone_number',
        'owner',
        'امتیاز_رستوران',
        'is_active',
        'created_date',
        'updated_date',
    )
    list_display_links = ('id', 'name',)
    list_filter = ('owner', 'is_active', 'created_date', 'updated_date')
    list_editable = ('is_active',)
    # Order by primary key
    ordering = ('pk',)

    search_fields = ('id', 'name', 'address', 'phone_number')


@admin.register(Category)
class AdminCategory(BaseAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'is_active',
        'created_date',
        'updated_date',
    )
    list_display_links = ('id', 'title',)
    list_filter = ('is_active', 'created_date', 'updated_date')
    list_editable = ('is_active',)
    # Order by primary key
    ordering = ('pk',)

    search_fields = ('id', 'title', 'description',)


@admin.register(Order)
class AdminOrder(BaseAdmin):
    list_display = (
        'id',
        'name',
        'cost',
        'category',
        'picture',
        'is_active',
        'created_date',
        'updated_date',
    )
    list_display_links = ('id', 'name',)
    list_filter = ('cost', 'is_active', 'created_date', 'updated_date')
    list_editable = ('is_active',)
    # Order by primary key
    ordering = ('pk',)

    search_fields = ('id', 'name', 'category__title',)


@admin.register(RestaurantMenu)
class AdminRestaurantMenu(BaseAdmin):
    list_display = (
        'id',
        'restaurant',
        'order',
        'is_active',
        'created_date',
        'updated_date',
    )
    list_display_links = ('id', 'restaurant', 'order',)
    list_filter = ('is_active', 'created_date', 'updated_date')
    list_editable = ('is_active',)
    # Order by primary key
    ordering = ('pk',)

    search_fields = ('id', 'restaurant__name', 'order__name',)


@admin.register(Review)
class AdminReview(BaseAdmin):
    list_display = (
        'id',
        'restaurant',
        'user',
        'rate',
        'description',
        'is_active',
        'created_date',
        'updated_date',
    )
    list_display_links = ('id', 'restaurant', 'user', 'rate')
    list_filter = ('restaurant', 'user', 'rate', 'is_active', 'created_date', 'updated_date')
    list_editable = ('is_active',)
    # Order by primary key
    ordering = ('created_date',)

    search_fields = ('id', 'restaurant__name', 'user__username', 'description',)
