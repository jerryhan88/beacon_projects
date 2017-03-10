import __init__
'''
'''
#
from bisect import bisect

TIME_INTERVAL = 60
N = 10
#
K, alpha, beta, P = None, None, None, None


def run():
    from problem import problem1, problem2
    curProblem = problem1
    Z, B, U, _K, _alpha, _beta, _P = curProblem()
    global K, alpha, beta, P
    K, alpha, beta, P = _K, _alpha, _beta, _P
    iterCount = 0
    while True:
        print 'Iteration %d' % iterCount
        if curProblem == problem1:
            curProblem = problem2
        else:
            curProblem = problem1
        _, _, U, _, _, _, _ = curProblem()
        S = heuristicRun(Z, B, U)
        if S == 'End':
            print 'No iteration (End)'
            return
        resultDisplay(S, Z, B, U)
        setPowerLevel(S, B)
        iterCount += 1
        print ''


def setPowerLevel(S, B):
    for b in B.itervalues():
        minDist = 1e400
        for z in S:
            bi, bj = b.locatedZone.i, b.locatedZone.j
            distManhatan = abs(z.i - bi) + abs(z.j - bj)
            if distManhatan < minDist:
                minDist = distManhatan
        if minDist == 0:
            minDist = 1
        b.remainingBC -= minDist * alpha

def resultDisplay(S, Z, B, U):
    pb = {}
    for b in B.itervalues():
        minDist = 1e400
        for z in S:
            bi, bj = b.locatedZone.i, b.locatedZone.j
            distManhatan = abs(z.i - bi) + abs(z.j - bj)
            if distManhatan < minDist:
                minDist = distManhatan
        if minDist == 0:
            minDist = 1
        pb[b] = minDist
    print '\t O1. EMR %d;' % min(b.remainingBC - pb[b] * alpha for b in B.itervalues())
    for b in B.itervalues():
        print "\t\t\t %s: PL %d, BC %d" % (b, pb[b], b.remainingBC - pb[b] * alpha)
    #
    #
    #
    print '\t O2. numZones %d; %s' % (len(S), str(list(S)))
    time_unit = TIME_INTERVAL / float(K)
    Uzk = {}
    xPoints, yPoints = set(), set()
    for z in Z.itervalues():
        for k in xrange(K):
            Uzk[z, k] = set()
        for x, y in [z.leftUpperCoords, z.leftLowerCoords, z.rightLowerCoords, z.rightUpperCoords]:
            xPoints.add(x)
            yPoints.add(y)
    xPoints, yPoints = sorted(list(xPoints)), sorted(list(yPoints))
    for u in U.itervalues():
        for l in u.trajectory:
            t, x, y = l
            k = int(t / time_unit)
            i, j = bisect(xPoints, x) - 1, bisect(yPoints, y) - 1
            Uzk[Z[i, j], k].add(u)
    Uz = {}
    for (z, _), usersSet in Uzk.iteritems():
        if not Uz.has_key(z):
            Uz[z] = set()
        Uz[z] = Uz[z].union(usersSet)
    print '\t O3. Popularity %d' % (sum(len(Uz[z]) for z in S))
    #
    #
    #
    UU = set()
    for z in S:
        UU = UU.union(Uz[z])
    print '\t O4. NUU %d' % (len(UU))









def heuristicRun(Z, B, U):
    time_unit = TIME_INTERVAL / float(K)
    #
    Uzk = {}
    xPoints, yPoints = set(), set()
    for z in Z.itervalues():
        for k in xrange(K):
            Uzk[z, k] = set()
        for x, y in [z.leftUpperCoords, z.leftLowerCoords, z.rightLowerCoords, z.rightUpperCoords]:
            xPoints.add(x)
            yPoints.add(y)
    xPoints, yPoints = sorted(list(xPoints)), sorted(list(yPoints))
    #
    pbz = {}
    for z in Z.itervalues():
        for b in B.itervalues():
            bi, bj = b.locatedZone.i, b.locatedZone.j
            distManhatan = abs(z.i - bi) + abs(z.j - bj)
            if distManhatan > P * beta:
                pbz[b, z] = 1e400
            else:
                pbz[b, z] = distManhatan * beta
    #
    # S1. Define Uzk
    #
    for u in U.itervalues():
        for l in u.trajectory:
            t, x, y = l
            k = int(t / time_unit)
            i, j = bisect(xPoints, x) - 1, bisect(yPoints, y) - 1
            Uzk[Z[i, j], k].add(u)
    #
    # S2. Define Zf
    #
    Zf = []
    for z in Z.itervalues():
        for k in xrange(K):
            if not Uzk[z, k]:
                break
        else:
            Zf += [z]
    #
    # S3. Set EMR0
    #
    EMR0 = 1e400
    for b in B.itervalues():
        if EMR0 > b.remainingBC - alpha:
            EMR0 = b.remainingBC - alpha
    NUU0, S0 = findGreedySolution(Zf, B, EMR0, Uzk, pbz)
    while NUU0 == None:
        EMR0 -= alpha
        NUU0, S0 = findGreedySolution(Zf, B, EMR0, Uzk, pbz)
        if EMR0 < 0:
            return 'infeasible'
    if EMR0 == 0:
        return 'End'
    #
    # S4. Set EMR1
    #
    EMR1 = EMR0 - alpha
    #
    # S5 and S6
    #
    NUU1, S1 = findGreedySolution(Zf, B, EMR1, Uzk, pbz)
    #
    #
    #
    deltaEMR = (EMR0 - EMR1) / float(EMR0)
    deltaNUU = (NUU0 - NUU1) / float(NUU0)
    while abs(deltaEMR) < abs(deltaNUU):
        EMR0, NUU0, S0 = EMR1, NUU1, S1
        EMR1 = EMR0 - alpha
        NUU1, S1 = findGreedySolution(Zf, B, EMR1, Uzk, pbz)
        deltaEMR = (EMR0 - EMR1) / float(EMR0)
        deltaNUU = (NUU0 - NUU1) / float(NUU0)
    return S0
        
    
def findGreedySolution(Zf, B, EMR, Uzk, pbz):
    Uz = {}
    for (z, _), usersSet in Uzk.iteritems():
        if not Uz.has_key(z):
            Uz[z] = set()
        Uz[z] = Uz[z].union(usersSet)
    #
    # S1. Set nSolutions
    #
    nSolutions = findNBestSolutions(Zf, B, EMR, Uz, Uzk, pbz)
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
    

def findNBestSolutions(Zf, B, EMR, Uz, Uzk, pbz):
    #
    # S1. Define Bz and adj
    #
    Bz, adj = {}, {}
    xVulnerableBeacons = set()
    for z in Zf:
        bz = set()
        for b in B.itervalues():
            if b.remainingBC - alpha * pbz[b, z] >= EMR:
                bz.add(b)
                xVulnerableBeacons.add(b)
        Bz[z] = bz
        adj[z] = []
    if len(xVulnerableBeacons) != len(B):
        return None, None
    #
    # S2. Graph construction
    #
    for z0 in Zf:
        for z1 in Zf:
            if z0 == z1:
                continue
            if len(Bz[z0].difference(Bz[z1])) != 0:
                adj[z0] += [z1]
    #
    # S3. Set nSolutions
    #
    nSolutions = []  
    #
    # S4. Sort Zf
    #
    L = sorted(Zf, key=lambda z: len(Uz[z]), reverse=True)
    #
    # S5
    #
    while L:
        coveredBeacons = {}
        parent = {}
        for z in Zf:
            coveredBeacons[z] = set()
            parent[z] = None
        z0 = L.pop(0)
        coveredBeacons[z0] = coveredBeacons[z0].union(Bz[z0])
        nSolutions = greedyDFS(z0, Bz, adj, B, Uz, coveredBeacons, parent, nSolutions)
        if len(nSolutions) == N:
            break
    return nSolutions

        
def greedyDFS(z0, Bz, adj, B, Uz, coveredBeacons, parent, solutions):
    if len(coveredBeacons[z0]) == len(B):
        solution = set()
        solution.add(z0)
        z = parent[z0]
        while parent[z] != None:
            solution.add(z)
            z = parent[z]
        solutions += [solution]
        if len(solutions) == N:
            return solutions
    Q = []
    for z1 in adj[z0]:
        estimatedNumCoveredBeacons = len(coveredBeacons[z0].union(Bz[z1]))
        Q += [(len(B) - estimatedNumCoveredBeacons, len(Uz[z1]), z1)]
    Q.sort(key=lambda ele: (ele[0], -ele[1]))
    for _, _, z1 in Q:
        if not coveredBeacons[z1]:
            parent[z1] = z0
            coveredBeacons[z1] = coveredBeacons[z0].union(Bz[z1])
            solutions = greedyDFS(z1, Bz, adj, B, Uz, coveredBeacons, parent, solutions)
            if len(solutions) == N:
                return solutions
    return solutions
    
    
if __name__ == '__main__':
    run()
