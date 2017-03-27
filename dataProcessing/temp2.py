from _configuration import tra_dpath
from _configuration import levelNames
from _configuration import beacon_data
from supporting_modules.file_handling_functions import check_file_exist, check_dir_create

import csv, gzip
import time

candi_levels = ['0%d0' % int(ln[len('Lv'):]) for ln in levelNames]

check_dir_create(tra_dpath)

with gzip.open('%s/%s.csv.gz' % (beacon_data, 'location_archival_2017_3_1'), 'rt') as r_csvfile:
    reader = csv.reader(r_csvfile)
    headers = reader.next()
    hid = {h: i for i, h in enumerate(headers)}
    for row in reader:
        landmarkID = row[hid['location']]
        entity = landmarkID[:1]
        building = landmarkID[1:3]
        lv = landmarkID[3:6]
        lm = landmarkID[6:]
        if lv not in candi_levels:
            continue
        t = time.strptime(row[hid['time']], "%Y-%m-%d %H:%M:%S")
        lv = 'Lv%s' % lv[1:-1]
        fpath = '%s/tra-%s-%d%02d%02d-H%02d.csv' % (tra_dpath, lv, t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour)
        if not check_file_exist(fpath):
            with open(fpath, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_headers = ['time', 'id', 'location']
                writer.writerow(new_headers)
        with open(fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['time', 'id', 'location']
            writer.writerow([row[hid['time']], row[hid['id']], row[hid['location']]])
