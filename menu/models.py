from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_positive(value):
    if value <= 0:
        raise ValidationError('قیمت باید بیشتر از صفر باشد.')


def validate_rate(value):
    if value <= 0 or value > 5:
        raise ValidationError('امتیاز رستوران باید بین 1 و 5 باشد.')


class BaseModel(models.Model):
    """A base class for other models"""
    is_active = models.BooleanField(
        default=False,
        verbose_name='فعال',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد شده'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ تغییر داده شده'
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        raise NotImplementedError('You did not override the string method!')


class Restaurant(BaseModel):
    """
    The restaurant's information
    """
    name = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='اسم',
    )
    address = models.TextField(
        blank=False,
        verbose_name='آدرس',
    )
    phone_number = models.CharField(
        blank=False,
        max_length=11,
        verbose_name='شماره تماس',
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='restaurants',
        verbose_name='صاحب رستوران'
    )
    picture = models.ImageField(
        upload_to='restaurants/', blank=True, default='media/restaurants/default_image.jpg', verbose_name='عکس'
    )

    class Meta:
        verbose_name = 'رستوران'
        verbose_name_plural = 'رستوران ها'

    def __str__(self) -> str:
        return f'{self.name}'

    @property
    def امتیاز_رستوران(self):
        reviews = Review.objects.filter(is_active=True, restaurant=self)
        total = 0
        for review in reviews:
            total += review.rate

        if reviews:
            average = total / len(reviews)
            return average
        else:
            return 0


class Category(BaseModel):

    title = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='تیتر',
    )
    description = models.TextField(
        blank=False,
        verbose_name='توضیحات',
    )

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self) -> str:
        return f'{self.title}'


class Order(BaseModel):

    name = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='اسم',
    )
    cost = models.FloatField(
        verbose_name='قیمت ( ریال ) ',
        validators=[validate_positive]
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='دسته بندی'
    )
    picture = models.ImageField(
        upload_to='menu_images/', blank=True, default='menu_images/default_image.jpg'
    )

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self) -> str:
        return f'{self.name} : {self.cost}ریال '


class RestaurantMenu(BaseModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, verbose_name='رستوران'
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='سفارش'
    )

    class Meta:
        verbose_name = 'سفارش رستوران'
        verbose_name_plural = 'سفارشات رستوران ها'

    def __str__(self) -> str:
        return f'{self.restaurant} : {self.order}'


class Review(BaseModel):
    rate = models.IntegerField(
        verbose_name='امتیاز',
        validators=[validate_rate]
    )
    description = models.TextField(
        blank=False,
        verbose_name='توضیحات'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='رستوران')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self) -> str:
        return f'{self.rate} : {self.description}'
