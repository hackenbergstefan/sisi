import os
import numpy as np
from sisi.simulator import hamming_weight


def cpa():
    path = r'C:/Users/hackenbs/chipwhisperer/projects/base-01_data/traces'
    traces = np.load(os.path.join(path, r'simple_leakage_traces.npy'))
    textin = np.load(os.path.join(path, r'simple_leakage_textin.npy'))

    numtraces = traces.shape[0]
    numpoint = traces.shape[1]

    # Mean of all points in trace
    print('traces[0] = ', traces[0])
    meant = np.mean(traces, axis=0, dtype=np.float64)
    print('meant = ', meant)

    for kguess in range(256):

        hyp = np.zeros(numtraces)
        for tnum in range(0, numtraces):
            hyp[tnum] = hamming_weight(textin[tnum, 0] ^ kguess)

        #Mean of hypothesis
        meanh = np.mean(hyp, dtype=np.float64)
        # print('hyp = ', hyp)
        print('meanh = ', meanh)

        #Initialize arrays & variables to zero
        sumnum = np.zeros(numpoint, dtype=np.float64)
        sumden1 = np.zeros(numpoint, dtype=np.float64)
        sumden2 = np.zeros(numpoint, dtype=np.float64)

        # For each trace, do the following
        for tnum in range(numtraces):
            hdiff = hyp[tnum] - meanh
            tdiff = traces[tnum, :] - meant

            sumnum = sumnum + hdiff*tdiff
            sumden1 = sumden1 + hdiff*hdiff
            sumden2 = sumden2 + tdiff*tdiff

        #print('sumnum = ', sumnum)
        #print('sumden1 = ', sumden1)
        #print('sumden2 = ', sumden2)
        print('rij = ', sumnum/np.sqrt(sumden1*sumden2))

if __name__ == '__main__':
    cpa()