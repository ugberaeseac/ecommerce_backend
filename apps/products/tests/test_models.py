from django.test import TestCase
from apps.products.models import Category, Product



class CategoryModelTest(TestCase):
    """
    test for the category model
    """

    def test_create_category(self):
        """ test to create a category """
        category = Category.objects.create(
                name = 'Electronics',
                slug = 'electronics'
                )
        self.assertEqual(category.name, 'Electronics')
        self.assertEqual(category.slug, 'electronics')


class ProductModelTest(TestCase):
    """
    test for the product model
    """

    def test_create_product_with_stock(self):
        """ test to create product with stock """
        category = Category.objects.create(
                name = 'Romance Novels',
                slug = 'romance-novels'
                )
        product = Product.objects.create(
                name = 'The Big Picture',
                price = 15590.00,
                stock = 18,
                category = category)
        self.assertEqual(product.name, 'The Big Picture')
        self.assertEqual(product.price, 15590.00)
        self.assertEqual(product.stock, 18)
        self.assertEqual(product.category.name, 'Romance Novels')
        self.assertEqual(product.category.slug, 'romance-novels')
        self.assertTrue(product.in_stock)



    def test_create_product_without_stock(self):
        """ test to create product without stock """
        category = Category.objects.create(
                name = 'Kitchen Utensils',
                slug = 'kitchen-utensils'
                )
        product = Product.objects.create(
                name = 'Steel spoons',
                price = 450.50,
                stock = 0,
                category = category)
        self.assertFalse(product.in_stock)




