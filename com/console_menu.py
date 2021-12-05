import os
from com.color import COLOR
from collections import namedtuple

import train as train


class MENU:
    def __init__(self, __pnt, args, path):
        self.__pnt = __pnt
        self.path = path
        Option = namedtuple('Option', 'label')
        # s = ','.join(STR)
        self.command = {0: Option("Pseudonymization"),
                        1: Option("Generate Pseudonymized data"),
                        2: Option("Exit")}
        self.data_dir = args.input
        self.dataset = args.dataset
        self.export_dir = args.out
        self.plot = args.plot  # do you want top plot
        self.resolution = args.r
        print('abspath:     ', path)
        #print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))
        self.nested_command = {
            0: Option("Import Data"),
            1: Option("Export Pseudonymized Data ->"),
            2: Option("Import Pseudonymized Data <-"),
            3: Option("Sample Plot Pseudonymized Data"),
            4: Option("Back")}
        self.nested_command_1 = {
            0: Option("Generate Pseudonymized data"),
            1: Option("Sample Plot"),
            2: Option("Back")}

    def args(self, args):
        self.input = args.input
        self.dataset = args.dataset
        self.plot = args.plot
        self.resolution = args.r

    @staticmethod
    def user(option_size):
        try:
            print("-" * 40)
            out = input(COLOR.Green + "\tChoose your option [0..{0}] :".format(option_size - 1) + COLOR.END)

        except ValueError:
            print(COLOR.Red + "\tError! This option does not exist" + COLOR.END)
        return out

    def ask_user_to_exit(self):
        check = str(input(COLOR.Red + "\tDo you want to exit ? (y/n): " + COLOR.END)).lower().strip()
        try:
            if check[0] == 'y':
                return True
            elif check[0] == 'n':
                return False
            else:
                print(COLOR.Red + '\tInvalid Input' + COLOR.END)
                return self.ask_user_to_exit()
        except Exception as error:
            print(COLOR.Red + "\tPlease enter valid inputs" + COLOR.END)
            print(error)
            return self.ask_user_to_exit()

    def ask_user_to_import(self):
        check = str(input(COLOR.Red + "\tDo you want to import ? (y/n): " + COLOR.END)).lower().strip()
        try:
            if check[0] == 'y':
                return True
            elif check[0] == 'n':
                return False
            else:
                print(COLOR.Red + '\tInvalid Input' + COLOR.END)
                return self.ask_user_to_exit()
        except Exception as error:
            print(COLOR.Red + "\tPlease enter valid inputs" + COLOR.END)
            print(error)
            return self.ask_user_to_exit()

    def ask_user_to_rescale(self):
        rescale = input(
            COLOR.Green + "\tDo you want to RESCALE source images? Choose- [64, 128, 256], If not, press ENTER, or [Q] to exit" + COLOR.END)
        if rescale == "":
            return 512
        elif rescale.strip().isdigit():
            if int(rescale) == 256:
                return 256
            elif int(rescale) == 128:
                return 128
            elif int(rescale) == 64:
                return 64
            else:
                print(COLOR.Red + '\tInvalid Input. Choose again' + COLOR.END)
                return self.ask_user_to_rescale()
        elif rescale == 'q' or rescale == 'Q':
            return False
        else:
            print(COLOR.Red + "\tPlease enter valid inputs" + COLOR.END)
            return self.ask_user_to_rescale()

    def ask_user_to_generate_images(self):
        while True:
            numImages = input(COLOR.Green + "\t\tEnter number of images to generate in range [0,..., {}]: ".format(
                1000 - 1) + COLOR.END)
            if numImages.isdigit() and (int(numImages) >= 0 and int(numImages) < 1000):
                return int(numImages)
            else:
                print(COLOR.Red + "\t\t\tSelected number {} is not supported".format(
                    int(numImages)) + COLOR.END)

    def ask_user_to_chose_dataset(self):
        STR = [os.path.basename(f.path.replace("\\", "/")) for f in os.scandir(self.__pnt.data_dir) if f.is_dir()]
        print(STR)
        if not STR:
            print(COLOR.Red + "\tImport Data not found in folder:\t" + self.__pnt.data_dir + COLOR.END)
            return False
        s = ','.join(STR)
        if len(STR) == 1:
            s = "\tDo you want to load [" + s + "] ? Choose- [0], Or press [Q] to exit: "
        else:
            s = "\tDo you want to load [" + s + "] ? Choose- [0..{}], , Or press [Q] to exit: ".format(len(STR) - 1)
        check = (input(COLOR.Green + s + COLOR.END))
        if check.strip().isdigit():
            try:
                if int(check) == 0:
                    return STR[0]
                elif int(check) == 1:
                    return STR[1]
                elif int(check) == 2:
                    return STR[2]
                else:
                    print(COLOR.Red + '\tInvalid Input. Choose again' + COLOR.END)
                    return self.ask_user_to_chose_dataset()
            except Exception as error:
                print(COLOR.Red + "\tPlease enter valid inputs" + COLOR.END)
                print(error)
            return self.ask_user_to_chose_dataset()
        elif check == 'q' or check == 'Q':
            return False
        else:
            print(COLOR.Red + '\tInvalid Input. Chose again' + COLOR.END)
            return self.ask_user_to_chose_dataset()

    def ask_user2generateNumber(self, N):
        while True:

            numImages = input(COLOR.Green + "\t\tEnter number of images to generate in range [0,..., {}]: ".format(
                1000 - 1) + COLOR.END)

            if numImages.isdigit() and (int(numImages) >= 0 and int(numImages) < N):

                return int(numImages)
            else:
                print(COLOR.Red + "\t\t\tSelected number {} is not supported".format(int(numImages)) + COLOR.END)

    def print_menu(self, user_choice):
        print("-" * 40)
        for option in sorted(self.command.keys()):
            if user_choice is None:
                print(COLOR.Blue + "\t[{0}]\t\t{1}".format(option, self.command[option].label) + COLOR.END)
            elif option == user_choice:
                if user_choice == 0:
                    self.print_submenu(option, user_choice)
                elif user_choice == 1:
                    self.print_submenu(option, user_choice)
            else:
                print(COLOR.Blue + "\t[{0}]\t\t{1}".format("+", self.command[option].label) + COLOR.END)

    def print_submenu(self, option, user_choice):
        print(COLOR.BBlue + "\t[{0}]\t\t{1}".format("-", self.command[option].label) + COLOR.END)
        if user_choice == 0:
            for option in sorted(self.nested_command.keys()):
                print(COLOR.Blue + "\t\t[{0}]\t{1}".format(option, self.nested_command[option].label) + COLOR.END)
        elif user_choice == 1:
            for option in sorted(self.nested_command_1.keys()):
                print(COLOR.Blue + "\t\t[{0}]\t{1}".format(option, self.nested_command_1[option].label) + COLOR.END)

    def ask_user_to_chose_import_dataset(self):
        [print(f.path) for f in os.scandir('np') if f.is_file()]
        STR = [os.path.basename(f.path.replace("\\", "/")).split('.')[0] for f in os.scandir('np') if f.is_file()]
        # os.path.basename(f.path.replace("\\", "/"))
        print(STR)
        if not STR:
            print(COLOR.Red + "\tImport Data not found in folder:\t" + self.__pnt.data_dir + COLOR.END)
            return False
        s = ','.join(STR)
        if len(STR) == 1:
            s = "\tDo you want to load [" + s + "] ? Choose- [0], Or press [Q] to exit:"
        else:
            s = "\tDo you want to load [" + s + "] ? Choose- [0..{}], Or press [Q] to exit:".format(len(STR) - 1)
        check = (input(COLOR.Green + s + COLOR.END))
        if check.strip().isdigit():
            try:
                if int(check) == 0:
                    return STR[0]
                elif int(check) == 1:
                    return STR[1]
                elif int(check) == 2:
                    return STR[2]
                else:
                    print(COLOR.Red + '\tInvalid Input. Choose again' + COLOR.END)
                    return self.ask_user_to_chose_import_dataset()
            except Exception as error:
                print(COLOR.Red + "\tPlease enter valid inputs" + COLOR.END)
                print(error)
            return self.ask_user_to_chose_import_dataset()
        elif check == 'q' or check == 'Q':
            return False
        else:
            print(COLOR.Red + '\tInvalid Input. Chose again' + COLOR.END)
            return self.ask_user_to_chose_import_dataset()

    def option_import_data(self):
        s = self.ask_user_to_chose_dataset()
        if s == False:
            return False
        else:
            self.__pnt.list_dir2dict(data_dir=self.__pnt.data_dir, dataset=s)
            return True

    def option_export_data(self):
        if not self.__pnt.patient_slices:
            print(COLOR.Red + "\tNo  Data to export:\t" + self.__pnt.data_dir + COLOR.END)
            if self.ask_user_to_import():
                self.option_import_data()
        else:
            rescale = self.ask_user_to_rescale()
            print('\tRescale ' + str(rescale))
            self.__pnt.numpy_writer(Rescale=rescale, dir_name=self.path)

    def option_import_pseudonymized_data(self):
        s = self.ask_user_to_chose_import_dataset()
        if s == False:
            return False
        else:
            print(s)
            self.__pnt.coll_dict(dataset=s)

    def option_sample_plot(self, data_type):
        if data_type == "Pseudonymized":
            self.__pnt.slice_plot(fig_title='Random source plot', Random=True,dir_name=self.path)
        elif data_type == "Generated":
            pass
        else:
            pass

    def option_generate_pseudonymized_data(self):
        num = self.ask_user2generateNumber(N=1000)
        train.main()

    #        misc.init_output_logging()
    #       np.random.seed(config.random_seed)

    #      tfutil.init_tf(config.tf_config)
    # print('Running %s()...of %s ....%s images' % (config.train['func'],config.train['run_id'], config.train['num_pngs']))

    #     num_gpus = 1;
    #    desc = 'camelyon-fake-images'
    #   tfutil.call_func_by_name(
    #      **config.EasyDict(func='pcgan.util_scripts.generate_fake_images', run_id='camelyon', num_pngs=int(num)))
    # print('Exiting...')

    def ui_selection(self):

        i, j = None, None
        while True:
            self.print_menu(user_choice=i)
            user_i = self.user(option_size=len(self.command))
            if user_i.isdigit():
                i = int(user_i)
                if i == 0:
                    while True:
                        self.print_menu(user_choice=i)
                        user_j = self.user(option_size=len(self.nested_command))
                        if user_j.isdigit():
                            j = int(user_j)
                            if j == 0:
                                self.option_import_data()
                            elif j == 1:
                                self.option_export_data()
                            elif j == 2:
                                self.option_import_pseudonymized_data()
                            elif j == 3:
                                self.option_sample_plot(data_type="Pseudonymized")
                            elif j == 4:
                                # print('Back')
                                i, j = None, None
                                break
                            else:
                                print(COLOR.Red + "That is not an option:" + COLOR.END)
                        else:
                            print(COLOR.Red + "That is not an option:" + COLOR.END)
                elif i == 1:
                    while True:
                        self.print_menu(user_choice=i)
                        user_j = self.user(option_size=len(self.nested_command_1))
                        if user_j.isdigit():
                            j = int(user_j)
                            if j == 0:
                                self.option_generate_pseudonymized_data()
                            elif j == 1:
                                self.option_sample_plot(data_type="Generated")
                            elif j == 2:
                                # print('Back')
                                i, j = None, None
                                break
                            else:
                                print(COLOR.Red + "That is not an option:" + COLOR.END)
                        else:
                            print(COLOR.Red + "That is not an option:" + COLOR.END)
                elif i == 2:
                    if self.ask_user_to_exit():
                        print(COLOR.Red + "Exit" + COLOR.END)
                        quit()
            else:
                print(COLOR.Red + "That is not an option:" + COLOR.END)
