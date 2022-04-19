import argparse
import com.color as c
import os


class ARG_PARSE:

    def __init__(self):

        if os.name == 'nt':
            self.data_dir = 'D:/Scapis/Data'
        else:
            self.data_dir = '/media/igofed/DATA/SCAPIS_Processed_Data'

    def argParse(self):
        parser = argparse.ArgumentParser(
            description='''Scapis. This is an updatable software platform to integrate pseudo anonymized data and 
            run selected GAN to generate medical images''',

            epilog="""All is well that ends well.""")
        parser.add_argument("-input",
                            "--input",
                            required=False,
                            type=str,
                            help='Path to pseudoanonimized dataset',
                            default=self.data_dir)

        parser.add_argument("-dataset",
                            "--dataset",
                            required=False,
                            type=str,
                            default="drli",
                            help='Type of the dataset')

        parser.add_argument("-out",
                            "--out",
                            required=False,
                            type=str,
                            help='Import directory')


        parser.add_argument("-r", "--r",
                            required=False,
                            type=int,
                            help='Setup resolution to rescale')

        parser.add_argument("-n", "--n",
                            required=False,
                            type=int,
                            help='number of images to generate using PCGAN')

        parser.add_argument("-gan_path", "--gan_path",
                            required=False,
                            type=str,
                            help='Path to the GAN results folder')


        parser.add_argument("-plot", "--plot",  action='store_true', required=False, help='Plot sample')

        args = parser.parse_args()
        print(c.COLOR.Blue + "-" * 100)

        print(c.COLOR.END)

        # if not os.path.exists(os.path.join(os.path.join(args.data_dir, args.dataset))):
        #    print(c.COLOR.Red + args.dataset + " is not existed" + c.COLOR.END)
        # sys.exit(0)
        return args
