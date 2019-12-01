"""
Hello,

I'm a Python program for suggesting words based on Project Gutenberg books.

Before you start using me please do:
$ python3 -m nltk.downloader punkt

To use me type:
$ python3 whats_next.py --book-id <book id> --query <your query>

For example:
$ python3 whats_next.py --book-id 46 --query god bless

I seem to return ['us'] in these conditions.

I also accept more than one parameter foor book id. You can consult my help
documentation: python3 whats_next.py --help

I wanted to be much more, but I'm a Python program. Without the comments I'm
not that big - you can combine me in one method, in around 100 lines of code.

Also I wanted to have threads but I'm more slow with them. Don't ask me why...

Have fun!
"""
import argparse

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

from argparse_validators import required_length
from text_indexer import TextIndexer

def main():
    """
    The main method.
    """

    parser = argparse.ArgumentParser(
        description='Word suggestion based on Project Gutenberg books.')
    parser.add_argument('--book-id', dest='book_ids', nargs='+', type=int, required=True,
                        help='the book id of the Project Gutenberg')
    parser.add_argument('--query', nargs='+', type=str, required=True,
                        help='suggest next word for list of string',
                        action=required_length(1, 5))

    try:
        args = parser.parse_args()
        text_indexer = TextIndexer(len(args.query))

        for book_id in list(dict.fromkeys(args.book_ids)):
            text = strip_headers(load_etext(book_id)).strip()
            text_indexer.add_text(book_id, text)

        print(text_indexer.suggest(*args.query))
    except Exception as exc: # pylint: disable=W0703
        print(exc)

if __name__ == "__main__":
    main()
