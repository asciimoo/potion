# This file is part of potion.
#
#  potion is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  potion is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with potion. If not, see <http://www.gnu.org/licenses/>.
#
# (C) 2012- by Adam Tauber, <asciimoo@gmail.com>

import ConfigParser

cfg = ConfigParser.SafeConfigParser()
cfg.read('/etc/potion.cfg')
cfg.read('.potionrc')

