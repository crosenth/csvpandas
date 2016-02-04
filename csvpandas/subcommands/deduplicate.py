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

log = logging.getLogger(__name__)


def build_parser(parser):
    parser.add_argument(
        '--on',
        metavar='COLS',
        help=('Comma delimited list of column '
              'names or indices if --no-header'))
    parser.add_argument(
        '--take-last',
        action='store_true',
        help='Take the last duplicate value. Default is first.')


def action(args):
    if args.on:
        on = args.on.split(',')

        if args.no_header:
            on = map(int, on)

        df = args.csv.groupby(by=on, sort=False)
        df = df.tail(1) if args.take_last else df.head(1)
    else:
        keep = 'last' if args.take_last else 'first'
        df = args.csv.drop_duplicates(keep=keep)

    df.to_csv(args.out, index=False)
