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

import bz2
import gzip
import sys


def opener(mode='r'):
    """Factory for creating file objects

    Keyword Arguments:
        - mode -- A string indicating how the file is to be opened. Accepts the
            same values as the builtin open() function.
        - bufsize -- The file's desired buffer size. Accepts the same values as
            the builtin open() function.
    """

    def open_file(f):
        if f is sys.stdout or f is sys.stdin:
            return f
        elif f == '-':
            return sys.stdin if 'r' in mode else sys.stdout
        elif f.endswith('.bz2'):
            return bz2.BZ2File(f, mode)
        elif f.endswith('.gz'):
            return gzip.open(f, mode)
        else:
            return open(f, mode)

    return open_file
