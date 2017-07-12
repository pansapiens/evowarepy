##  evoware/py -- python modules for Evoware scripting
##   Copyright 2014 Raik Gruenberg
##   Copyright 2017 Andrew Perry (Python 3)
##
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##       http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.
"""microplate format handling"""

import numpy as np
import re
import string


class PlateError(Exception):
    pass


class PlateFormat(object):
    """
    Describe plate columns : rows dimensions and convert back and for between
    'human' (e.g. 'B2') and 'Tecan' (e.g. 10) well numbering.

    Usage:

    >>> f = PlateFormat(96)
    >>> f.nx
    12
    >>> f.ny
    8
    >>> f.pos2int('A2')
    9
    >>> f.pos2int('h12')
    96
    >>> f.int2human(96)
    'H12'

    """

    ex_position = re.compile('([A-Za-z]{0,1})([0-9]+)')

    def __init__(self, n, nx=None, ny=None):
        """
        Define Plate format. Number of columns (nx) and rows (ny) is deduced
        from well number (n), assuming a 3 : 2 ratio of columns : rows. This
        gives the expected dimensions for plates with 1, 2, 6, 12, 24, 48,
        96, 384 and 1536 wells. For any format more odd than this, nx and ny
        should be given explicitely.

        @param n: int, number of wells (e.g. 96)
        @param nx: int, optionally, number of columns (else calculated from n)
        @param ny: int, optionally, number of rows (else calculated from nx)
        """
        self.n = int(n)
        self.nx = int(nx or round(np.sqrt(3. / 2 * self.n)))
        self.ny = int(ny or round(1.0 * n / self.nx))

        if self.nx * self.ny != self.n:
            raise PlateError('invalid plate format: %r x %r != %r' % \
                             (self.nx, self.ny, self.n))

    def str2tuple(self, pos):
        """
        Normalize position string to tuple.
        @param well: str, like 'A1' or '12'
        @return (str, int) - uppercase letter or '', number
        """
        assert isinstance(pos, str)
        match = self.ex_position.match(pos)
        if not match:
            return '', None
        letter, number = match.groups()
        return letter.upper(), int(number)

    def pos2int(self, pos):
        """
        Convert input position to Tecan numbering
        @param pos: str | int | float, e.g. 'A2' or 'a2' or 2 or 2.0
        @return int, plate position according to Tecan numbering ('B1'=>9)

        @raise PlateError, if the resulting position is outside well number
        """
        if type(pos) in [int, float]:
            letter, number = '', int(pos)
        else:
            letter, number = self.str2tuple(pos)

        if letter:
            row = string.ascii_uppercase.find(letter) + 1
            col = number
            r = (col - 1) * self.ny + row
        else:
            r = number

        if r > self.n:
            raise PlateError('plate position %r exceeds number of wells' % r)
        if not r:
            raise PlateError('invalid plate position: %r' % pos)

        return r

    def int2human(self, pos):
        """
        Convert Tecan well position (e.g. running from 1 to 96) into human-
        readable plate coordinate such as 'A1' or 'H12'.
        @param pos: int, well position in Tecan numbering
        @return str, plate coordinate
        """
        assert type(pos) is int

        col = int((pos - 1) / self.ny)
        row = int((pos - 1) % self.ny)

        if col + 1 > self.nx or row > self.ny:
            raise PlateError('position outside plate dimensions')

        r = string.ascii_uppercase[row] + str(col + 1)
        return r

    def gridindex2int(self, row, col):
        """
        >>> p = PlateFormat(96)
        >>> p.gridindex2int(0, 0)
        1
        >>> p.gridindex2int(7, 0)
        8
        >>> p.gridindex2int(0, 1)
        9
        >>> p.gridindex2int(7, 1)
        16
        >>> p.gridindex2int(7, 2)
        24
        >>> p.gridindex2int(3, 2)
        20
        >>> p.gridindex2int(7, 5)
        48

        :param row:
        :type row:
        :param col:
        :type col:
        :param num_cols:
        :type num_cols:
        :param num_rows:
        :type num_rows:
        :return:
        :rtype:
        """
        return (col * self.ny) + row + 1

    def __str__(self):
        return '%i well PlateFormat' % self.n

    def __repr__(self):
        return '<%s>' % str(self)

    def __eq__(self, o):
        return isinstance(o, PlateFormat) and \
               self.n == o.n and self.nx == o.nx and self.ny == o.ny
