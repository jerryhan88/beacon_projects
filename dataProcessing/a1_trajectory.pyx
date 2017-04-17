import __init__
'''

'''

from _configuration import tra_dpath
from _configuration import floorNames
from _configuration import beacon_data
from supporting_modules.file_handling_functions import check_file_exist, check_dir_create

import csv, gzip
import time

candi_levels = ['0%d0' % int(ln[len('Lv'):]) for ln in floorNames]
HOUR_9AM_6PM = [h for h in range(9, 18)]
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)

try:
    check_dir_create(tra_dpath)
except OSError:
    pass

def run(month):
    with gzip.open('%s/%s.csv.gz' % (beacon_data, 'location_archival_2017_%d_1' % month), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            t = time.strptime(row[hid['time']], "%Y-%m-%d %H:%M:%S")
            if t.tm_wday in [SAT, SUN]:
                continue
            if not t.tm_hour in HOUR_9AM_6PM:
                continue
            landmarkID = row[hid['location']]
            entity = landmarkID[:1]
            building = landmarkID[1:3]
            lv = landmarkID[3:6]
            lm = landmarkID[6:]
            if lv not in candi_levels:
                continue
            lv = 'Lv%s' % lv[1:-1]
            fpath = '%s/tra-%s-%d%02d%02d-H%02d.csv' % (tra_dpath, lv, t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour)
            if not check_file_exist(fpath):
                with open(fpath, 'wb') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_headers = ['time', 'id', 'location']
                    writer.writerow(new_headers)
            with open(fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([row[hid['time']], row[hid['id']], row[hid['location']]])

if __name__ == '__main__':
    run()