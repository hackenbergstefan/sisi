#/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import numpy as np
from configparser import ConfigParser


class CWTraceFile(object):

    def __init__(self, fileprefix, textin, textout, knownkey, keylist, traces):
        self.fileprefix = fileprefix
        self.textin = textin
        self.textout = textout
        self.knownkey = knownkey
        self.keylist = keylist
        self.traces = traces

    def save(self):
        np.save('%s_textin.npy' % self.fileprefix, self.textin)
        np.save('%s_traces.npy' % self.fileprefix, self.traces)
        np.save('%s_textout.npy' % self.fileprefix, self.textout)
        np.save('%s_knownkey.npy' % self.fileprefix, self.knownkey)
        np.save('%s_keylist.npy' % self.fileprefix, self.keylist)

        config = ConfigParser()
        config.optionxform = str
        config.read_dict({
            'Trace Config': {
                'numTraces': self.traces.shape[0],
                'numPoints': self.traces.shape[1],
                'format': 'native',
                'prefix': '%s_' % os.path.basename(self.fileprefix),
                'scopeName': 'Sisi'
            }
        })
        with open('%s.cfg' % self.fileprefix, 'w') as fout:
            config.write(fout)
