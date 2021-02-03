import argparse
import swsearch


def get_parser():
    parser = argparse.ArgumentParser(
        description='swsearch version {}'.format(swsearch.version)
    )

    add_search_term_argument(parser)
    add_config_path_option(parser)
    return parser


def add_search_term_argument(parser):
    parser.add_argument(
        'search_term',
        type=str,
        help='The term to search for e.g. “Luke” or “Millennium Falcon“.'
    )


def add_config_path_option(parser):
    parser.add_argument(
        '--config',
        help='Path to local Configuration file.',
        required=False
    )
