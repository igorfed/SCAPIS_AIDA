"""Module documentation goes here
   and here
   and ...
"""

__author__ = "Igor F"
__copyright__ = "free"
__version__ = "1.0.1"

from pars.parser import ARG_PARSE
from com.patient import PATIENTS

from com.console_menu import MENU



def main(pnt, args):

    __menu = MENU(pnt, args)
    __menu.ui_selection()


if __name__ == '__main__':

    __args = ARG_PARSE()
    args = __args.argParse()

    __pnt = PATIENTS(args)
    main(__pnt, args)