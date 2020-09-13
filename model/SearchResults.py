from utils.messages import MSG_ADD_SEARCH_RESULT, MSG_CLEAR_SEARCH_RESULT
from pubsub import pub


class SearchResults:
    searchResults = []

    def add(self, data):
        self.searchResults.append(data)

    def clear(self):
        self.searchResults = []

    def count(self):
        return len(self.searchResults)
