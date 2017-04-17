import __init__
'''

'''
#
from _configuration import zone_dpath, beacon_dpath
from _configuration import Uzk_dpath, Zf_dpath
from _configuration import Zf_dpath
#
from supporting_modules.file_handling_functions import load_pklFile
#
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import pyplot
from pylab import legend
from matplotlib.lines import Line2D

from_date, to_date = '01/02/2017', '01/03/2017'
# floor = 'Lv4'
floor = 'Lv2'
HOUR_9AM_6PM = ['H%d' %h for h in range(9, 18)]
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
#
P = 20  # The maximum power level
K = 4  # The number of time slots
alpha, beta = 1, 1
INIT_BATTERY_CAPA = P * 9 * 20  # Maximum power level * hours in a day * days in a month (except weekends)
N = 10  # The number of candidate solutions
MIN_POWER_LEVEL = 1
#
Z = load_pklFile('%s/z-%s.pkl' % (zone_dpath, floor))
B = load_pklFile('%s/b-%s.pkl' % (beacon_dpath, floor))
for b in B.itervalues():
    b.init4heuristic(INIT_BATTERY_CAPA, alpha, beta)
for z in Z.itervalues():
    for b in B.itervalues():
        bi, bj = b.l.z.i, b.l.z.j
        distManhatan = abs(z.i - bi) + abs(z.j - bj)
        if distManhatan > P * beta:
            b.pbz[z.zid] = 1e400
        else:
            if distManhatan == 0:
                b.pbz[z.zid] = MIN_POWER_LEVEL
            else:
                b.pbz[z.zid] = distManhatan * beta

def run():
    from_dt = datetime.fromtimestamp(time.mktime(time.strptime(from_date, "%d/%m/%Y")))
    to_dt = datetime.fromtimestamp(time.mktime(time.strptime(to_date, "%d/%m/%Y")))
    cur_dt = from_dt
    numIter = 0
    beacon_remaining_power = {b.bid: [b.rb] for b in B.itervalues()}
    fixed_power_level = {'f%d' % x:[INIT_BATTERY_CAPA] for x in [3,5,10,15]}
    while cur_dt != to_dt:
        cur_dt += timedelta(hours=1)
        if cur_dt.weekday() in [SAT, SUN]:
            continue
        H = 'H%02d' % cur_dt.hour
        if H not in HOUR_9AM_6PM:
            continue
        D = '%04d%02d%02d' % (cur_dt.year, cur_dt.month, cur_dt.day)
        #
        numIter += 1
        print '#%03d %s-%s' % (numIter, D, H)
        Uzk = load_pklFile('%s/Uzk-%s-%s-%s.pkl' % (Uzk_dpath, floor, D, H))
        Uz = {}
        for (zid, _), usersSet in Uzk.iteritems():
            if not Uz.has_key(zid):
                Uz[zid] = set()
            Uz[zid] = Uz[zid].union(usersSet)
        Zf = load_pklFile('%s/Zf-%s-%s-%s.pkl' % (Zf_dpath, floor, D, H))
        S, Xcovered_beacons = heuristicRun(Uz, Zf, B)
        if S == 'End':
            print 'No iteration (End)'
            return
        #
        # Display results
        #
        pb = {}
        for b in B.itervalues():
            minPowerLevel = 1e400
            for zid in S:
                if b.pbz[zid] < minPowerLevel:
                    minPowerLevel = b.pbz[zid]
            pb[b] = minPowerLevel
        print S, Xcovered_beacons
        print '\t O1. EMR %d;' % min(int(b.rb - pb[b] * alpha) for b in B.itervalues())
        for b in B.itervalues():
            print "\t\t\t bid %s: PL %d, BC %d" % (b, pb[b], b.rb - pb[b] * alpha)
            beacon_remaining_power[b.bid] += [b.rb]
        print '\t O2. numZones %d; %s' % (len(S), str(list(S)))
        print '\t O3. Popularity %d' % (sum(len(Uz[zid]) for zid in S))
        UU = set()
        for zid in S:
            UU = UU.union(Uz[zid])
        print '\t O4. NUU %d' % (len(UU))
        #
        # Set power levels
        #
        for b in B.itervalues():
            b.rb = b.rb - pb[b] * alpha
        print ''


        for _fl in fixed_power_level.iterkeys():
            fl = int(_fl[len('f'):])
            fixed_power_level[_fl] += [INIT_BATTERY_CAPA - fl * numIter]


    fig = pyplot.figure()
    axes = plt.subplot()
    axes.set_title(floor, fontsize=11)
    markers = []
    for m in Line2D.markers:
        try:
            if len(m) == 1 and m != ' ':
                markers.append(m)
        except TypeError:
            pass
    styles = markers + [
        r'$\lambda$',
        r'$\bowtie$',
        r'$\circlearrowleft$',
        r'$\clubsuit$',
        r'$\checkmark$']
    for i, (bid, pls) in enumerate(beacon_remaining_power.iteritems()):
        plt.plot(range(len(pls)), pls, marker=styles[i % len(styles)], markersize=6, linewidth=1, label=bid)

    for fl, pls in fixed_power_level.iteritems():
        plt.plot(range(len(pls)), pls, '--', linewidth=1, label=fl)

    legend()
    plt.show()

    

def heuristicRun(Uz, Zf, B):
    Ocovered_beacons = set()
    for zid in Zf:
        for b in B.itervalues():
            if b.pbz[zid] != 1e400:
                Ocovered_beacons.add(b.bid)
    Xcovered_beacons = set([b.bid for b in B.itervalues()]).difference(Ocovered_beacons)
    modi_B = {b.bid: b for b in B.itervalues() if b.bid not in Xcovered_beacons}
    #
    EMR0 = 1e400
    for b in modi_B.itervalues():
        if EMR0 > b.rb - alpha:
            EMR0 = b.rb - alpha
    NUU0, S0 = findGreedySolution(Uz, Zf, modi_B, EMR0)
    while NUU0 == None:
        EMR0 -= alpha
        NUU0, S0 = findGreedySolution(Uz, Zf, modi_B, EMR0)
        if EMR0 < 0:
            return 'infeasible', 'infeasible'
    if EMR0 == 0:
        return 'End', 'End'
    #
    # S4. Set EMR1
    #
    EMR1 = EMR0 - alpha
    #
    # S5 and S6
    #
    NUU1, S1 = findGreedySolution(Uz, Zf, modi_B, EMR1)
    if NUU1 == None:
        return S0, Xcovered_beacons
    #
    #
    #
    deltaEMR = (EMR0 - EMR1) / float(EMR0)
    deltaNUU = (NUU1 - NUU0) / float(NUU0)
    if deltaNUU < 0:
        return S0, Xcovered_beacons
    else:
        while abs(deltaEMR) < abs(deltaNUU):
            EMR0, NUU0, S0 = EMR1, NUU1, S1
            EMR1 = EMR0 - alpha
            NUU1, S1 = findGreedySolution(Uz, Zf, modi_B, EMR1)
            if NUU1 == None:
                return S0, Xcovered_beacons
            deltaEMR = (EMR0 - EMR1) / float(EMR0)
            deltaNUU = (NUU0 - NUU1) / float(NUU0)
            if deltaNUU < 0:
                break
        return S0, Xcovered_beacons


def findGreedySolution(Uz, Zf, B, EMR):
    #
    # S1. Set nSolutions
    #
    nSolutions = findNBestSolutions(Uz, Zf, B, EMR)
    if nSolutions == None:
        return None, None
    if nSolutions[0] == None:
        return None, None
    #
    # S2.
    #
    minNUU, bestS = 1e400, None
    for S in nSolutions:
        UU = set()
        for z in S:
            UU = UU.union(Uz[z])
        NUU = len(UU)
        if NUU < minNUU:
            minNUU = NUU
            bestS = S
    return minNUU, bestS


def findNBestSolutions(Uz, Zf, B, EMR):
    #
    # S1. Define Bz and adj
    #
    Bz, adj = {}, {}
    xVulnerableBeacons = set()
    for zid in Zf:
        bz = set()
        for b in B.itervalues():
            if b.rb - alpha * b.pbz[zid] >= EMR:
                bz.add(b)
                xVulnerableBeacons.add(b)
        Bz[zid] = bz
        adj[zid] = []
    if len(xVulnerableBeacons) != len(B):
        return None, None
    #
    # S2. Graph construction
    #
    for z0id in Zf:
        for z1id in Zf:
            if z0id == z1id:
                continue
            if len(Bz[z0id].difference(Bz[z1id])) != 0:
                adj[z0id] += [z1id]
    #
    # S3. Set nSolutions
    #
    nSolutions = []  
    #
    # S4. Sort Zf
    #
    L = sorted(Zf, key=lambda zid: len(Uz[zid]), reverse=True)
    #
    # S5
    #
    while L:
        coveredBeacons = {}
        parent = {}
        for zid in Zf:
            coveredBeacons[zid] = set()
            parent[zid] = None
        z0id = L.pop(0)
        coveredBeacons[z0id] = coveredBeacons[z0id].union(Bz[z0id])
        nSolutions = greedyDFS(z0id, Bz, adj, B, Uz, coveredBeacons, parent, nSolutions)
        if nSolutions == None:
            continue
        if len(nSolutions) == N:
            break
    return nSolutions

     
def greedyDFS(z0id, Bz, adj, B, Uz, coveredBeacons, parent, solutions):
    if len(coveredBeacons[z0id]) == len(B):
        solution = set()
        solution.add(z0id)
        zid = parent[z0id]
        if zid != None:
            while parent[zid] != None:
                solution.add(zid)
                zid = parent[zid]
            solution.add(zid)
            if solutions == None:
                solutions = []
            solutions += [solution]
        # print '\t\t', solution
        # return solutions
    else:
        Q = []
        for z1id in adj[z0id]:
            estimatedNumCoveredBeacons = len(coveredBeacons[z0id].union(Bz[z1id]))
            Q += [(len(B) - estimatedNumCoveredBeacons, len(Uz[z1id]), z1id)]
        Q.sort(key=lambda ele: (ele[0], -ele[1]))
        for _, _, z1id in Q:
            if not coveredBeacons[z1id]:
                # print '\t', z0id, z1id
                parent[z1id] = z0id
                coveredBeacons[z1id] = coveredBeacons[z0id].union(Bz[z1id])
                # solutions = greedyDFS(z1id, Bz, adj, B, Uz, coveredBeacons, parent, solutions)
                greedyDFS(z1id, Bz, adj, B, Uz, coveredBeacons, parent, solutions)
                if solutions == None:
                    continue
                if len(solutions) == N:
                    break
        return solutions


if __name__ == '__main__':
    run()
