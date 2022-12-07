
from .models import Category, Product


def category(request):
    return {'category': Category.objects.filter(is_sub=False)}
