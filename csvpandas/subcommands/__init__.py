import logging

log = logging.getLogger(__name__)


# global args
def parse_args(parser, argv=None, namespace=None):
    arguments = [
        parser.add_argument(
            '--test',
            type=int,
            help='blah blah')
        ]

    for arg in arguments:
        namespace, argv = parser.parse_known_args(
            args=argv, namespace=namespace)

    return namespace, argv
