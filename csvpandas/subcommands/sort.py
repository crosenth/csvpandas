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

"""Sort by column(s) or whole table
"""

import logging

log = logging.getLogger(__name__)


def build_parser(parser):
    parser.add_argument(
        '--columns',
        metavar='COLS',
        help=('Comma delimited list of column '
              'names or indices if --no-header'))
    parser.add_argument(
        '--descending',
        action='store_false',
        dest='ascending',
        help='return results in descending order')


def action(args):
    df = args.csv
    columns = args.columns.split(',') if args.columns else df.columns.tolist()
    df = df.sort_values(by=columns, ascending=args.ascending)
    df.to_csv(args.out, index=False)
