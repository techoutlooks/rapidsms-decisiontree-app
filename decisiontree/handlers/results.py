from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler

from decisiontree.utils import get_survey


class ResultsHandler(KeywordHandler):
    keyword = "results"

    def help(self):
        self.respond("Please enter a survey keyword")

    def handle(self, text):
        """Send the summary of the survey, if one exists."""
        survey = get_survey(text, self.msg.connection)
        if not survey:
            self.respond('Survey "{0}" does not exist'.format(text))
        elif survey.summary:
            self.respond(survey.summary)
        else:
            self.respond('No summary for "{0}" survey'.format(text))
        return True
