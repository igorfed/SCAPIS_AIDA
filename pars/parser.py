import argparse
import sys
import com.color as c
import os

class ARG_PARSE():

    def __init__(self):

        if os.name == 'nt':
            self.data_dir = 'D:/Scapis/Data1'
        else:
            self.data_dir = '/media/igofed/DATA/SCAPIS_Processed_Data'

    def argParse(self):
        parser = argparse.ArgumentParser(description="Scapis. Pre-processing of the data-set")
        parser.add_argument("-data_dir", "--data_dir", required=False, type=str, help='Path to the dataset', default=self.data_dir)
        parser.add_argument("-dataset", "--dataset", required=False, type=str, help='Type of the dataset (drli / ctpi / scapis )', default='ctpa')
        #parser.add_argument("-output_dir", "--output_dir", required=False, type=str,
        #                    help='Output Directory to Store Pseudonymized data', default='ctpa')
        #parser.add_argument("-resolution", "--resolution", required=False, type=str,
        #                    help='Resolution of ', default='ctpa')
        args = parser.parse_args()
        print(c.COLOR.Blue + "-" * 100)
        print(args)
        print(c.COLOR.END)
        #if not os.path.exists(os.path.join(os.path.join(args.data_dir, args.dataset))):
        #    print(c.COLOR.Red + args.dataset + " is not existed" + c.COLOR.END)
            #sys.exit(0)
        return args
