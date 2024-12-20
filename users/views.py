from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm, OrderForm, RestaurantForm, ReviewForm
from django.contrib.auth.decorators import login_required
from menu.models import RestaurantMenu, Restaurant, Order, Review
from django.contrib import messages
from django.db.models import Q


def restaurants_view(request):
    # Retrieve all active restaurants
    query = request.GET.get('query', '')

    if query:
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) | Q(address__icontains=query), is_active=True
        )
    else:
        restaurants = Restaurant.objects.filter(is_active=True)

    return render(request, 'users/restaurants.html', {
        'restaurants': restaurants,
        'query': query,
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('restaurants')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('restaurants')
            else:
                form.add_error(None, 'نام کاربری یا رمز عبور نادرست است')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def menu_list(request, restaurant_id):
    query = request.GET.get('query', '')
    restaurant = get_object_or_404(Restaurant, id=restaurant_id,)
    if query:
        menu_items = RestaurantMenu.objects.filter(
            Q(order__name__icontains=query) | Q(order__category__title__icontains=query, is_active=True)
        )
    else:
        menu_items = RestaurantMenu.objects.filter(restaurant=restaurant, )
    reviews = Review.objects.filter(is_active=True, restaurant=restaurant)

    return render(request, 'users/menu_list.html', {
        'menu_items': menu_items,
        'restaurant': restaurant,
        'reviews': reviews,
        'query': query,
    })


@login_required
def edit_menu_item(request, menu_item_id):
    # Retrieve the order instance
    restaurant_order = get_object_or_404(RestaurantMenu, id=menu_item_id)
    restaurant = restaurant_order.restaurant
    order = restaurant_order.order

    if restaurant.owner != request.user:
        messages.error(request, "You do not have permission to delete this menu item.")
        return redirect('menu_list', restaurant.id)

    if request.method == 'POST':
        # Bind the form to the data from the POST request
        form = OrderForm(request.POST, request.FILES, instance=order)

        if form.is_valid():
            # Save the updated order
            form.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('menu_list', restaurant.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Instantiate the form with the current order instance to pre-populate it
        form = OrderForm(instance=order)

    return render(request, 'users/edit_menu_item.html', {
        'form': form, 'order': order,
    })


@login_required
def delete_menu_item(request, menu_item_id):
    # Get the menu item and its associated restaurant
    menu_item = get_object_or_404(RestaurantMenu, id=menu_item_id)
    restaurant = menu_item.restaurant

    # Ensure the current user is the owner of the restaurant
    if restaurant.owner != request.user:
        messages.error(request, "You do not have permission to delete this menu item.")
        return redirect('menu_list', restaurant.id)

    if request.method == "POST":
        menu_item.delete()
        messages.success(request, "Menu item deleted successfully!")
        return redirect('menu_list', restaurant.id)

    return render(
        request, 'users/confirm_delete.html', {'menu_item': menu_item, 'restaurant': restaurant}
    )


@login_required
def add_order_to_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if restaurant.owner != request.user:
        messages.error(request, "You do not have permission to delete this menu item.")
        return redirect('menu_list', restaurant.id)

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            restaurant_menu = RestaurantMenu(order=order, restaurant=restaurant)
            restaurant_menu.save()
            return redirect('menu_list', restaurant.id)  # Replace with your desired redirect URL
    else:
        form = OrderForm()

    return render(request, 'users/add_order_to_menu.html', {'form': form, 'restaurant': restaurant})


@login_required
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new restaurant instance, but don't save it yet
            restaurant = form.save(commit=False)
            restaurant.owner = request.user  # Set the current logged-in user as the owner
            restaurant.save()  # Save the restaurant to the database
            return redirect('restaurants')  # Redirect to a page showing the list of restaurants
    else:
        form = RestaurantForm()

    return render(request, 'users/add_restaurant.html', {'form': form})


@login_required
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id,)
    if restaurant.owner != request.user:
        messages.error(request, "You do not have permission to delete this menu item.")
        return redirect('menu_list', restaurant.id)
    if request.method == "POST":
        restaurant.delete()
        messages.success(request, "Menu item deleted successfully!")
        return redirect('dashboard')

    return render(
        request, 'users/confirm_restaurant_delete.html', {'restaurant': restaurant}
    )


@login_required
def edit_restaurant(request, restaurant_id):
    # Retrieve the order instance
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if restaurant.owner != request.user:
        messages.error(request, "You do not have permission to delete this menu item.")
        return redirect('menu_list', restaurant.id)

    if request.method == 'POST':
        # Bind the form to the data from the POST request
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)

        if form.is_valid():
            # Save the updated order
            form.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('menu_list', restaurant.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Instantiate the form with the current order instance to pre-populate it
        form = RestaurantForm(instance=restaurant)

    return render(request, 'users/edit_restaurant.html', {
        'form': form,
    })


@login_required
def add_review_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.user != restaurant.owner:
        if request.method == 'POST':
            form = ReviewForm(request.POST, restaurant)
            if form.is_valid():
                review = form.save(commit=False)
                review.restaurant = restaurant
                review.user = request.user
                review.is_active = True
                review.save()
                return redirect('menu_list', restaurant_id=restaurant_id)
        else:
            form = ReviewForm()

        return render(request, 'users/add_review.html', {'form': form, 'restaurant': restaurant})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, is_active=True)
    restaurant = review.restaurant
    if restaurant.owner != request.user:
        messages.error(request, "You do not have permission to delete this menu item.")
        return redirect('menu_list', restaurant.id)
    if request.method == "POST":
        review.delete()
        messages.success(request, "Menu item deleted successfully!")
        return redirect('menu_list', restaurant.id)

    return render(
        request, 'users/confirm_review_delete.html', {'restaurant': restaurant}
    )


@login_required
def user_dash_view(request):
    restaurants = Restaurant.objects.filter(owner=request.user,)
    return render(request, 'users/dashboard.html', {'restaurants': restaurants})
