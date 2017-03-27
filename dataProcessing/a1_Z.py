import __init__
'''

'''
from _configuration import levelNames
from _configuration import zone_dpath, landmark_dpath
from _class import Zone, Landmark
from supporting_modules.file_handling_functions import save_pklFile, check_dir_create
#
from xlrd import open_workbook


for dpath in [zone_dpath, landmark_dpath]:
    check_dir_create(dpath)

book = open_workbook('../z_data/Landmark.xlsx')
for floor in levelNames:
    sh = book.sheet_by_name('%s' % (floor))
    nRows, nCols = (sh.nrows - 1), (sh.ncols - 1)
    # About zones and landmarks
    zones, landmarks = {}, {}
    lmz = {}
    for i in xrange(sh.nrows):
        for j in xrange(sh.ncols):
            if i < 1 or j < 1:
                continue
            coords = j - 1, i - 1
            z = Zone(coords)
            zones[z.zid] = z
            if sh.cell(i, j).value:
                l_num = int(sh.cell(i, j).value)
                lid = '1010%s0%04d' % (floor[len('Lv'):], l_num)
                l = Landmark(lid, z)
                landmarks[lid] = l
                z.set_landmark(l)
    save_pklFile('%s/z-%s.pkl' % (zone_dpath, floor), zones)
    save_pklFile('%s/l-%s.pkl' % (landmark_dpath, floor), landmarks)