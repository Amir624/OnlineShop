from .models import Product


class Compair:
    def __init__(self, request):
        self.user = request.user
        self.session = request.session

        compair = self.session.get('compair')

        if not compair:
            compair = self.session['compair'] = {}

        self.compair = compair

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.compair:
            self.compair[product_id] = {}
        self.save()

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.compair:
            del self.compair[product_id]
            self.save()

    def save(self):
        self.session.modified = True


    def __iter__(self):
        product_ids = self.compair.keys()
        products = Product.objects.filter(id__in=product_ids)

        compair = self.compair.copy()

        for product in products:
            compair[str(product.id)]['product_obj'] = product

        for item in compair.values():

            yield item