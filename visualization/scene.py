import __init__
'''

'''
#
from supporting_modules.file_handling_functions import load_pklFile
from _configuration import zone_dpath, landmark_dpath, beacon_dpath
from _configuration import Uzk_dpath, Zf_dpath
from decisionMaking.heuristic import heuristicRun
from chart import series
#
import wx
from xlrd import open_workbook
from bisect import bisect


xPos, yPos, cUnit = (34, 156, 7.75)
book = open_workbook('../z_data/Landmarks.xlsx')
sh = book.sheet_by_name('Lv1')
xPoints = [xPos + i * cUnit for i in range(sh.ncols)]
yPoints = [yPos + j * cUnit for j in range(sh.nrows)]
nRows, nCols = (sh.nrows - 1), (sh.ncols - 1)


class LayoutView(wx.Panel):
    def __init__(self, parent, floorName):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.floorName = floorName
        self.SetBackgroundColour(wx.WHITE)
        #
        self.grid = Grid(self)
        self.InitUI()

    def InitUI(self):
        self.SetDoubleBuffered(True)
        (self.fixed_x, self.fixed_y), self.isLeftDown = (0, 0), False
        self.translate_x, self.translate_y = 0, 0
        self.scale = 1
        self.isLeftDown = False
        # event binding
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        # prepare stock objects.
        self.default_pen = self.create_pen(wx.BLACK, 1)
        self.default_font = self.create_font(8, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        # initialize a background
        bmp = wx.BitmapFromImage(wx.Image('../z_figs/%s.png' % (self.floorName)).AdjustChannels(1.0, 1.0, 1.0, 1.0))
        w, h = bmp.GetWidth() * self.scale, bmp.GetHeight() * self.scale
        self.bg_bmp = (bmp, w, h)

    def update_date(self, cur_datetime):
        self.grid.update_Zf(cur_datetime)
        self.Refresh()
        self.Update()

    def create_pen(self, color, width):
        return wx.Pen(color, width)

    def create_font(self, size, family, style, weight):
        return wx.Font(size, family, style, weight)

    def OnPaint(self, _):
        # prepare.
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen(self.default_pen)
        gc.SetFont(self.default_font, wx.BLACK)
        # draw on logical space.
        oldTransform = gc.GetTransform()
        gc.Translate(self.translate_x, self.translate_y)
        gc.Scale(self.scale, self.scale)
        self.OnDraw(gc)
        gc.SetTransform(oldTransform)

    def OnDraw(self, gc):
        # draw background image
        bmp, w, h = self.bg_bmp
        gc.DrawBitmap(bmp, 0, 0, w, h)
        self.grid.draw(gc)
        # gc.DrawBitmap(base_bmp, 0, 0, w, h)
        # if checkBoxValues['Grid']:
        #     self.grid.draw(gc)
        # for cb_name in checkBoxNames:
        #     if cb_name == 'Grid' or cb_name == 'Landmark2':
        #         continue
        #     if checkBoxValues[cb_name]:
        #         bmp, w, h = self.bg_bmps[cb_name]
        #         gc.DrawBitmap(bmp, 0, 0, w, h)


    def OnLeftDown(self, e):
        self.grid.pick_beacon(e.GetX(), e.GetY())
        self.isLeftDown = True
        self.SetFocus()
        self.CaptureMouse()

    def OnMotion(self, e):
        if self.isLeftDown:
            cur_x, cur_y = e.GetX(), e.GetY()
            self.grid.update_pickedBeaconPos(e.GetX(), e.GetY())
            self.Refresh()
            self.Update()

    def OnLeftUp(self, e):
        if self.isLeftDown:
            self.isLeftDown = False
            self.grid.drop_beacon(e.GetX(), e.GetY())
            self.ReleaseMouse()
            self.Refresh()
            self.Update()


class Grid(object):
    def __init__(self, viewer):
        self.floorName = viewer.floorName
        book = open_workbook('../z_data/Landmarks.xlsx')
        sh = book.sheet_by_name('%s' % (self.floorName))
        self.zones = load_pklFile('%s/z-%s.pkl' % (zone_dpath, self.floorName))
        self.landmarks = load_pklFile('%s/l-%s.pkl' % (landmark_dpath, self.floorName))
        self.beacons = load_pklFile('%s/b-%s.pkl' % (beacon_dpath, self.floorName))
        for i in xrange(sh.nrows):
            for j in xrange(sh.ncols):
                if i < 1 or j < 1:
                    continue
                coords = j - 1, i - 1
                zid = 'z(%d, %d)' % tuple(coords)
                z = self.zones[zid]
                z.init4viz(xPos, yPos, cUnit, wx.Brush(wx.Colour(115, 28, 96)))  # Purple

        blue = wx.Colour(0, 0, 255)  # BLUE
        tr_pen = wx.Pen(blue, 1)
        tr_brush = wx.Brush(blue, wx.TRANSPARENT)
        for b in self.beacons.itervalues():
            z = self.zones[b.l.z.zid]
            z.add_beacon(b)
            b.init4viz(z.centerCoords, cUnit / float(4), cUnit,
                       wx.Brush(wx.Colour(228, 108, 10)), tr_pen, tr_brush)  # ORANGE



        self.picked_beacon = None

    def draw(self, gc):
        #
        # Draw grid   # gc.DrawRectangle(xPos, yPos, nCols * cUnit, nRows * cUnit)
        #
        gc.SetPen(wx.Pen(wx.Colour(100, 100, 100), 0.9))
        for i in xrange(nRows + 1):
            gc.DrawLines([(xPos, yPos + i * cUnit),
                          (xPos + nCols * cUnit, yPos + i * cUnit)])

        for j in xrange(nCols + 1):
            gc.DrawLines([(xPos + j * cUnit, yPos),
                          (xPos + j * cUnit, yPos + nRows * cUnit)])

        for z in self.zones.itervalues():
            z.draw(gc)

        for b in self.beacons.itervalues():
            b.draw(gc)

        #
        # if checkBoxValues['Landmark2']:
        #     for l in self.landmarks.itervalues():
        #         l.draw(gc, SMALL_FONT, RADIUS)

    def update_Zf(self, cur_datetime):
        H = 'H%02d' % cur_datetime.hour
        D = '%d%02d%02d' % (cur_datetime.year, cur_datetime.month, cur_datetime.day)
        Zf = load_pklFile('%s/Zf-%s-%s-%s.pkl' % (Zf_dpath, self.floorName, D, H))
        for z in self.zones.itervalues():
            z.feasible = True if z.zid in Zf else False

    def write_log(self, s):
        self.logger.write(s)

    def pick_beacon(self, x, y):
        if x < xPoints[0] or x > xPoints[-1]:
            print 'outside of grid\n'
            return None
        if y < yPoints[0] or y > yPoints[-1]:
            print 'outside of grid\n'
            return None
        #
        i, j = bisect(xPoints, x) - 1, bisect(yPoints, y) - 1
        zid = 'z(%d, %d)' % (i, j)
        z = self.zones[zid]
        if z.bs:
            self.picked_beacon = z.remove_beacon()
            print 'picked beacon %s\n' % self.picked_beacon
        else:
            print 'no beacon in the zone\n'

    def update_pickedBeaconPos(self, x, y):
        if not self.picked_beacon:
            print 'there is no picked beacon\n'
            return None
        self.picked_beacon.pos = (x, y)

    def drop_beacon(self, x, y):
        if not self.picked_beacon:
            # self.write_log('there is no picked beacon\n')
            return None
        if x < xPoints[0] or x > xPoints[-1]:
            print 'outside of grid\n'
            self.return_original_location()
            return None
        if y < yPoints[0] or y > yPoints[-1]:
            print 'outside of grid\n'
            self.return_original_location()
            return None
        i, j = bisect(xPoints, x) - 1, bisect(yPoints, y) - 1
        zid = 'z(%d, %d)' % (i, j)
        z = self.zones[zid]
        if len(z.bs) != 0:
            print 'another beacon exists\n'
            self.return_original_location()
            return None
        #
        print 'relocate the beacon to zone %s\n' % z
        self.picked_beacon.coords = z.coords
        self.picked_beacon.pos = z.centerCoords
        z.add_beacon(self.picked_beacon)
        self.picked_beacon = None

    def return_original_location(self):
        self.write_log('return beacon to the original location\n')
        ori_z = self.zones[self.picked_beacon.coords]
        self.picked_beacon.pos = ori_z.centerCoords
        ori_z.set_beacon(self.picked_beacon)
        self.picked_beacon = None

    def initProblem(self, INIT_BATTERY_CAPA, alpha, beta, P, MIN_POWER_LEVEL):
        self.Z, self.B = self.zones, self.beacons

        print '%s, # of beacons is %d' % (self.floorName, len(self.B))

        self.P = P
        self.alpha = alpha
        for b in self.B.itervalues():
            b.init4heuristic(INIT_BATTERY_CAPA, alpha, beta)
        #
        self.fixed10_bz = {}
        self.fixed20_bz = {}
        self.fixed30_bz = {}
        #
        for z in self.Z.itervalues():
            for b in self.B.itervalues():
                bi, bj = b.l.z.i, b.l.z.j
                distManhatan = abs(z.i - bi) + abs(z.j - bj)
                #
                self.fixed10_bz[b.bid, z.zid] = True if distManhatan <= 10 else False
                self.fixed20_bz[b.bid, z.zid] = True if distManhatan <= 20 else False
                self.fixed30_bz[b.bid, z.zid] = True if distManhatan <= 30 else False
                #
                if distManhatan > P * beta:
                    b.pbz[z.zid] = 1e400
                else:
                    if distManhatan == 0:
                        b.pbz[z.zid] = MIN_POWER_LEVEL
                    else:
                        b.pbz[z.zid] = distManhatan * beta
        self.numIter = 0
        self.measures_APL = {}
        for mn in ['minBattery', 'numZone', 'popularity', 'numUniUser']:
            self.measures_APL[mn] = series()
        #
        #
        self.br_F10, self.br_F20, self.br_F30 = {}, {}, {}
        for b in self.B.itervalues():
            self.br_F10[b.bid] = INIT_BATTERY_CAPA
            self.br_F20[b.bid] = INIT_BATTERY_CAPA
            self.br_F30[b.bid] = INIT_BATTERY_CAPA
        self.measures_F10, self.measures_F20, self.measures_F30 = {}, {}, {}
        for mn in ['minBattery', 'numZone', 'popularity', 'numUniUser']:
            self.measures_F10[mn] = series()
        for mn in ['minBattery', 'numZone', 'popularity', 'numUniUser']:
            self.measures_F20[mn] = series()
        for mn in ['minBattery', 'numZone', 'popularity', 'numUniUser']:
            self.measures_F30[mn] = series()

    def iterativeSolving(self, cur_datetime):
        self.numIter += 1
        H = 'H%02d' % cur_datetime.hour
        D = '%d%02d%02d' % (cur_datetime.year, cur_datetime.month, cur_datetime.day)
        Zf = load_pklFile('%s/Zf-%s-%s-%s.pkl' % (Zf_dpath, self.floorName, D, H))
        Uzk = load_pklFile('%s/Uzk-%s-%s-%s.pkl' % (Uzk_dpath, self.floorName, D, H))
        Uz = {}
        for (zid, _), usersSet in Uzk.iteritems():
            if not Uz.has_key(zid):
                Uz[zid] = set()
            Uz[zid] = Uz[zid].union(usersSet)
        S, Xcovered_beacons = heuristicRun(Uz, Zf, self.B)
        if S == 'End':
            print 'No iteration (End)'
            return
        if S == 'infeasible':
            print 'infeasible (Stop)'
            print cur_datetime, self.floorName
            assert False
        pb = {}
        for b in self.B.itervalues():
            minPowerLevel = 1e400
            for zid in S:
                if b.pbz[zid] < minPowerLevel:
                    minPowerLevel = b.pbz[zid]
            pb[b] = minPowerLevel
        # print S, Xcovered_beacons
        self.measures_APL['minBattery'].record(self.numIter, min(int(b.rb - pb[b] * self.alpha) for b in self.B.itervalues()))
        self.measures_APL['numZone'].record(self.numIter, len(S))
        self.measures_APL['popularity'].record(self.numIter, sum(len(Uz[zid]) for zid in S))
        UU = set()
        for zid in S:
            UU = UU.union(Uz[zid])
        self.measures_APL['numUniUser'].record(self.numIter, len(UU))
        #
        # Set power levels
        #
        for b in self.B.itervalues():
            b.curPowerLevel = pb[b]
            b.rb = b.rb - b.curPowerLevel * self.alpha
            b.calc_transmitRange()
        #
        #
        #
        coveredBeacons_F10 = {b.bid: False for b in self.B.itervalues()}
        coveringZones_F10 = set()
        coveredBeacons_F20 = {b.bid: False for b in self.B.itervalues()}
        coveringZones_F20 = set()
        coveredBeacons_F30 = {b.bid: False for b in self.B.itervalues()}
        coveringZones_F30 = set()
        for b in self.B.itervalues():
            canCoverd10 = False
            canCoverd20 = False
            canCoverd30 = False
            for zid in Zf:
                if self.fixed10_bz[b.bid, zid]:
                    canCoverd10 = True
                    #
                    if zid not in coveringZones_F10 and not coveredBeacons_F10[b.bid]:
                        coveredBeacons_F10[b.bid] = True
                        coveringZones_F10.add(zid)
                        for b1 in self.B.itervalues():
                            if b == b1:
                                continue
                            if coveredBeacons_F10[b1.bid]:
                                continue
                            if self.fixed10_bz[b1.bid, zid]:
                                coveredBeacons_F10[b1.bid] = True
                if self.fixed20_bz[b.bid, zid]:
                    canCoverd20 = True
                    #
                    if zid not in coveringZones_F20 and not coveredBeacons_F20[b.bid]:
                        coveredBeacons_F20[b.bid] = True
                        coveringZones_F20.add(zid)
                        for b1 in self.B.itervalues():
                            if b == b1:
                                continue
                            if coveredBeacons_F20[b1.bid]:
                                continue
                            if self.fixed20_bz[b1.bid, zid]:
                                coveredBeacons_F20[b1.bid] = True
                if self.fixed30_bz[b.bid, zid]:
                    canCoverd30 = True
                    #
                    if zid not in coveringZones_F30 and not coveredBeacons_F30[b.bid]:
                        coveredBeacons_F30[b.bid] = True
                        coveringZones_F30.add(zid)
                        for b1 in self.B.itervalues():
                            if b == b1:
                                continue
                            if coveredBeacons_F30[b1.bid]:
                                continue
                            if self.fixed30_bz[b1.bid, zid]:
                                coveredBeacons_F30[b1.bid] = True


            if canCoverd10:
                self.br_F10[b.bid] -= 10
            else:
                self.br_F10[b.bid] -= self.P
            if canCoverd20:
                self.br_F20[b.bid] -= 20
            else:
                self.br_F20[b.bid] -= self.P
            if canCoverd30:
                self.br_F30[b.bid] -= 30
            else:
                self.br_F30[b.bid] -= self.P


        self.measures_F10['minBattery'].record(self.numIter, min(self.br_F10[b.bid] for b in self.B.itervalues()))
        self.measures_F20['minBattery'].record(self.numIter, min(self.br_F20[b.bid] for b in self.B.itervalues()))
        self.measures_F30['minBattery'].record(self.numIter, min(self.br_F30[b.bid] for b in self.B.itervalues()))
        #
        self.measures_F10['numZone'].record(self.numIter, len(coveringZones_F10))
        self.measures_F20['numZone'].record(self.numIter, len(coveringZones_F20))
        self.measures_F30['numZone'].record(self.numIter, len(coveringZones_F30))
        #
        self.measures_F10['popularity'].record(self.numIter, sum(len(Uz[zid]) for zid in coveringZones_F10))
        self.measures_F20['popularity'].record(self.numIter, sum(len(Uz[zid]) for zid in coveringZones_F20))
        self.measures_F30['popularity'].record(self.numIter, sum(len(Uz[zid]) for zid in coveringZones_F30))
        #
        UU = set()
        for zid in coveringZones_F10:
            UU = UU.union(Uz[zid])
        self.measures_F10['numUniUser'].record(self.numIter, len(UU))
        UU = set()
        for zid in coveringZones_F20:
            UU = UU.union(Uz[zid])
        self.measures_F20['numUniUser'].record(self.numIter, len(UU))
        UU = set()
        for zid in coveringZones_F30:
            UU = UU.union(Uz[zid])
        self.measures_F30['numUniUser'].record(self.numIter, len(UU))


class tempFrame(wx.Frame):
    def __init__(self, title="AdaptivePowerLevel", pos=(30, 30), size=(1500, 900)):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        #
        self.InitUI()
        self.Centre()
        self.Show(True)

    def InitUI(self):
        basePanel = wx.Panel(self)
        basePanel.logger = None
        basePanel.SetBackgroundColour('#4f5049')
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(LayoutView(basePanel, 'Lv4'), 1, wx.EXPAND | wx.ALL, 5)
        basePanel.SetSizer(vbox)


if __name__ == '__main__':
    from visualization import app
    tempFrame()
    app.MainLoop()
