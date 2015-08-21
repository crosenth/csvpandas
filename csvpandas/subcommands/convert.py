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

"""Convert a csv file in various ways
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
        metavar='CSV',
        nargs='+',
        help='tabulated input file')

    # common outputs
    parser.add_argument(
        '-o', '--out', metavar='FILE',
        default=sys.stdout, type=utils.opener('w'),
        help="out delimited file")

    parser.add_argument(
        '--limit', type=int, help='Limit number of rows read from each csv')
    parser.add_argument(
        '--comment', metavar='CHAR',
        help=('comment character'))

    parser.add_argument(
        '-f', '--from-delimiter',
        metavar='DELIM',
        help=('Delimiter value coming in'))
    parser.add_argument(
        '-t', '--to-delimiter',
        metavar='DELIM',
        help='delimeter value coming out')

    parser.add_argument(
        '--header',
        help=('comma delimted list of header names. '
              'If used in combination with --no-header '
              'then a header wil be added.  Else '
              'this will replace the header line.'))
    parser.add_argument(
        '--no-header',
        action='store_true',
        help='if first line is data')


def action(args):
    # for debugging:
    # pandas.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)

    dfs = []
    for csv in args.csv:
        df = utils.read_csv(
            csv,
            dtype=str,
            nrows=args.limit,
            sep=args.from_delimiter,
            comment=args.comment,
            na_filter=False,
            header=None if args.no_header else 0)
        dfs.append(df)

    df = pandas.concat(dfs, ignore_index=True)

    if args.header:
        df.columns = args.header.split(',')

    df.to_csv(
        args.out,
        header=args.header or not args.no_header,
        sep=args.to_delimiter,
        index=False)
