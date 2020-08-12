#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 08:51:39 2020

@author: nuralakchurin
"""

from LC3377 import *
from UtilityModules import DummyModule

class TDCUnpacker(DummyModule):
    # In the constructor, provide whatever arguments
    # you intend to play with
    def __init__(self, name):
        DummyModule.__init__(self, name)

    def beginRun(self, runNumber, runRecord):
        runConfiguration = runRecord[(runNumber, "runConfiguration")]
        self.tdc_slots=runConfiguration["tdc_slots_3377"]
        
    def processEvent(self, runNumber, eventNumber, eventRecord):
        
        tdcData = dict()
        
        
        for slot in self.tdc_slots:
            fifoData = eventRecord[(slot,"LeCroy3377")]
            unpacked = LC3377Readout(fifoData)
            
            if len(unpacked.events) > 0:
                lastevent = unpacked.events[-1]
                for datum in lastevent.data:
                    tdcData[(slot,datum.channel)]=datum.tdc
        
        eventRecord["unpacked3377Data"] = tdcData


