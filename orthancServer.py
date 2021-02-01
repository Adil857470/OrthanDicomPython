import requests
import sys
import cv2
import pydicom
import pyodbc
import numpy as np


host = 'http://182.156.200.179:8042'
link = 'http://182.156.200.179:8042/patients'
f = requests.get(link)
all_patient_id_index = f.json()
# print(all_patient_id_index)
patientNameOrID = input("Enter Patient Name or Id to searched: ")
patientNameOrID = patientNameOrID.upper()
conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=182.156.200.178;DATABASE=python;UID=sa;PWD=elmcindia786@')
insert = conn.cursor()
try:
    print(int(patientNameOrID))
    sql = "SELECT dcmID from python.dbo.dicom where PID='" + str(patientNameOrID) + "'"
    check = insert.execute(sql)
    a = check.fetchall()
    try:
        dcmID = a[0][0]
    except:
        x = "This PID/Name is not valid!"
        sys.exit(x)
    nmb = True
except:
    sql = "SELECT dcmID from python.dbo.dicom where patientName LIKE'%" + str(patientNameOrID) + "%'"
    check = insert.execute(sql)
    a = check.fetchall()
    try:
        dcmID = a[0][0]
    except:
        x = "This PID/Name is not valid!"
        sys.exit(x)
    nmb = False
print(dcmID)
singlePatientDetails = link + '/' + dcmID
singlePatientDetails = requests.get(singlePatientDetails)
singlePatientDetails = singlePatientDetails.json()
patientId = singlePatientDetails['MainDicomTags']['PatientID']
# ________________patient ID_________________________________________
# print(patientId)
# ________________patient ID_________________________________________
name = patientNameOrID
"for fetching name"
# __________________________________________________________________________________________________________________
patientName = singlePatientDetails['MainDicomTags']['PatientName']
filterName = patientName.split('^')
# patientNameSave = filterName[0]
try:
    patientName = filterName[0] + ' ' + filterName[1]
    try:
        patientNameSave = filterName[0] + '' + filterName[1]
    except:
        pass
    # ________________patient NAME_________________________________________
    print(patientName)
    # ________________patient NAME_________________________________________
    print("studies available:", singlePatientDetails['Studies'])
except:
    # patientNameSave = filterName[0]
    pass

# __________________________________________________________________________________________________________________
if nmb == True:
    patientStudy = host + '/studies/' + singlePatientDetails['Studies'][0]
    patientStudy = requests.get(patientStudy)
    patientStudy = patientStudy.json()
    patientSeries = patientStudy['Series']
    print("data series available: ", len(patientSeries))
    patientSeriesData = host + '/series/' + patientSeries[0]
    patientSeriesData = requests.get(patientSeriesData)
    patientSeriesData = patientSeriesData.json()
    patientSeriesData = (patientSeriesData['Instances'])

    patientDicomFile = host + '/instances/' + patientSeriesData[0] + '/file'
    patientDicomFile = requests.get(patientDicomFile)
    try:
        open('ERADCM/' + patientNameSave + '.dcm', 'wb').write(patientDicomFile.content)
        filename = 'ERADCM/' + patientNameSave + '.dcm'
        dataset = pydicom.dcmread(filename)
        print("dataset: ", dataset)
        arr = np.array(dataset.pixel_array)
        jsonDat = {}
        try:
            for i in dataset:
                dat = str(i).split('     ')
                # print(dat[0],     dat[len(dat)-1])
                jData = {"'" + dat[0] + "'": dat[len(dat) - 1]}
                # load = json.load(jsonDat)
                jsonDat.update(jData)
            data = (jsonDat)
            # return Response(dat)
        except Exception as e:
            print(e)
            pass

        patientDicomFileIMG = host + '/instances/' + patientSeriesData[0] + '/preview'
        patientDicomFileIMG = requests.get(patientDicomFileIMG)
        open('dcmimg.png', 'wb').write(patientDicomFileIMG.content)
        img = cv2.imread('dcmimg.png')
        res = cv2.resize(img, (480, 500))
        is_success, im_buf_arr = cv2.imencode(".png", res)
        byte_im = im_buf_arr.tobytes()
        cv2.imwrite("ERADCMIMG/" + patientNameSave + ".png", res)
        print("done with name")
        data = {'image': str(byte_im), 'Details': str(jsonDat)}
    except:
        open('ERADCM/' + str(patientNameOrID) + '.dcm', 'wb').write(patientDicomFile.content)
        filename = 'ERADCM/' + str(patientNameOrID) + '.dcm'
        dataset = pydicom.dcmread(filename)
        print("dataset: ", dataset)
        arr = np.array(dataset.pixel_array)
        jsonDat = {}
        try:
            for i in dataset:
                dat = str(i).split('     ')
                # print(dat[0],     dat[len(dat)-1])
                jData = {"'" + dat[0] + "'": dat[len(dat) - 1]}
                # load = json.load(jsonDat)
                jsonDat.update(jData)
            data = (jsonDat)
            # return Response(dat)
        except Exception as e:
            # print(e)
            pass

        patientDicomFileIMG = host + '/instances/' + patientSeriesData[0] + '/preview'
        patientDicomFileIMG = requests.get(patientDicomFileIMG)
        open('dcmimg.png', 'wb').write(patientDicomFileIMG.content)
        img = cv2.imread('dcmimg.png')
        res = cv2.resize(img, (480, 500))
        is_success, im_buf_arr = cv2.imencode(".png", res)
        byte_im = im_buf_arr.tobytes()
        cv2.imwrite("ERADCMIMG/" + str(patientNameOrID) + ".png", res)
        print("done with name")
        data = {'image': str(byte_im), 'Details': str(jsonDat)}
elif nmb == False:
    patientStudy = host + '/studies/' + singlePatientDetails['Studies'][0]
    patientStudy = requests.get(patientStudy)
    patientStudy = patientStudy.json()
    patientSeries = patientStudy['Series']
    print("data series available: ", len(patientSeries))
    patientSeriesData = host + '/series/' + patientSeries[0]
    patientSeriesData = requests.get(patientSeriesData)
    patientSeriesData = patientSeriesData.json()
    patientSeriesData = (patientSeriesData['Instances'])

    patientDicomFile = host + '/instances/' + patientSeriesData[0] + '/file'
    patientDicomFile = requests.get(patientDicomFile)
    try:
        open('ERADCM/' + patientNameSave + '.dcm', 'wb').write(patientDicomFile.content)
        filename = 'ERADCM/' + patientNameSave + '.dcm'
        dataset = pydicom.dcmread(filename)
        print("dataset: ", dataset)
        arr = np.array(dataset.pixel_array)
        jsonDat = {}
        try:
            for i in dataset:
                dat = str(i).split('     ')
                # print(dat[0],     dat[len(dat)-1])
                jData = {"'" + dat[0] + "'": dat[len(dat) - 1]}
                # load = json.load(jsonDat)
                jsonDat.update(jData)
            data = (jsonDat)
            # return Response(dat)
        except Exception as e:
            # print(e)
            pass

        patientDicomFileIMG = host + '/instances/' + patientSeriesData[0] + '/preview'
        patientDicomFileIMG = requests.get(patientDicomFileIMG)
        open('dcmimg.png', 'wb').write(patientDicomFileIMG.content)
        img = cv2.imread('dcmimg.png')
        res = cv2.resize(img, (480, 500))
        is_success, im_buf_arr = cv2.imencode(".png", res)
        byte_im = im_buf_arr.tobytes()
        cv2.imwrite("ERADCMIMG/" + patientNameSave + ".png", res)
        print("done with name")
        data = {'image': str(byte_im), 'Details': str(jsonDat)}
    except:
        open('ERADCM/' + str(patientNameOrID) + '.dcm', 'wb').write(patientDicomFile.content)
        filename = 'ERADCM/' + str(patientNameOrID) + '.dcm'
        dataset = pydicom.dcmread(filename)
        print("dataset: ", dataset)
        arr = np.array(dataset.pixel_array)
        jsonDat = {}
        try:
            for i in dataset:
                dat = str(i).split('     ')
                # print(dat[0],     dat[len(dat)-1])
                jData = {"'" + dat[0] + "'": dat[len(dat) - 1]}
                # load = json.load(jsonDat)
                jsonDat.update(jData)
            data = (jsonDat)
            # return Response(dat)
        except Exception as e:
            print(e)
            pass

        patientDicomFileIMG = host + '/instances/' + patientSeriesData[0] + '/preview'
        patientDicomFileIMG = requests.get(patientDicomFileIMG)
        open('dcmimg.png', 'wb').write(patientDicomFileIMG.content)
        img = cv2.imread('dcmimg.png')
        res = cv2.resize(img, (480, 500))
        is_success, im_buf_arr = cv2.imencode(".png", res)
        byte_im = im_buf_arr.tobytes()
        cv2.imwrite("ERADCMIMG/" + str(patientNameOrID) + ".png", res)
        print("done with name")
        data = {'image': str(byte_im), 'Details': str(jsonDat)}
else:
    print("wrong name/PID!")

try:
    try:
        img = cv2.imread("ERADCMIMG/" + patientNameSave + ".png")
    except:
        img = cv2.imread("ERADCMIMG/" + str(patientNameOrID) + ".png")
    cv2.imshow("Dicom Image",img)
    cv2.waitKey(0)
except:
    pass


