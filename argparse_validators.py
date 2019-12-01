
# pylint: disable=R0903
# the RequiredLength will be reported to have too few public methods
"""
Custom argparse validations.
"""
import argparse

def required_length(nmin: int, nmax: int):
    """
    Integer interval validator for argparse.

    Example:
    >>> import argparse
    >>> from argparse_validators import required_length

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('arg', action=required_length(1, 5))
    """
    class RequiredLength(argparse.Action):
        """
        RequiredLenght validation extends argparse.Action
        """

        def __call__(self, parser, args, values, option_string=None):
            if not nmin <= len(values) <= nmax:
                msg = 'argument "{f}" requires between {s} and {e} arguments, passed {p}'.format(
                    f=self.dest, s=nmin, e=nmax, p=len(values))
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)

        # def dummy(self):
        #     """
        #     pylint is now satisfied, without this method it is 8.89/10
        #     """
        #     return self

    return RequiredLength
