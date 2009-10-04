from base import TestCase, VARIANTS_TEXT

from zope import component

from getpaid.atshop.variation import Variation
from getpaid.atshop.interfaces import IVariationItemFactory

import getpaid.core.interfaces

class BuyTestCase(TestCase):
    """ Test variant product shopping functionality """

    def test_buy_variant(self):

        self.loginAsPortalOwner()

        self.portal.invokeFactory("VariantProduct", "product")

        self.portal.product.setVariations(VARIANTS_TEXT)

        # create a line item and add it to the car
        cart = self.create_cart()
        item_factory = component.getMultiAdapter((cart, self.portal.product), IVariationItemFactory )

        item = item_factory.create("t-shirt-s")

        self.assertEqual(item.cost, 20.00)

    def test_buy_multi_image(self):

        self.loginAsPortalOwner()

        self.portal.invokeFactory("MultiImageProduct", "product")

        self.portal.product.setPrice(20.00)
        self.portal.product.setWeight(5.00)
        self.portal.product.product_code = u"Foobar"

        # Check that we resolve payable correctly
        payable = getpaid.core.interfaces.IPayable(self.portal.product)

        self.assertEqual(payable.price, 20.00)

        # create a line item and add it to the car
        cart = self.create_cart()

        item_factory = component.getMultiAdapter((cart, self.portal.product), getpaid.core.interfaces.ILineItemFactory)

        item = item_factory.create()

        self.assertEqual(item.cost, 20.00)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(BuyTestCase))
    return suite
