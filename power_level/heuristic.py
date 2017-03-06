import __init__
'''
'''
#
from power_level import default_pn_fpath
from _class import beacon
#
from file_handling_functions import load_pklFile
#
from heapq import heappush, heappop
import itertools


def binseq(k):
    return [map(int, x) for x in itertools.product('01', repeat=k)]

def run(beacons, zones):
    #
    # Calculate the minimum power level
    #    Consider Manhattan distances as the power level
    #
    feasibleZones = set()
    for (i, j), z in zones.iteritems():
        if z.isFeasible:
            feasibleZones.add(z)
        z.beaconMinBL = []
    m_bz = {}
    for z in feasibleZones:
        for (bi, bj), b in beacons.iteritems():
            distManhatan = abs(z.i - bi) + abs(z.j - bj)
            if distManhatan > beacon.MAX_PL:
                continue
            z.beaconMinBL += [(distManhatan, b)]
            m_bz[b, z] = distManhatan * 1
    #
    # Calculate weights and insert them in a priority queue
    #
    Q = []
    for _i, z in enumerate(feasibleZones):
        combinations = binseq(len(z.beaconMinBL))
        for binVS in combinations:
            mC = [z.beaconMinBL[i] for i, binV in enumerate(binVS) if binV == 1]
            if not mC:
                continue
            f1 = len(mC) / float(len(beacons))
            f2 = min([b.remaingBP - ml for ml, b in mC]) / float(min([b.remaingBP for b in beacons.itervalues()]))
            w = f1 * f2
            heappush(Q, (-w, z, mC))
    print len(Q), sorted(Q)
    #
    # Initialize beacons' power level
    #
    for b in beacons.itervalues():
        b.p = 1e400
    #
    # Set battery power
    #
    while sum([b.p for b in beacons.itervalues()]) >= 1e400:
        _, z, mC = heappop(Q)
        if min([b.p for _, b in mC]) >= 1e400:
            for _, b in mC:
                b.p = m_bz[b, z]
                b.zC = (z, mC)
        else:
            continue
    print 'sol'
    for b in beacons.itervalues():
        print b, b.p, b.zC


if __name__ == '__main__':
    from _class import zone
    zones = load_pklFile(default_pn_fpath)
    run(zones)
