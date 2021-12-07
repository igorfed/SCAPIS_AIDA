"""Module documentation goes here
   and here
   and ...
"""

__author__ = "Igor F"
__copyright__ = "free"
__version__ = "1.0.1"

import os

from patients import PATIENTS
from console_menu import MENU
from pars.parser import ARG_PARSE


def main(pnt, args):

    __menu = MENU(pnt, args, os.path.dirname(os.path.abspath(__file__)))
    __menu.ui_selection()


if __name__ == '__main__':
    import sys

    for p in sys.path:
        print(p)

    __args = ARG_PARSE()
    args = __args.argParse()
    __pnt = PATIENTS(args)
    main(__pnt, args)