from com.color import COLOR
from collections import namedtuple
#from SCAPIS_AIDA.com.patient import PATIENTS
#from pcgan import misc, config, tfutil

import numpy as np
#from pars.parser import STR


class MENU:
    def __init__(self, args):
        Option = namedtuple('Option', 'label')

        s = ','.join(STR)
        self.command = {0: Option("Download DCOM images from [" + s + "] into the Dictionary and create JSON"),
                        1: Option("Save Dictionary into Numpy and CSV"),
                        2: Option("Load Dictionary from Numpy and CSV"),
                        3: Option("Plot random Slices"),
                        4: Option("Show slices Info"),
                        5: Option("Hounsfield Units (HU)"),
                        6: Option("OpenGL show in 3D"),
                        7: Option("Generate Images by PCGAN"),
                        8: Option("Exit")}
        self.__pnt = args

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


    def ask_user_to_chose_dataset(self, STR):
        s = ','.join(STR)
        check = (input(COLOR.Green + "\tDo you want to load [" + s + "] ? Choose- [0..2]: " + COLOR.END))  # .lower().strip()
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
                    return self.ask_user_to_chose_dataset(STR)
            except Exception as error:
                print(COLOR.Red + "\tPlease enter valid inputs" + COLOR.END)
                print(error)
            return self.ask_user_to_exit()
        else:
            print(COLOR.Red + '\tInvalid Input. Chose again' + COLOR.END)
            return self.ask_user_to_chose_dataset(STR)

    def ask_user_to_resize(self):
        check = str(input(COLOR.Red + "\tImage will resize to [128x128], Are you agree? (y/n): " + COLOR.END)).lower().strip()
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


    def print_menu(self):
        print("-" * 40)
        for option in sorted(self.command.keys()):
            print(COLOR.Blue + "\t[{0}]\t\t{1}:".format(option, self.command[option].label) + COLOR.END)

    def ui_selection(self):

        def user():
            try:
                print("-" * 40)
                out = input(COLOR.Green + "\tChoose your option: " + COLOR.END)

            except ValueError:
                print(COLOR.Red + "\tError! This option does not exist" + COLOR.END)
            return out

        while True:
            self.print_menu()
            user_p = user()
            if user_p.isdigit():
                i = int(user_p)
                if i == 0:
                    #print('\t\tExecuting menu item 0')
                    self.Option0()

                elif int(user_p) == 1:
                    self.Option1()


                elif int(user_p) == 2:
                    self.Option2()


                elif int(user_p) == 3:
                    self.Option3()


                elif int(user_p) == 4:
                    self.Option4()
                    print('Executing menu item 4')
                elif int(user_p) == 5:
                    self.Option5()

                elif int(user_p) == 6:
                    self.Option6()

                elif int(user_p) == 7:
                    self.Option7()
                elif int(user_p) == 8:
                    if self.ask_user_to_exit():
                        print(COLOR.Red + "Exit" + COLOR.END)
                        quit()
            else:
                print(COLOR.Red + "That is not an option:" + COLOR.END)

    def Option0(self):
        '''
        Download images into the dictionary and json
        :return:
        '''
        s = self.ask_user_to_chose_dataset(STR=STR)
        #print(s)
        # self.list_dir2dict(data_dir, dataset)
        #print('self.__pnt.data_dir', self.__pnt.data_dir)
        #print('dataset', s)
        self.__pnt.list_dir2dict(data_dir=self.__pnt.data_dir, dataset=s)

    def Option1(self):
        def ask2rescale():
            check = (input(COLOR.Green + "\tDo you want to RESCALE source images? Choose- [64, 128, 256]: " + COLOR.END))  # .lower().strip()
            if check.strip().isdigit():
                try:
                    if int(check) == 256:
                        return 256
                    elif int(check) == 128:
                        return 128
                    elif int(check) == 64:
                        return 64
                    else:
                        print(COLOR.Red + '\tInvalid Input. Choose again' + COLOR.END)
                        return ask2rescale()

                except Exception as error:
                    print(COLOR.Red + "\tPlease enter valid inputs" + COLOR.END)
                    print(error)
                    return ask2rescale()
            else:
                print(COLOR.Red + '\tInvalid Input. Chose again' + COLOR.END)
                return ask2rescale()


        '''
        Dictionary to numpy
        :return:
        '''


        if self.__pnt.patient_slices == []:
            print(COLOR.Red + "Patient list is empty or corrupted"+COLOR.END)
            self.Option0()

        s = ask2rescale()
        print('\tRescale ' + str(s))
        self.__pnt.numpy_writer(Rescale=s)

        print('111111114')
    def Option2(self):
        def ask_user_to_chose_numpi_csv():
            s = ','.join(STR)
            check = (input(
                COLOR.Green + "\tDo you want to load [" + s + "] dataset ? Choose- [0..2]: " + COLOR.END))  # .lower().strip()
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
                        return self.ask_user_to_chose_dataset(STR)
                except Exception as error:
                    print(COLOR.Red + "\tPlease enter valid inputs" + COLOR.END)
                    print(error)
                return self.ask_user_to_exit()
            else:
                print(COLOR.Red + '\tInvalid Input. Chose again' + COLOR.END)
                return self.ask_user_to_chose_dataset(STR)
        '''
        numpy to Dictionary
        :return:
        '''
        #self.__pnt.numpy_writer(256)
        s = ask_user_to_chose_numpi_csv()
        print(s)
        self.__pnt.coll_dict(dataset=s)

    def Option3(self):
        '''
        Plot slices randomly from the Dictionary
        '''
        #self.__pnt.numpy_writer(256)
        self.__pnt.slice_plot(fig_title='Random source plot', Random=True)



    def Option4(self):
        """Get nmuber of pationts"""

        #Patient, Image, Slice = self.ask_2choose_patient()
        print(COLOR.Red + "Option removed. You have a look csv file" + COLOR.END)


    def Option5(self):

        from com.dcom import HOU
        __hou = HOU()
        __hou.num = __hou.ask_user_to_plot_hou(slices=self.__pnt.slices)
        print(__hou.num)
        if __hou.num != None:
            __hou.houndsfield_units(slices=self.__pnt.slices, dict_CSV=self.__pnt.dict_CSV, num=__hou.num)


    def Option6(self):

        print(COLOR.Red + "Option removed" + COLOR.END)

    def ask_2choose_patient(self):
        while True:
            """Get nmuber of pationts"""
            self.NumP = len(self.__pnt.patient_slices)
            while True:
                getPatient = input(
                    COLOR.Green + "\t\tEnter patient' number in range [0,..., {}]: ".format(self.NumP-1) + COLOR.END)

                if getPatient.isdigit() and (int(getPatient) >= 0 and int(getPatient) < self.NumP):
                    while True:
                        getPatientImage = input(
                            COLOR.Green + "\t\tEnter {} patient' image in range [0,..., {}]: ".format(getPatient, len(
                                self.__pnt.patient_slices[int(getPatient)]) - 1) + COLOR.END)

                        if getPatientImage.isdigit() and (int(getPatientImage) >= 0 and (
                                int(getPatientImage) < int(len(self.__pnt.patient_slices[int(getPatient)])))):

                            while True:
                                if len(self.__pnt.patient_slices[int(getPatient)][int(getPatientImage)]) - 1 == 0:
                                    getPatientImageSlice = "0"
                                    print(COLOR.Green + "\t\tSellected slice " + getPatientImageSlice + COLOR.END)
                                    #print(getPatient, len(self.__pnt.patient_slices[int(getPatient)]), str(self.NumP),
                                    #      len(self.__pnt.patient_slices[int(getPatient)][int(getPatientImage)]),
                                    #      int((getPatientImageSlice)))
                                    return int(getPatient), int(getPatientImage), int(getPatientImageSlice)
                                else:
                                    S = "\t\tEnter Number of Slice' in range [0,..., {}]: "
                                    getPatientImageSlice = input(COLOR.Green + S.format(
                                        len(self.__pnt.patient_slices[int(getPatient)][int(getPatientImage)]) - 1) + COLOR.END)
                                    if getPatientImageSlice.isdigit() and (int(getPatientImageSlice) >= 0 and (
                                            int(getPatientImageSlice) < int(
                                        len(self.__pnt.patient_slices[int(getPatient)][int(getPatientImage)])))):
                                        #print(getPatient, len(self.__pnt.patient_slices[int(getPatient)]), str(self.NumP),
                                        #      len(self.__pnt.patient_slices[int(getPatient)][int(getPatientImage)]),
                                        #      int((getPatientImageSlice)))

                                        return int(getPatient), int(getPatientImage), int(getPatientImageSlice)
                                    else:
                                        print(
                                            COLOR.Red + "\t\t\tSelected Slice in {} image in {} patient does not exist".format(
                                                int(getPatient), int(getPatientImage)) + COLOR.END)

                        else:
                            print(COLOR.Red + "\t\t\tSelected image in {} patient does not exist".format(
                                int(getPatient)) + COLOR.END)

                else:
                    print(COLOR.Red + "\t\t\tThis patient number does not exist" + COLOR.END)


    def all_patients_and_slices(self):
        # NumP = self.__pnt.slices_size()
        for i in range(len(self.__pnt.slices)):
            print(COLOR.Green + "\t\tPatient: [{}]\t\t Slices: {}".format(i, len(self.__pnt.slices[i])) + COLOR.END)

    def Option7(self):

        num = self.ask_user2generateNumber()

        misc.init_output_logging()
        np.random.seed(config.random_seed)

        tfutil.init_tf(config.tf_config)
        #print('Running %s()...of %s ....%s images' % (config.train['func'],config.train['run_id'], config.train['num_pngs']))


        num_gpus = 1;
        desc = 'camelyon-fake-images'
        tfutil.call_func_by_name(** config.EasyDict(func='util_scripts.generate_fake_images', run_id='camelyon', num_pngs=int(num)))
        print('Exiting...')

    def ask_user2generateNumber(self):
        while True:
            """Get nmuber of pationts"""
            numImages = input(
                    COLOR.Green + "\t\tEnter number of images to generate in range [0,..., {}]: ".format(1000 - 1) + COLOR.END)

            if numImages.isdigit() and (int(numImages) >= 0 and int(numImages) < 1000):

                return  int(numImages)
            else:
                print(COLOR.Red + "\t\t\tSelected number {} is not supported".format(
                    int(numImages)) + COLOR.END)