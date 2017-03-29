import __init__
'''

'''
from _configuration import levelNames
from _configuration import landmark_dpath, beacon_dpath
from _class import Beacon
from supporting_modules.file_handling_functions import save_pklFile, load_pklFile, check_dir_create
#
from xlrd import open_workbook
#
check_dir_create(beacon_dpath)


book = open_workbook('../z_data/BeaconLocation.xlsx')
for floor in levelNames:
    landmarks = load_pklFile('%s/l-%s.pkl' % (landmark_dpath, floor))
    floor_format = '0' + floor[len('Lv'):] + '0'
    sh = book.sheet_by_name('BriefRepresentation')
    beacons = {}
    for i in range(1, sh.nrows):
        locationID, landmarkID = map(str, map(int, [sh.cell(i, 0).value, sh.cell(i, 1).value]))
        entity = landmarkID[:1]
        building = landmarkID[1:3]
        lv = landmarkID[3:6]
        lm = landmarkID[6:]
        if floor_format == lv:
            b = Beacon(locationID, landmarks[landmarkID])
            beacons[locationID] = b
    save_pklFile('%s/b-%s.pkl' % (beacon_dpath, floor), beacons)
