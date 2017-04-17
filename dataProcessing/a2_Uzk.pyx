import __init__
'''

'''
from _configuration import landmark_dpath
from _configuration import tra_dpath
from _configuration import Uzk_dpath
from _configuration import TIME_UNIT
#
from supporting_modules.file_handling_functions import get_all_files, check_dir_create, check_file_exist, load_pklFile, save_pklFile
#
import time
import csv

try:
    check_dir_create(Uzk_dpath)
except OSError:
    pass


numWorker = 5


def run(processerID):
    for i, fn in enumerate(get_all_files(tra_dpath, '*-H*.csv')):
        if i % numWorker != processerID:
            continue
        _, lv, D, H = fn[:-len('.csv')].split('-')
        hour = int(H[len('H'):])
        Uzk_fpath = '%s/Uzk-%s-%s-%s.pkl' % (Uzk_dpath, lv, D, H)
        if check_file_exist(Uzk_fpath):
            continue
        Uzk = {}
        landmarks = load_pklFile('%s/l-%s.pkl' % (landmark_dpath, lv))
        with open('%s/%s' % (tra_dpath, fn), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            header = reader.next()
            hid = {h: i for i, h in enumerate(header)}
            for row in reader:
                landmarkID = row[hid['location']]
                t = time.strptime(row[hid['time']], "%Y-%m-%d %H:%M:%S")
                try:
                    l = landmarks[landmarkID]
                    k = int(t.tm_min / TIME_UNIT)
                    if not Uzk.has_key((l.z.zid, k)):
                        Uzk[l.z.zid, k] = set()
                    Uzk[l.z.zid, k].add(row[hid['id']])
                except KeyError:
                    with open('missing_location.st_cur_datetime', 'a') as f:
                        f.write('%s\n' % landmarkID)
        save_pklFile(Uzk_fpath, Uzk)


if __name__ == '__main__':
    run(2)