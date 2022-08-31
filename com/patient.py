import random
import numpy as np
import cv2
import os
from com.color import COLOR
import json
import matplotlib
import matplotlib.pyplot as plt
import pydicom
import pandas as pd
from com.dcom import BYTE
from com.dcom import DCM, DCM_TAG
from com.dcom import TAGS
import csv
import time



matplotlib.use('Agg')

timestr = time.strftime("_%Y%m%d_%H%M%S")


# from matplotlib.widgets import Button


def file_existed(filename):


    try:
        f = open(filename)
        print(COLOR.Green + filename + " created" + COLOR.END)
        f.close()
        return 1
    except IOError:
        print(COLOR.Red + "File not accessible" + COLOR.END)
        return 0


class PATIENTS:

    def __init__(self, args):
        for key, value in args._get_kwargs():
            # if value is not None:
            print("{0} = {1}".format(key, value))

        self.data_dir = args.input
        self.dataset = args.dataset
        self.plot = args.plot
        self.resolution = args.resolution
        self.script_dir = os.path.dirname(os.path.realpath('__file__'))
        self.json_dir = "json"
        self.np_dir = "np"
        self.__dcm = BYTE()
        self.patient_slices = []
        self.slices = []
        self.dict_CSV = {}
        # self.list_dir2dict(data_dir, dataset)

    def dcom_tags(self):
        self.TransferSyntaxUID = None
        self.MediaStorageSOPClassUID = None
        self.ImplementationClassUID = None
        self.ImplementationVersionName = None

    def list_dir2dict(self, data_dir, dataset):

        self.json_filename = dataset + "_info.json"
        self.dataset = dataset
        self.slices = []
        self.patient_slices = []
        self.patient_dict = {}
        self.patients = []
        self.patients_path = []
        self.data_dir = data_dir
        self.name_of_dataset = dataset
        self.heador = []
        self.keys = []

        i = 0
        print(COLOR.Blue + "\tPatient Dict start", self.data_dir, self.name_of_dataset + COLOR.END)
        for pos, value in enumerate(os.listdir(self.data_dir)):
            if os.listdir(self.data_dir)[pos] == self.name_of_dataset:
                data_path = os.path.join(self.data_dir, os.listdir(self.data_dir)[pos])
                # print(i, data_path)
                for it in os.scandir(data_path):
                    if it.is_dir():
                        self.patient_slices.append([])
                        self.patients_path.append(it.path)
                        self.patients.append(os.path.basename(it.path))
                        print('\tPatient:', i)
                        self.list_subdir(patient=self.patients[-1], path=self.patients_path[-1], i=i)
                        i = i + 1
        print(COLOR.Green + "Patient Dict done" + COLOR.END)
        self.dict_to_json()
        self.patient_slices_print()

    def list_subdir(self, patient, path, i):
        self.patient_dict[i] = {}
        self.patient_dict[i]["id"] = patient
        self.patient_dict[i]["path"] = path
        self.patient_dict[i]["image"] = {}
        J = 0
        self.patient_dict[i]["image"][J] = {}
        l = []
        folder = False
        for j, value in enumerate(os.listdir(self.patients_path[-1])):
            v = os.path.join(self.patients_path[-1], value)
            if os.path.isdir(v):
                self.patient_dict[i]["image"][J] = {}
                folder = True
                for x, _, images in os.walk(os.path.join(self.patients_path[-1], value)):
                    images.sort()  # sort files by name
                    self.patient_dict[i]["image"][J] = images
                print('\t\tImage', J, 'slices', len(images))
                self.patient_slices[i].append([pydicom.dcmread(x + "/" + s) for s in os.listdir(x)])
                J += 1
            else:
                folder = False
                l = l + (list(value.split(" ")))
        if not folder:
            l.sort()
            print('\t\tImage', J, 'slices', len(l))
            self.patient_dict[i]["image"][J] = l
            self.patient_slices[i].append([pydicom.dcmread(self.patients_path[-1] + '/' + s) for s in l])

    def patient_slices_print(self):
        print(COLOR.Blue + "Patient Dict check start" + COLOR.END)
        for i in range(len(self.patient_slices)):
            # getIm = len(self.patient_slices[i])
            for j in range(len(self.patient_slices[i])):
                getSlices = len(self.patient_slices[i][j])
                print("Patient size", len(self.patient_slices), "Patient", i, "Image", j, 'getSlices', getSlices)
        print(COLOR.Green + "Patient Dict check done" + COLOR.END)

    def slices_size(self):
        self.NumP = len(self.slices)
        return self.NumP

    def dict_to_numpy(self):
        # Save loaded images in npy format
        print(COLOR.Red + 'Dict to numpy array' + COLOR.END)

        self.dir_existed(self.np_dir)

        for i in range(len(self.slices)):
            for j in range(len(self.slices[i])):
                if len(self.slices[i][j]) > 1:
                    s = self.dataset + f'_{i:03d}' + f'_{j:03d}' + '.npy'
                    np_name = os.path.join(os.path.join(self.script_dir, self.np_dir, s))
                    if not self.file_existed(np_name):
                        image = np.stack([s.pixel_array for s in self.slices[i][j]])

                        with open(np_name, 'wb') as f:
                            np.save(f, image)
                    print(np_name)

    def dict_to_json(self):
        json_name = os.path.join(os.path.join(self.script_dir, self.json_dir, self.json_filename))
        self.dir_existed(self.json_dir)
        with open(json_name, 'w') as f:
            json.dump(self.patient_dict, f, indent=4)
        self.file_existed(json_name)

    def numpy_writer(self, Rescale):
        def dcm_value(slices, i, j, k):
            keys, value = [], []
            for key in slices[i][j][k].file_meta.keys():
                keys.append(key)
                value.append(key.group.to_bytes(2, 'big') + key.element.to_bytes(2, 'big'))
            for key in slices[i][j][k].keys():
                keys.append(key)
                value.append(key.group.to_bytes(2, 'big') + key.element.to_bytes(2, 'big'))
            return keys, value

        def dcm_scale_down(slices, scale):
            return cv2.resize(np.array(slices), (scale, scale), interpolation=cv2.INTER_AREA)

        def np_file_writer(dataset, data):
            print(COLOR.Blue + ' Dict to numpy array...' + COLOR.END)
            s = dataset + timestr
            numpy_dir = "np"
            if not os.path.exists(os.path.join(self.script_dir, numpy_dir)):
                os.makedirs(numpy_dir)
            # name = os.path.join(os.path.join(self.script_dir, numpy_dir, s + '.npy'))
            np_name = os.path.join(os.path.join(self.script_dir, numpy_dir, dataset + '.npy'))
            if not file_existed(np_name):
                with open(np_name, 'wb') as f:
                    np.save(f, data)
                # shutil.copy(name, np_name)
                f.close()
            print("NP Done", np_name)

        def csv_file_writer(dataset, dict):
            print(COLOR.Blue + ' Dict to CSV...' + COLOR.END)
            s = dataset + timestr
            csv_dir = "csv"
            if not os.path.exists(os.path.join(self.script_dir, csv_dir)):
                os.makedirs(csv_dir)
            # csv_name_patient = os.path.join(os.path.join(self.script_dir, csv_dir, s + '.csv'))
            csv_name = os.path.join(os.path.join(self.script_dir, csv_dir, dataset + '.csv'))
            print(csv_name)
            # print(dict.keys())
            with open(csv_name, 'w', newline="") as csv_file_patient:
                w = csv.writer(csv_file_patient, delimiter=',')
                w.writerow(dict.keys())
                w.writerows(zip(*dict.values()))
                # w.writerows(zip(*dict.values()))
            # csv_name = os.path.join(os.path.join(self.script_dir, csv_dir, dataset + '.csv'))
            # shutil.copy(csv_name_patient, csv_name)
            csv_file_patient.close()
            print("CSV Done", csv_name)

        print(COLOR.Blue + ' Pars dict...' + COLOR.END)
        __bt = BYTE()

        TAGS.CTPI = []

        TAGS.dict_CSV = {}

        print(len(self.patient_slices))
        for i in range(len(self.patient_slices)):
            P = []
            for j in range(len(self.patient_slices[i])):
                for k in range(len(self.patient_slices[i][j])):
                    keys, value = dcm_value(slices=self.patient_slices, i=i, j=j, k=k)
                    if __bt.byte2concat(DCM.SOP, DCM.MODALITY) in value:
                        if self.patient_slices[i][j][k].Modality == "CT":
                            P.append(dcm_scale_down(self.patient_slices[i][j][k].pixel_array, Rescale))
                            TAGS.Rows.append(self.patient_slices[i][j][k].Rows)
                            TAGS.Columns.append(self.patient_slices[i][j][k].Rows)
                            TAGS.Patient.append(i)
                            TAGS.Image.append(j)
                            TAGS.Slices.append(k)

                            if __bt.byte2concat(b"\x00\x20", b"\x00\x10") in value:
                                TAGS.StudyID.append(self.patient_slices[i][j][k].StudyID)
                            else:
                                TAGS.StudyID.append(None)

                            if __bt.byte2concat(b"\x00\x18", b"\x11\x52") in value:
                                TAGS.Exposure.append(self.patient_slices[i][j][k].ExposureTime)
                            else:
                                TAGS.Exposure.append(None)

                            if __bt.byte2concat(b"\x00\x20", b"\x00\x13") in value:
                                TAGS.Instance_Number.append(self.patient_slices[i][j][k].InstanceNumber)
                            else:
                                TAGS.Instance_Number.append(None)

                            if __bt.byte2concat(b"\x00\x20", b"\x00\x12") in value:
                                TAGS.Acquisition_Number.append(self.patient_slices[i][j][k].AcquisitionNumber)
                            else:
                                TAGS.Acquisition_Number.append(None)

                            if __bt.byte2concat(b"\x00\x20", b"\x10\x41") in value:
                                TAGS.SliceLocation.append(self.patient_slices[i][j][k].SliceLocation)
                            else:
                                TAGS.SliceLocation.append(None)

                            if __bt.byte2concat(b"\x00\x28", b"\x00\x30") in value:
                                TAGS.Pixel_Spacing.append([self.patient_slices[i][j][k].PixelSpacing[0]] +
                                                          [self.patient_slices[i][j][k].PixelSpacing[1]])
                            else:
                                TAGS.Pixel_Spacing.append(None)

                            if __bt.byte2concat(b"\x00\x10", b"\x00\x20") in value:
                                TAGS.PatientID.append(self.patient_slices[i][j][k].PatientID)
                            else:
                                TAGS.PatientID.append(None)

                            if __bt.byte2concat(DCM_TAG.GR.GR0010, DCM_TAG.EL.EL0040) in value:
                                TAGS.PatientSex.append(self.patient_slices[i][j][k].PatientSex)
                            else:
                                TAGS.PatientSex.append(None)

                            if __bt.byte2concat(DCM_TAG.GR.GR0010, DCM_TAG.EL.EL1010) in value:
                                TAGS.PatientAge.append(self.patient_slices[i][j][k].PatientAge)
                            else:
                                TAGS.PatientAge.append(None)

                            if (__bt.byte2concat(DCM.SOP, DCM.STUDY_DESCRIPTION) in value):
                                TAGS.StudyDescription.append(str(self.patient_slices[i][j][k].StudyDescription))
                            else:
                                TAGS.StudyDescription.append(None)

                            if (__bt.byte2concat(DCM.META, DCM.TRANS_SYNTAX_UID) in value):
                                TAGS.TransferSyntaxUID.append(self.patient_slices[i][j][k].file_meta.TransferSyntaxUID)
                            else:
                                TAGS.TransferSyntaxUID.append(None)

                            if (__bt.byte2concat(b"\x00\x18", b"\x00\x15") in value):
                                TAGS.Body_Part.append(self.patient_slices[i][j][k].BodyPartExamined)
                            else:
                                TAGS.Body_Part.append(None)

                            if k == 0 and (__bt.byte2concat(DCM.META, DCM.META_STORAGE_SOP_INST_UID) in value):
                                TAGS.MediaStorageSOPClassUID.append(
                                    self.patient_slices[i][j][k].file_meta.MediaStorageSOPClassUID.name)
                            else:
                                TAGS.MediaStorageSOPClassUID.append(None)

            V_Image = np.stack(P)
            TAGS.CTPI = TAGS.CTPI + P
            print(V_Image.ndim, V_Image.shape, len(V_Image), np.size(V_Image))

        CTPI_Image = np.stack(TAGS.CTPI)
        print("-" * 40)
        print("\tDict:", 'Patients:', CTPI_Image.ndim, 'Shape:', CTPI_Image.shape, "Num of Slices:", len(CTPI_Image))
        print("-" * 40)
        np_file_writer(self.dataset, CTPI_Image)
        TAGS.dict_CSV["StudyID"] = TAGS.StudyID
        TAGS.dict_CSV["Patient"] = TAGS.Patient
        TAGS.dict_CSV["Image"] = TAGS.Image
        TAGS.dict_CSV["Slices"] = TAGS.Slices
        TAGS.dict_CSV["Exposure"] = TAGS.Exposure
        TAGS.dict_CSV["Rows"] = TAGS.Rows
        TAGS.dict_CSV["Columns"] = TAGS.Columns
        TAGS.dict_CSV["Pixel_Spacing"] = TAGS.Pixel_Spacing
        TAGS.dict_CSV["Instance_Number"] = TAGS.Instance_Number
        TAGS.dict_CSV["Acquisition_Number"] = TAGS.Acquisition_Number
        TAGS.dict_CSV["SliceLocation"] = TAGS.SliceLocation
        TAGS.dict_CSV["Body_Part"] = TAGS.Body_Part
        self.dict_CSV = TAGS.dict_CSV
        csv_file_writer(self.dataset, TAGS.dict_CSV)

    def coll_dict(self, dataset):

        def csv_file_reader(srcipt_dir, dataset, dict):
            print(COLOR.Blue + ' CSV to Dict...' + COLOR.END)
            s = dataset
            csv_dir = "csv"
            if not os.path.exists(os.path.join(srcipt_dir, csv_dir)):
                print('CSV did find')
                return
            else:
                csv_name_patient = os.path.join(os.path.join(srcipt_dir, csv_dir, s + '.csv'))
                try:
                    dict = pd.read_csv(csv_name_patient)
                    print(dict.head(5))
                except IOError:
                    print(COLOR.Red, 'Unable to load "%s".  Check if its exist.' % csv_name_patient, COLOR.END)
                    return
                    # Read the header row and create the dictionary from it.
                return dict

        def np_file_reader(srcipt_dir, dataset, data):
            print(COLOR.Blue + ' Numpy to Dict...' + COLOR.END)
            numpy_dir = "np"
            if not os.path.exists(os.path.join(srcipt_dir, numpy_dir)):
                print('NP did find')
                return
            else:
                np_name = os.path.join(os.path.join(srcipt_dir, numpy_dir, dataset + '.npy'))
                try:
                    data = np.array(np.load(np_name))
                    print("-" * 40)
                    print("\tDict:", 'Patients:', data.ndim, 'Shape:', data.shape, "Num of Slices:",
                          len(data))
                    print("-" * 40)

                except IOError:
                    print(COLOR.Red, 'Unable to load "%s".  Check that it exists.' % np_name, COLOR.END)
                    return
                    # Read the header row and create the dictionary from it.

                return data

        self.dict_CSV = {}
        self.dict_CSV = csv_file_reader(srcipt_dir=self.script_dir, dataset=dataset, dict=self.dict_CSV)
        self.slices = []
        self.slices = np_file_reader(srcipt_dir=self.script_dir, dataset=dataset, data=self.slices)

    def dir_existed(self, dir_name):

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(COLOR.Red + "Directory " + dir_name + " created" + COLOR.END)
        else:
            print(COLOR.Blue + "Directory " + dir_name + " already created" + COLOR.END)

    def file_existed(self, filename):
        try:
            f = open(filename)
            print(COLOR.Green + filename + " created at " + COLOR.END + time.ctime(os.path.getctime(filename)))
            f.close()
            return 1
        except IOError:
            print(COLOR.Red + "File not accessible" + COLOR.END)
            return 0

    def patient_Info(self):
        self.NumP = self.slices_size()
        return False, True

    def slice_plot(self, fig_title, Random):
        def figure_save(dataset):
            print(COLOR.Blue + ' Safe figure...' + COLOR.END)
            s = dataset + timestr
            figure_dir = "figure"
            if not os.path.exists(os.path.join(self.script_dir, figure_dir)):
                os.makedirs(figure_dir)
            figure_fname = os.path.join(os.path.join(self.script_dir, figure_dir, s + '.pdf'))
            return figure_fname

        if self.slices == []:
            print(COLOR.Red + "Patient list is empty or corrupted" + COLOR.END)
            return
        else:
            print("\tDict:", 'Patients:', self.slices.ndim, 'Shape:', self.slices.shape, "Num of Slices:")
            # w = self.slices.shape[1]
            # h = self.slices.shape[2]
            fig = plt.figure(fig_title, figsize=(30, 20), dpi=80)
            if Random:
                for num in range(20):
                    r = random.randint(0, len(self.slices))
                    ax = fig.add_subplot(4, 5, num + 1)
                    s = r, " Slice: " + str(self.dict_CSV["SliceLocation"][r])
                    ax.set_title(s, fontsize=10, color='red')
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    textstr = '\n'.join((
                        r'$Patient= %s$' % (self.dict_CSV["StudyID"][r],),
                        r'$BodyPart= %s$' % (self.dict_CSV["Body_Part"][r],),
                        r'$InstNumber= %d$' % (self.dict_CSV["Instance_Number"][r],),
                        r'Exposure= %f[mAsec]$' % (self.dict_CSV["Exposure"][r],),
                        r'$Slice= %s$' % (self.dict_CSV["SliceLocation"][r])))
                    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=8,
                            verticalalignment='top', bbox=props)

                    ax.imshow(self.slices[r], cmap='gray')
                    ax.set_aspect('equal')
                self.dir_existed(dir_name="figure")
                plt.savefig(figure_save(self.dataset))

            else:
                pass
            # plt.show()
