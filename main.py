"""
#######################################################################
LICENSE INFORMATION
This file is part of TinyFEM.

TinyFEM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TinyFEM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TinyFEM. If not, see <https://www.gnu.org/licenses/>.
#######################################################################

#######################################################################
Description:
Main file.
Execute to start.
#######################################################################
"""
from source.gui import GUI

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()