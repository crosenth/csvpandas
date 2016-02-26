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
import pandas

log = logging.getLogger(__name__)


def build_parser(parser):
    # required inputs
    parser.add_argument(
        '--other',
        required=True,
        action='append',
        help='tabulated input file')

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


def action(args):
    others = []
    for other in args.other:
        others.append(pandas.read_csv(
            other,
            dtype=str,
            comment=args.comment,
            na_filter=False,
            sep=args.sep,
            header=None if args.no_header else 0))

    if args.on:
        on = args.on.split(',')

        if args.no_header:
            on = map(int, on)
    else:
        on = None

    for other in others:
        args.csv = args.csv.merge(other, how=args.how, on=on)

    args.csv.to_csv(args.out, header=not args.no_header, index=False)
