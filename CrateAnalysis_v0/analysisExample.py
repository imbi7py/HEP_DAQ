#!/usr/bin/env python3
"""
Usage: analysisExample.py outputPrefix inputFile0 ...
"""

import sys
from runAnalysisSequence import runAnalysisSequence
from UtilityModules import *
from ADCPrintingModule import *
from TDCPrintingModule import *
from GenericPrintingModule import *
from HistoMaker1D import *
from ADCHisto import *
from datetime import datetime

def main(argv):
    # Parse command line options
    argc = len(argv)
    if (argc < 2):
        # Convention used here: command invoked without any arguments
        # prints its usage instruction and exits successfully
        print(__doc__)
        return 0

    outputPrefix = argv[0]
    inputFiles = argv[1:]

    # Example histogram specifier
    h0 = Histo1DSpec("Dead Time", "Counts", 100, lambda x: x["deadtime"])

    # Create various analysis modules
    mod0 = VerboseModule("VerboseModule", True, True, 10, True, True)
    mod1 = EventCounter("Counter 0")
    mod2 = DutyCycleModue("DC0", 100)
    mod3 = ADCPrintingModule(outputPrefix + "_adc")
    mod4 = EventCounter("Counter 1")
    mod5 = TDCPrintingModule(outputPrefix + "_tdc")
    gptr = GenericPrintingModule(("hw_event_count", "deadtime"))
    hMaker = HistoMaker1D((h0,))
    adcPlotter = ADCHisto(100, 5, 0.4)
    tdcPlotter = TDCHisto(100, 5, 0.4)

    # Define the sequence of modules
    # modules = (mod0, mod1, hMaker, plotUpdater, mod2, mod3, gptr, mod4)
    # modules = (mod0, mod1, mod3, mod5)
    modules = (mod0, mod1, adcPlotter, tdcPlotter)

    # Call the code which actually does the job
    t0 = datetime.now()
    n = runAnalysisSequence(modules, inputFiles)
    dt = datetime.now() - t0

    # Print a mini summary of event processing
    print('Processed %d events in %g sec' % (n, dt.total_seconds()))
    return 0

if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))
