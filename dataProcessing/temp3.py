from supporting_modules.file_handling_functions import load_pklFile
from _configuration import Uzk_dpath, Zf_dpath

print load_pklFile('%s/%s' % (Uzk_dpath, 'Uzk-Lv2-20170201-H07.pkl'))
print load_pklFile('%s/%s' % (Zf_dpath, 'Zf-Lv2-20170214-H06.pkl'))
print load_pklFile('%s/%s' % (Zf_dpath, 'Zf-Lv2-20170214-H15.pkl'))
print load_pklFile('%s/%s' % (Zf_dpath, 'Zf-Lv2-20170214-H17.pkl'))
print load_pklFile('%s/%s' % (Zf_dpath, 'Zf-Lv2-20170214-H23.pkl'))