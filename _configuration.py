import os

levelNames = ['Lv%d' % x for x in range(1, 6)]

levelNames = ['Lv1', 'Lv2', 'Lv4']
levelNames = ['Lv2', 'Lv4']
K = 4
TIME_INTERVAL = 60
TIME_UNIT = TIME_INTERVAL / float(K)

beacon_data = os.path.dirname(os.path.realpath(__file__)) + '/z_data'
zone_dpath = '%s/%s' % (beacon_data, 'zone')
landmark_dpath = '%s/%s' % (beacon_data, 'landmark')
lmz_dpath = '%s/%s' % (beacon_data, 'lmz')
tra_dpath = '%s/%s' % (beacon_data, 'tra')
Uzk_dpath = '%s/%s' % (beacon_data, 'Uzk')
Zf_dpath = '%s/%s' % (beacon_data, 'Zf')

