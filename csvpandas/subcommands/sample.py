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

"""Randomly sample rows of a csv file
"""

import logging
import pandas
import sys
import time

from csvpandas import utils

log = logging.getLogger(__name__)


def build_parser(parser):
    # required inputs
    parser.add_argument(
        'n',
        type=float,
        help='number of rows to sample.  Can be a decimal fraction.')
    parser.add_argument(
        'csv',
        nargs='+',
        help='CSV tabular blast file of query and subject hits.')
    parser.add_argument(
        '--seed-in',
        type=utils.opener('r'),
        help=('file containing integer to generate random seed'))
    parser.add_argument(
        '--seed-out',
        type=utils.opener('w'),
        help=('file containing integer used to generate seed'))

    # common outputs
    parser.add_argument(
        '-o', '--out', metavar='FILE',
        default=sys.stdout, type=utils.opener('w'),
        help="Classification results.")
    parser.add_argument(
        '--rest',
        help='file to output rows not included in sample.')

    parser.add_argument(
        '--replace',
        action='store_true',
        help=('Sample with or without replacement.'))
    parser.add_argument(
        '--limit', type=int, help='Limit number of rows read from each csv.')
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
        df.append(pandas.read_csv(
            csv,
            dtype=str,
            nrows=args.limit,
            comment='#',
            na_filter=False,
            header=None if args.no_header else 0))

    df = pandas.concat(df, ignore_index=True)

    if args.seed_in:
        seed = int(args.seed_in.read().strip())
    else:
        seed = int(time.time())

    if args.n < 1:
        sample = df.sample(
            frac=args.n, replace=args.replace, random_state=seed)
    else:
        sample = df.sample(
            n=args.n, replace=args.replace, random_state=seed)

    sample.to_csv(args.out)

    if args.rest:
        df[~df.index.isin(sample.index)].to_csv(args.rest)

    if args.seed_out:
        args.seed_out.write(str(seed))
