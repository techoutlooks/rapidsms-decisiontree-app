from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler

from decisiontree.models import Tree


class ResultsHandler(KeywordHandler):
    keyword = "results"

    def help(self):
        self.respond("Please enter a survey keyword")

    def get_survey(self, trigger):
        """Limit survey pool to those for the sender's tenant."""
        from decisiontree.multitenancy.utils import multitenancy_enabled
        queryset = Tree.objects.filter(trigger=trigger)
        if multitenancy_enabled():
            tenant = self.msg.connection.backend.tenantlink.tenant
            queryset = queryset.filter(tenantlink__tenant=tenant)
        return queryset[0] if queryset else None

    def handle(self, text):
        """Send the summary of the survey, if one exists."""
        survey = self.get_survey(trigger=text)
        if not survey:
            self.respond('Survey "{0}" does not exist'.format(text))
        elif survey.summary:
            self.respond(survey.summary)
        else:
            self.respond('No summary for "{0}" survey'.format(text))
        return True
