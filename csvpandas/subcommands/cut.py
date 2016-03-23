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

"""Filter and truncate CSV files. Like the Unix "cut" command, but for tabular data.
"""

import logging

log = logging.getLogger(__name__)


def build_parser(parser):
    parser.add_argument(
        '--columns',
        metavar='COLS',
        help=('Comma delimited list of column '
              'names or indices if --no-header'))


def action(args):
    columns = args.columns.split(',')
    args.csv[columns].to_csv(args.out, index=False)
