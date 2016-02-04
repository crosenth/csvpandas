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

"""Search for regex patterns
"""

import logging
import re

log = logging.getLogger(__name__)


def build_parser(parser):
    # required inputs
    parser.add_argument(
        'pattern',
        help=('search for pattern in column(s)'))

    parser.add_argument(
        '--columns',
        metavar='COLS',
        help=('Comma delimited list of column '
              'names or indices if --no-header'))
    parser.add_argument(
        '--all',
        action='store_true',
        help='pattern must exist in any column(s) [any]')
    parser.add_argument(
        '-i',
        '--ignore-case',
        action='store_true',
        help=('Ignore case distinctions in both '
              'the PATTERN and the input files.'))


def action(args):
    if args.columns:
        columns = args.columns.split(',')
    else:
        columns = args.csv.columns.tolist()

    if args.ignore_case:
        pattern = re.compile(args.pattern, re.IGNORECASE)
    else:
        pattern = re.compile(args.pattern)

    def search(string):
        return bool(re.search(pattern, string))

    df = args.csv

    if args.all:
        df = df[df[columns].apply(lambda x: x.map(search).all(), axis=1)]
    else:
        df = df[df[columns].apply(lambda x: x.map(search).any(), axis=1)]

    df.to_csv(args.out, index=False)
