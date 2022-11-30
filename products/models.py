from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)
    sub_cat = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='sub', blank=True, null=True)
    is_sub = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    VARIANT = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Both', 'Both'),
    )

    category = models.ManyToManyField(Category, related_name='cat_product')
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    tags = TaggableManager(blank=True)
    cover = models.ImageField(upload_to='cover/')
    title = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True, unique=True)
    status = models.CharField(max_length=10, choices=VARIANT)
    color = models.ManyToManyField(Color, blank=True,  related_name='color_product')
    size = models.ManyToManyField(Size, blank=True, related_name='size_products')
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.PositiveIntegerField()
    description = models.TextField()
    favorite = models.ManyToManyField(get_user_model(), blank=True, related_name='favorite')
    total_favorite = models.PositiveIntegerField(default=0)
    sell = models.PositiveIntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:detail_page', args=[self.slug, self.id])

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.unit_price * self.discount)

            return int(total - self.unit_price)
        return self.total_price


class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant')
    color = models.ForeignKey(Color, on_delete=models.CASCADE,related_name='var_color', blank=True, null=True)
    size = models.ForeignKey(Size,  on_delete=models.CASCADE,related_name='var_size', blank=True, null=True)
    stock = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.unit_price * self.discount) / 100

            return int(total - self.unit_price)
        return self.total_price


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/', null=True, blank=True)

    def __str__(self):
        return self.product.title


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    like = models.ManyToManyField(get_user_model(), blank=True, related_name='like')
    dislike = models.ManyToManyField(get_user_model(), blank=True, related_name='dislike')
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('product:detail_page', args=[self.id])
