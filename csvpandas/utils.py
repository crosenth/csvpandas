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
import logging
import os
import pandas
import pkg_resources
import re
import subprocess
import sys

from os import path


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


def read_csv(filename, compression=None, **kwargs):
    """Read a csv file using pandas.read_csv with compression defined by
    the file suffix unless provided.
    """

    suffixes = {'.bz2': 'bz2', '.gz': 'gzip'}
    compression = compression or suffixes.get(path.splitext(filename)[-1])
    kwargs['compression'] = compression

    return pandas.read_csv(filename, **kwargs)


def version():
    """
    Depending on if git exists and at what version we can try these commands
    to get the git version from the git tags.  Second, if the package has been
    installed return the installed version.  Finally, if nothing else,
    return 0.0.0
    """

    install_dir = os.path.dirname(__file__)
    git_cmds = (['git', '-C', install_dir, 'describe', '--tags'],  # >= 1.8.5
                ['git', 'describe', '--tags'])  # < 1.8.5
    devnull = open(os.devnull, 'w')

    """
    try the two git commands above ^
    git versions are organized as
    [tag]-[number of commits over tag]-[commit id]
    ex - v0.1.2-38-g6a8e5e3
    """
    for cmd in git_cmds:
        try:
            logging.debug(' '.join(cmd))
            git_re = 'v(?P<tag>[\d.]*)-?(?P<commit>[\d.]*)-?.*'
            git_ver = subprocess.check_output(cmd, stderr=devnull)
            git_search = re.search(git_re, git_ver)
            if git_search.group('commit') == '':
                return git_search.group('tag')
            else:
                return '{tag}.dev{commit} '.format(**git_search.groupdict())
        except Exception as e:
            logging.warn('{} {}'.format(type(e), e.message))

    try:
        """
        return version that was installed if available
        """
        return pkg_resources.require("csvpandas")[0].version
    except pkg_resources.DistributionNotFound as e:
        logging.warn(e)

    return '0.0.0'
