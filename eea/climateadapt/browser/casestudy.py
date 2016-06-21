from eea.climateadapt.browser import AceViewApi
from eea.climateadapt.vocabulary import _relevance
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from plone.z3cform.fieldsets.extensible import FormExtender
from zope.interface import classImplements


class CaseStudyView(DefaultView, AceViewApi):
    def __call__(self):
        return super(CaseStudyView, self).__call__()

    def get_adaptation_options(self):
        # TODO: filter by published
        return [o.to_object for o in self.context.adaptationoptions]

    def relevances_dict(self):
        return dict(_relevance)


class CaseStudyEditForm(DefaultEditForm):
    """ Edit form for case studies
    """

CaseStudyEditView = layout.wrap_form(CaseStudyEditForm)
classImplements(CaseStudyEditView, IDexterityEditForm)


class CaseStudyAddForm(DefaultAddForm):
    """ Add Form for case studies
    """


class CaseStudyFormExtender(FormExtender):
    def update(self):
        self.move('IGeolocatable.geolocation', after='geochars')
        self.move('primary_photo', after='long_description')
        self.move('relevance', after='climate_impacts')
        self.move('solutions', after='climate_impacts')
        self.move('adaptationoptions', after='climate_impacts')
        self.move('objectives', after='climate_impacts')
        self.move('challenges', after='climate_impacts')
        self.move('contact', before='websites')
