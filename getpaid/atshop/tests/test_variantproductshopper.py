from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from getpaid.atshop.portlets import variantproductshopper
from getpaid.atshop.tests.base import TestCase


class TestPortlet(TestCase):
    """
    Test variant product buy portlet basic functionality.
    """

    def afterSetUp(self):
        self.setRoles(('Manager',))

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name='getpaid.atshop.portlets.VariantProductShopper')
        self.assertEquals(portlet.addview, 'getpaid.atshop.portlets.VariantProductShopper')

    def test_interfaces(self):
        # TODO: Pass any keywoard arguments to the Assignment constructor
        portlet = variantproductshopper.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(IPortletType, name='getpaid.atshop.portlets.VariantProductShopper')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # TODO: Pass a dictionary containing dummy form inputs from the add form
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], variantproductshopper.Assignment))


    def test_obtain_renderer(self):


        self.portal.invokeFactory("MultiImageProduct", "product")
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal.product)

        # TODO: Pass any keywoard arguments to the Assignment constructor
        assignment = variantproductshopper.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, variantproductshopper.Renderer))


class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))
        self.portal.invokeFactory("MultiImageProduct", "product")


    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)

        # TODO: Pass any default keywoard arguments to the Assignment constructor
        assignment = assignment or variantproductshopper.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        # TODO: Pass any keywoard arguments to the Assignment constructor
        r = self.renderer(context=self.portal.product, assignment=variantproductshopper.Assignment())
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        # TODO: Test output


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
