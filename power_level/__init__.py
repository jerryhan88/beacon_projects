import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

prob_dpath = os.getcwd() + '/problems'
default_pn = 'p1'
default_pn_fpath = '%s/%s' % (prob_dpath, '%s.pkl' % default_pn)