from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from .models import Product, ProductGallery, Variant, Category, Comment, Color
from .forms import CommentForm
from django.db.models import Q, Min, Max
from .compair import Compair
from django.views.decorators.http import require_GET, require_POST
from .filters import ProductFilter


def home_page(request):
    category = Category.objects.filter(is_sub=False)
    return render(request, 'products/home.html', {'category': category})


def products_views(request):
    products = Product.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    min = Product.objects.aggregate(unit_price=Min('unit_price'))
    min_price = int(min['unit_price'])
    max = Product.objects.aggregate(unit_price=Max('unit_price'))
    max_price = int(max['unit_price'])

    return render(request, 'products/products.html',
                  {'products': products, 'filter': filter, 'min_price': min_price, 'max_price': max_price})


def product_detail(request, slug, pk):
    product = get_object_or_404(Product, slug=slug, pk=pk)
    # variant = get_object_or_404(Variant, pk=pk)
    gallery = ProductGallery.objects.filter(product_id=pk)
    comments = product.comments.all()
    similar = product.tags.similar_objects()[:4]
    form = CommentForm()
    color = Variant.objects.filter(product_id=pk).values('color__name', 'color_id', 'color__color_code').distinct()
    size = Variant.objects.filter(product_id=pk).distinct('size__name', 'size_id')
    if request.method == 'POST':
        variant = Variant.objects.filter(product_id=pk).distinct('color_id', )
        var_id = request.POST.get('select')
        variants = Variant.objects.get(id=var_id)

    else:
        variant = Variant.objects.filter(product_id=pk).distinct('color_id',)

        variants = Variant.objects.get(id=variant[0].id)

        # return render(request, 'products/product_details.html',{'variants': variants, 'variant': variant,'product_var': variant})

    return render(request, 'products/product_details.html',
                  {'products': product, 'form': form, 'similar': similar, 'product_var': variant, 'sizes': size,
                   'colors': color, 'variant': variant, 'variants': variants})

    # if request.method == 'POST':
    #
    #     # variant = Variant.objects.filter(product_id=pk).values('color__name', 'color_id',
    #     #                                                        'color__color_code').distinct()
    #
    # var_id = request.POST.get('select')
    # variants = Variant.objects.get(id=var_id)
    #
    #     variant = Variant.objects.filter(product_id=pk)
    #     variants = Variant.objects.get(id=variant[0].id)
    #     context = {'products': products, 'gallery': gallery, 'variant': variant, 'varints': variants, 'form': form,
    #            'comments': comments, 'similar': similar, }
    #     return render(request, 'products/product_details.html', context)


@require_POST
def product_comments(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.product = product
            new_form.save()
            form = CommentForm()
            return redirect('product:detail_page')

    else:
        form = CommentForm()

    return render(request, 'products/product_details.html', {'form': form, 'products': product})


def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if not comment.like.filter(id=request.user.id).exists():
        comment.like.add(request.user)
        comment.dislike.remove(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def comment_dislike(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if not comment.dislike.filter(id=request.user.id).exists():
        comment.dislike.add(request.user)
        comment.like.remove(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@require_GET
def favorite_products(request, pk):
    products = get_object_or_404(Product, pk=pk)
    if not products.favorite.filter(id=request.user.id).exists():
        products.favorite.add(request.user)
        products.total_favorite += 1
        products.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_favorite_products(request, pk):
    products = get_object_or_404(Product, pk=pk)
    if products.favorite.filter(id=request.user.id).exists():
        products.favorite.remove(request.user)
        products.total_favorite -= 1
        products.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def view_favorite_product(request):
    user = request.user
    product = user.favorite.all()
    return render(request, 'products/wishlist.html', {'products': product})


def search_bar(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        products = Product.objects.filter(Q(title__contains=searched) | Q(brand__name__contains=searched) | Q(
            category__name__contains=searched))
        return render(request, 'products/search_result.html', {'searched': searched, 'products': products, })
    else:
        return render(request, 'products/search_result.html')


def compair_detail_view(request):
    compair = Compair(request)

    return render(request, 'products/compair.html', {'compair': compair})


def add_to_compair(request, product_id):
    compair = Compair(request)
    product = get_object_or_404(Product, id=product_id)
    compair.add(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_compair(request, product_id):
    compair = Compair(request)
    product = get_object_or_404(Product, id=product_id)
    compair.remove(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
