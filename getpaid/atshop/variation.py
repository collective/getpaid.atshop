"""

    Define data structures describing product variations.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

import types

import zope.interface
from zope.schema.fieldproperty import FieldProperty
from Products.validation.exceptions import ValidatorError

from getpaid.atshop.interfaces import IVariation
from getpaid.atshop.currency import format_currency

class Variation(object):
    """

    Describe variation as run-time object.

    These objects are created by Archetypes accessors.
    """

    product_code = FieldProperty(IVariation["product_code"])
    title = FieldProperty(IVariation["title"])
    price = FieldProperty(IVariation["price"])

    def line_format(self):
        """
        @return: Describe this variation as one line string, human readable
        """

        value = format_currency(self.price)

        return u"%s (%s)" % (self.title, value)

    @staticmethod
    def decode(line):
        """ Try to decode line of text of variation human-input.

        @param line: Line of human inputted text as unicode string

        @return: Variation object if every thing goes well

        @raise: Products.validation.exceptions.ValidatorError if every does not go well
        """

        assert type(line) == types.UnicodeType, "Text lines must be decoded to unicode before processing"

        parts = line.split(";")

        if len(parts) != 3:
            raise ValidatorError(u"Line must contain three sections separated by two ; characters.")

        variation = Variation()

        try:
            variation.product_code = parts[0].strip()
        except Exception, e:
            # Raised by zope.schema.FieldProperty
            raise ValidatorError(u"product_code is not good value:" + str(e))

        try:
            variation.title = parts[1].strip()
        except Exception, e:
            # Raised by zope.schema.FieldProperty
            raise ValidatorError(u"Title is not good value:" + unicode(e))

        try:
            variation.price = float(parts[2].strip())
        except Exception, e:
            # Raised by zope.schema.FieldProperty
            raise ValidatorError(u"Price is not good value:" + unicode(e))

        return variation




