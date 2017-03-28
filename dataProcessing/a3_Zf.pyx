import __init__
'''

'''
from _configuration import levelNames
from _configuration import zone_dpath, Uzk_dpath
from _configuration import Zf_dpath
from _configuration import K
from supporting_modules.file_handling_functions import load_pklFile, get_all_files, save_pklFile, check_dir_create


try:
    check_dir_create(Zf_dpath)
except OSError:
    pass


numWorker = 6

def run(processerID):
    for hour in xrange(24):
        if hour % numWorker != processerID:
            continue
        for floor in levelNames:
            zones = load_pklFile('%s/z-%s.pkl' % (zone_dpath, floor))
            for fn in get_all_files(Uzk_dpath, '*-%s-*-H%02d.pkl' % (floor, hour)):
                _, lv, D, H = fn[:-len('.pkl')].split('-')
                Uzk = load_pklFile('%s/%s' % (Uzk_dpath, fn))
                Zf_fpath = '%s/Zf-%s-%s-%s.pkl' % (Zf_dpath, lv, D, H)
                #
                Zf = []
                for z in zones.itervalues():
                    for k in xrange(K):
                        if not Uzk.has_key((z.zid, k)):
                            break
                        if not Uzk[z.zid, k]:
                            break
                    else:
                        Zf += [z.zid]
                save_pklFile(Zf_fpath, Zf)