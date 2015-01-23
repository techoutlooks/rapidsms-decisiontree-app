from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler

from decisiontree.models import Tree


class ResultsHandler(KeywordHandler):

    keyword = "results"

    def help(self):
        self.respond("Please enter a survey keyword")

    def handle(self, text):
        try:
            tree = Tree.objects.get(trigger=text)
        except Tree.DoesNotExist:
            self.respond('Survey "{0}" does not exist'.format(text))
            return True
        if tree.summary:
            self.respond(tree.summary)
        else:
            self.respond('No summary for "{0}" survey'.format(text))
        return True
