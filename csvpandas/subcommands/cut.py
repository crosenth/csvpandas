# This file is part of csvpandas
#
#    csvpandas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    csvpandas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with csvpandas.  If not, see <http://www.gnu.org/licenses/>.

"""Deduplicate any number of csv file with optional column group indexing.
"""

import logging
import pandas
import sys

from csvpandas import utils

log = logging.getLogger(__name__)


def build_parser(parser):
    # required inputs
    parser.add_argument(
        'csv',
        nargs='+',
        help='CSV tabular blast file of query and subject hits.')

    # common outputs
    parser.add_argument(
        '-o', '--out', metavar='FILE',
        default=sys.stdout, type=utils.opener('w'),
        help="Classification results.")

    parser.add_argument(
        '--limit', type=int, help='Limit number of rows read from each csv.')
    parser.add_argument(
        '--columns',
        metavar='COLS',
        help=('Comma delimited list of column '
              'names or indices if --no-header'))
    parser.add_argument(
        '--no-header',
        action='store_true',
        help='If no header available.')


def action(args):
    # for debugging:
    # pandas.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)

    df = []
    for csv in args.csv:
        df.append(utils.read_csv(
            csv,
            dtype=str,
            nrows=args.limit,
            comment='#',
            na_filter=False,
            header=None if args.no_header else 0))

    df = pandas.concat(df, ignore_index=True)

    columns = args.columns.split(',')
    df[columns].to_csv(args.out, index=False)
