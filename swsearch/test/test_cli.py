import sys
import unittest

import swsearch.cli
import swsearch.__main__


class TestCli(unittest.TestCase):

    def test_arg_parsing(self):

        to_parse = [
            'foo',
            'bar --config foo',
        ]

        not_to_parse = [
            'bar foo',
            '--foo',
        ]

        parser = swsearch.cli.get_parser()

        for args in to_parse:
            try:
                parser.parse_args(args.split(' '))
            except SystemExit:
                self.fail('Arguments should be parsed: {!r}'.format(args))

        for args in not_to_parse:
            old_stderr = sys.stderr
            try:
                with open('/dev/null', 'w+') as sys.stderr:
                    parser.parse_args(args.split(' '))
                self.fail('Arguments should not be parsed: {!r}'.format(args))
            except SystemExit:
                pass
            finally:
                sys.stderr = old_stderr
