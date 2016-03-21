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

"""Pivot a level of the (possibly hierarchical) column labels, returning a
csv having a hierarchical index with a new inner-most level of row labels.
The level involved will automatically get sorted.
"""

import logging

log = logging.getLogger(__name__)


def build_parser(parser):
    return parser


def action(args):
    args.csv.stack(dropna=False).to_csv(args.out, index=False)
