"""Module documentation goes here
   and here
   and ...
"""

__author__ = "Igor F"
__copyright__ = "free"
__version__ = "1.0.1"

from pars.parser import ARG_PARSE
from com.patient import PATIENTS
from com.menu import MENU

def dcom_proc(args):
    __pnt = PATIENTS(data_dir=args.data_dir, dataset=args.dataset)
    return __pnt


def main(args):

    __menu = MENU(args)
    __menu.ui_selection()


if __name__ == '__main__':

    __args = ARG_PARSE()
    args = __args.argParse()
    __pnt = PATIENTS(data_dir=args.data_dir, dataset=args.dataset)
    main(__pnt)
