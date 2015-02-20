import mock

from model_mommy import mommy

from decisiontree.multitenancy.models import TreeLink

from .. import utils
from .cases import DecisionTreeTestCase


@mock.patch("decisiontree.multitenancy.utils.multitenancy_enabled")
class TestGetSurvey(DecisionTreeTestCase):

    def setUp(self):
        super(TestGetSurvey, self).setUp()
        self.survey = mommy.make('decisiontree.Tree')
        self.survey_link = mommy.make(TreeLink, linked=self.survey, tenant=self.tenant)

    def test_no_surveys(self, multitenancy_enabled):
        """get_survey should return None if there are no surveys."""
        self.survey.delete()
        multitenancy_enabled.return_value = False
        survey = utils.get_survey(self.survey.trigger, self.connection)
        self.assertTrue(multitenancy_enabled.call_count, 1)
        self.assertIsNone(survey)

    def test_no_surveys_for_trigger(self, multitenancy_enabled):
        """get_survey should return None if no surveys match the trigger."""
        multitenancy_enabled.return_value = False
        survey = utils.get_survey('asdf', self.connection)
        self.assertTrue(multitenancy_enabled.call_count, 1)
        self.assertIsNone(survey)

    def test_success(self, multitenancy_enabled):
        """get_survey should return survey matching trigger."""
        multitenancy_enabled.return_value = False
        survey = utils.get_survey(self.survey.trigger, self.connection)
        self.assertTrue(multitenancy_enabled.call_count, 1)
        self.assertEqual(survey.pk, self.survey.pk)

    def test_multitenancy_tenant_mismatch(self, multitenancy_enabled):
        """get_survey should return None if connection tenant doesn't match survey tenant."""
        self.survey.tenantlink.tenant = mommy.make('multitenancy.tenant')
        self.survey.tenantlink.save()
        multitenancy_enabled.return_value = True
        survey = utils.get_survey(self.survey.trigger, self.connection)
        self.assertTrue(multitenancy_enabled.call_count, 1)
        self.assertIsNone(survey)

    def test_multitenancy_success(self, multitenancy_enabled):
        """get_survey should return survey matching trigger for connection."""
        multitenancy_enabled.return_value = True
        survey = utils.get_survey(self.survey.trigger, self.connection)
        self.assertTrue(multitenancy_enabled.call_count, 1)
        self.assertEqual(survey.pk, self.survey.pk)
