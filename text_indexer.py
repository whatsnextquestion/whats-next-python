"""
Text suggestion based on indexing from TextIndexer.
"""
from collections import Counter
import re

import nltk
from nltk.util import ngrams

class TextIndexer:
    """
    TextIndexer supports adding and suggesting next words based on text indexes.

    Each text indexer instance supports queries with exact lenght. For example
    If one has been created with the query_count 3 it cannot be used for queries
    with length 5.

    Example:

    >>> from text_indexer import TextIndexer
    >>> ti = TextIndexer(2)

    >>> ti.add_text(1, 'Python is great! Python is funny! Python is great!')
    >>> ti.add_text(2, 'Python is slow!')

    >>> ti.suggest('python', 'is')
    ['great']
    """

    _paragraph_re = re.compile('\n{2,}')
    """
    Regular expression used to split text into paragraphs - one or more empty
    lines. The texts may contain table of titles, contents, indexes. Hence the
    sentence tokenizer may process them as one sentence.
    """

    _punctuation = ['.', '!', '?', ',', ';', ':', '...', '`', '\'', '"']
    """
    Used to filter non words from sentences.

    Future versions might distinguish between sentence borders and sentence
    segments separators such as ',', ':', '&', etc.
    """

    def __init__(self, query_count: int, split_paragraphs=False):
        """
        Creates new TextIndexer for quering with specified length.

        Paragraph splitting may be used to reduce suggestion based on text
        that is broken by multiple empty new lines.

        Args:
            query_count (int): length of the query
            split_paragraphs (bool): if paragraphs should be split.

        Raises:
            ValueError: If the query_count is not within 1 and 5.
        """

        self._indexes = {}
        self._split_paragraphs = split_paragraphs
        if 1 <= query_count <= 5:
            self._query_count = query_count
        else:
            raise ValueError('query count should be between 1 and 5, got {got}',
                             got=query_count)

    def add_text(self, text_id: int, text: str):
        """
        Adds text to the TextIndexer.

        When adding a text, the user must assign an id. Although it may seem superfluous,
        future version will support persisted indexes, which will allow more versatile
        suggestion scenarios.

        The text is indexed according to specified query_count when constructing the
        TextIndexer.

        Args:
            text_id (int): the id of the text
            text (str): the text to index
        """

        if text_id in self._indexes:
            return

        index = {}
        self._indexes[text_id] = index

        if self._split_paragraphs:
            paragraphs = TextIndexer._paragraph_re.split(text)
            for paragraph in paragraphs:
                self._index_text(index, paragraph)
        else:
            self._index_text(index, text)


    def _index_text(self, index: dict, text: str):
        for sentence in nltk.sent_tokenize(text):
            words = nltk.word_tokenize(sentence.lower())
            words = [w for w in words if w not in TextIndexer._punctuation]

            for ngram in ngrams(words, self._query_count + 1):
                query = ngram[:-1]
                word = ngram[-1]

                suggestions = {}
                if query not in index:
                    index[query] = suggestions
                else:
                    suggestions = index[query]

                if word not in suggestions:
                    suggestions[word] = 1
                else:
                    suggestions[word] = suggestions[word] + 1

    def suggest(self, *query):
        """
        Suggest a word based on query.

        Args:
            query (str): list of query words

        Returns:
            a list of words that have the higher matching appearances

        Raises:
            ValueError: If the has different count than the TextIndexer's query count.
            KeyError: If the query was not found.
        """
        if len(query) != self._query_count:
            raise ValueError('queries with length {supported} supported, got {got} instead'
                             .format(supported=self._query_count, got=len(query)))
        counter = Counter()
        for book_id in self._indexes:
            index = self._indexes[book_id]
            if query in index:
                counter.update(index[query])

        most_common = counter.most_common(1)
        if len(most_common) == 0:
            raise KeyError("not found")

        highest_count = most_common[0][1]
        suggestions = [e for e in counter if counter[e] == highest_count]

        return suggestions
