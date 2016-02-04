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

"""Output csv file in a command line interface friendly way.

FIXME: This might be better off as an extension of
pandas.core.format.TableFormatter.  Going from a DataFrame to string using
apply is a bit slow.
"""

import logging

log = logging.getLogger(__name__)


def build_parser(parser):
    return parser


def action(args):
    df = args.csv
    header = df.columns
    df.columns = ['column{}'.format(col) for col in xrange(len(df.columns))]
    header_dict = {col: header[i] for i, col in enumerate(df.columns)}

    # calculate column widths
    widths = {col: df[col].map(len).max() for col in df.columns}
    # check if header is longer
    for col, width in widths.items():
        widths[col] = max(len(str(header_dict[col])), width)

    # divider - add two spaces
    divider = '+'.join('-' * (widths[col] + 2) for col in df.columns)
    divider = '|' + divider + '|\n'

    # create column formats
    cols = ['{' + col + ':<' + str(widths[col]) + '}' for col in df.columns]
    # join columns into a row
    row = '| ' + ' | '.join(cols) + ' |\n'

    # write
    args.out.write(divider)

    if not args.no_header:
        args.out.write(row.format(**header_dict))
        args.out.write(divider)

    df.apply(lambda x: args.out.write(row.format(**x)), axis=1)

    args.out.write(divider)
