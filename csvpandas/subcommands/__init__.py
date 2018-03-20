# global
import csvpandas
import logging
import os
import pandas
import sys

log = logging.getLogger(__name__)


def build_parser(parser):
    parser.add_argument(
        'csv',
        nargs='*',
        default=[sys.stdin],
        help='CSV tabular blast file of query and subject hits.')

    parser.add_argument(
        '--limit',
        type=int, help='Limit number of rows read from each csv.')
    parser.add_argument(
        '--no-header',
        action='store_true',
        help='If no header available.')
    parser.add_argument(
        '--sep',
        default=',',
        help=('Delimiter to use. If sep is None, will try to '
              'automatically determine this. Regular '
              'expressions are accepted.'))

    # common outputs
    parser.add_argument(
        '-o', '--out',
        metavar='FILE',
        default=sys.stdout,
        type=csvpandas.utils.opener('w'),
        help="Classification results.")

    return parser


def action(args):
    # for debugging:
    # pandas.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)

    dfs = []
    xls_ext = ['.xls', '.xlsx']
    for csv in args.csv:
        try:
            if csv is not sys.stdin and os.path.splitext(csv)[-1] in xls_ext:
                df = pandas.read_excel(
                    csv,
                    header=None if args.no_header else 0)
                df = df.fillna('').astype(str)
            else:
                df = pandas.read_csv(
                        csv,
                        sep=bytes(args.sep, "utf-8").decode('unicode_escape'),
                        dtype=str,
                        nrows=args.limit,
                        comment='#',
                        na_filter=False,
                        header=None if args.no_header else 0)
        except Exception as err:
            log.error(str(err).replace('\n', ''))
            df = pandas.DataFrame()
        dfs.append(df)
    args.csv = pandas.concat(dfs, ignore_index=True)
    return args
