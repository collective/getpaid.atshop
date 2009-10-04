"""

    Interface definitions for products with variations.

"""

from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

import zope.schema

from getpaid.atshop import atshopMessageFactory as _

from multiimageproduct import IMultiImageProduct

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

class IVariantProduct(IMultiImageProduct):
    """ Marker interface used to identify VariantProduct content """

    def getProductVariations():
        """ Get variations of this product.

        @return: List of IVariation objects
        """

    def getProductVariationByProductCode(product_code):
        """


        """

    def getCheapestPrice():
        """
        @return: Floating point, cheapeast price of the variations
        """

class IVariationItemFactory(Interface):
    """ Create shopping cart items from IVariantProduct instance.
    """

    def createCartItem(context, variationId):
        """
        @return: IShippableLineItem instance
        """

class IVariation(Interface):
    """ Define information we need to know about one varation.
    """

    product_code = zope.schema.TextLine(title=u"Product code", description=u"Unique id for this variant used in internal data structures", required=True)

    title = zope.schema.TextLine(title=u"Title", description=u"Human readable name of this product", required=True)

    price = schema.Float(title = u"Price", description=u"Price of this variation", required=True)

