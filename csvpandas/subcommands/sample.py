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
        '--seed-in',
        type=utils.opener('r'),
        help=('file containing integer to generate random seed'))
    parser.add_argument(
        '--seed-out',
        type=utils.opener('w'),
        help=('file containing integer used to generate seed'))

    parser.add_argument(
        '--rest',
        help='file to output rows not included in sample.')

    parser.add_argument(
        '--replace',
        action='store_true',
        help=('Sample with or without replacement.'))


def action(args):
    if args.seed_in:
        seed = int(args.seed_in.read().strip())
    else:
        seed = int(time.time())

    df = args.csv

    if args.n < 1:
        sample = df.sample(
            frac=args.n, replace=args.replace, random_state=seed)
    else:
        sample = df.sample(
            n=int(args.n), replace=args.replace, random_state=seed)

    sample.to_csv(args.out)

    if args.rest:
        df[~df.index.isin(sample.index)].to_csv(args.rest)

    if args.seed_out:
        args.seed_out.write(str(seed))
