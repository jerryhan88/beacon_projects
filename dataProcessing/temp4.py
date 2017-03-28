from supporting_modules.file_handling_functions import load_pklFile

from _configuration import zone_dpath, landmark_dpath

landmarks = load_pklFile('%s/%s' % (landmark_dpath, 'l-Lv2.pkl'))

print landmarks['1010200120']