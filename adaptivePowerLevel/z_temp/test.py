import __init__
'''
'''
from xlrd import open_workbook

exFP = '../z_data/Landmark.xlsx'
book = open_workbook(exFP)
sh = book.sheet_by_name('Lv1')

for i in xrange(sh.nrows):
    for j in xrange(sh.ncols):
        print (i, j), sh.cell(i, j).value

