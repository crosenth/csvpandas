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

"""Merge any number of csvpandas file column wide
"""

import logging
import sys

from csvpandas import utils

log = logging.getLogger(__name__)


def build_parser(parser):
    # required inputs
    parser.add_argument(
        'csv',
        metavar='CSVs',
        nargs='+',
        help='tabulated input file')

    # common outputs
    parser.add_argument(
        '-o', '--out', metavar='FILE',
        default=sys.stdout, type=utils.opener('w'),
        help="out delimited file")

    parser.add_argument(
        '--how',
        choices=['inner', 'outer', 'left', 'right'],
        default='inner',
        help=('how to join %(choices)s'))
    parser.add_argument(
        '--on',
        help=('column delimite list of columns or single common column name'))
    parser.add_argument(
        '--comment', metavar='CHAR',
        help=('comment character'))
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
        dfs.append(utils.read_csv(
            csv,
            dtype=str,
            comment=args.comment,
            na_filter=False,
            header=None if args.no_header else 0))

    if args.on:
        on = args.on.split(',')

        if args.no_header:
            on = map(int, on)
    else:
        on = None

    df = dfs.pop(0)
    for d in dfs:
        df = df.merge(d, how=args.how, on=on)

    df.to_csv(args.out, header=not args.no_header, index=False)
