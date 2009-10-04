from base import TestCase

from getpaid.atshop.variation import Variation

from getpaid.atshop.interfaces import IProductImageProvider

class ProductImagesTestCase(TestCase):

    def test_get_images(self):

        self.loginAsPortalOwner()

        self.portal.invokeFactory("MultiImageProduct", "product")

        product = self.portal.product

        image_provider = IProductImageProvider(product)

        images = image_provider.getImages()

        # Not yet any uploaded images
        self.assertEqual(len(images), 0)

        main_image = image_provider.getMainImage()
        self.assertEqual(main_image, None)

    def test_get_images_one_image(self):

        self.loginAsPortalOwner()

        self.portal.invokeFactory("MultiImageProduct", "product")

        product = self.portal.product
        product.invokeFactory("ProductImage", "testimage")
        image_provider = IProductImageProvider(product)

        images = image_provider.getImages()

        # Not yet any uploaded images
        self.assertEqual(len(images), 1)

        main_image = image_provider.getMainImage()
        self.assertNotEqual(main_image, None)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ProductImagesTestCase))
    return suite
