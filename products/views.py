from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.core.paginator import Paginator
from .models import Product, ProductGallery, Variant, Category, Comment, Color, CountViews
from .forms import CommentForm
from django.db.models import Q, Min, Max
from .compair import Compair
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from .filters import ProductFilter
from django.contrib import messages


def home_page(request):
    category = Category.objects.filter(is_sub=False)
    products = Product.objects.all()[:4]

    return render(request, 'products/home.html', {'category': category, 'products': products})


def products_views(request):
    products = Product.objects.all()
    # paginator = Paginator(products)
    # page_num = request.GET.get('page')
    # page_obj = paginator.get_page(page_num)
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    min = Product.objects.aggregate(unit_price=Min('unit_price'))
    min_price = int(min['unit_price'])
    max = Product.objects.aggregate(unit_price=Max('unit_price'))
    max_price = int(max['unit_price'])

    return render(request, 'products/products.html',
                  {'products': products, 'filter': filter, 'min_price': min_price, 'max_price': max_price,
                   })


def product_detail(request, slug, pk):
    product = get_object_or_404(Product, slug=slug, pk=pk)
    gallery = ProductGallery.objects.filter(product_id=pk)
    comments = product.comments.all()
    ip = request.META.get('REMOTE_ADDR')
    view = CountViews.objects.filter(product_id=product.id, ip=ip)
    if not view.exists():
        CountViews.objects.create(product_id=product.id, ip=ip)
        product.views += 1
        product.save()
    similar = product.tags.similar_objects()[:4]
    form = CommentForm()

    if request.method == 'POST':
        variant = Variant.objects.filter(product_id=pk)
        var_id = request.POST.get('select')
        variants = Variant.objects.get(id=var_id)
        color = Variant.objects.filter(product_id=pk, available=True).distinct('color_id', )
        size = Variant.objects.filter(product_id=pk, color_id=variants.color_id, available=True)

    else:
        variant = Variant.objects.filter(product_id=pk)

        variants = Variant.objects.get(id=variant[0].id)
        color = Variant.objects.filter(product_id=pk,  available=True).distinct('color_id')
        size = Variant.objects.filter(product_id=pk, color_id=variants.color_id, available=True)

    return render(request, 'products/product_details.html',
                  {'products': product, 'form': form, 'similar': similar, 'product_var': variant, 'sizes': size,
                   'colors': color, 'variant': variant, 'variants': variants})


@require_POST
def product_comments(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, product.id)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.product = product
            new_form.save()
            messages.success(request, 'نظر شما ثبت شد')
            form = CommentForm()
            return redirect('product:detail_page', product.id)

    else:
        form = CommentForm()

    return render(request, 'products/product_details.html', {'form': form, 'products': product})


@login_required()
def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if not comment.like.filter(id=request.user.id).exists():
        comment.like.add(request.user)
        comment.dislike.remove(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def comment_dislike(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if not comment.dislike.filter(id=request.user.id).exists():
        comment.dislike.add(request.user)
        comment.like.remove(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def favorite_products(request, pk):
    products = get_object_or_404(Product, pk=pk)
    if not products.favorite.filter(id=request.user.id).exists():
        products.favorite.add(request.user)
        messages.success(request, 'محصول به لیست علاقه مندی اضافه شد')
        products.total_favorite += 1
        products.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def remove_favorite_products(request, pk):
    products = get_object_or_404(Product, pk=pk)
    if products.favorite.filter(id=request.user.id).exists():
        products.favorite.remove(request.user)
        messages.success(request, 'محصول از لیست علاقه مندی حذف شد')
        products.total_favorite -= 1
        products.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
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
    if compair.is_empty():
        messages.error(request, 'محصولی در لیست مقایسه وجود ندارد')
        return redirect('product:products')

    return render(request, 'products/compair.html', {'compair': compair})


def add_to_compair(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    compair = Compair(request)

    compair.add(product)

    messages.success(request, 'محصول به لیست مقایسه اضافه شد')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_compair(request, product_id):
    compair = Compair(request)
    product = get_object_or_404(Product, id=product_id)
    compair.remove(product)
    messages.warning(request, 'محصول از لیست مقایسه حذف شد')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def clear_compair(request):
    compair = Compair(request)
    compair.clear()
    return redirect('product:products')


def category(request, pk):
    cat = Product.objects.filter(category=pk)
    return render(request, 'products/category.html', {'category': cat})
