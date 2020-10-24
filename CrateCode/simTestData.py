#!/usr/bin/env python3
import os, sys, csv, time
from runCAMAC import runCAMAC
from ADCHisto import ADCHisto, TDCHisto
from MultipleUpdater import *
from ..CrateAnalysis.sas_analyis import *
"""
Usage: takeData.py configModule maxEvents maxTimeSec runNumber outputFile

Set "configModule" to "None" if the default DAQ configuration is acceptable.
Set "maxEvents" to 0 if the code should run until maxTimeSec seconds elapse.
Set "maxTimeSec" to 0 if the code should run until maxEvents events are taken.
Set "outputFile" to "None" if you just want to plot some events.
"""


def takeData(totalEvents, test_num, doPlot):
    configModule = "NuralTest"
    maxEvents = totalEvents
    maxTimeSec = 0
    runNumber = test_num
    outputFile = "test{}.bin".format(test_num)
    # Check argument validity
    ok = True
    if maxEvents < 0:
        print("Invalid number of events (can not be negative)")
        ok = False
    if maxTimeSec < 0:
        print("Invalid run time (can not be negative)")
        ok = False
    if not ok:
        print(__doc__)
        return 1
    global MUONRATE
    wtime = round(totalEvents * float(MUONRATE))
    if doPlot:
        print("Starting DAQ system with diagnostic plots...")
    else:
        print("Starting DAQ system....")
    print("Process will take roughly {} mins".format(wtime))
    # Configure the histogram plotter.
    # The channels to plot: a tuple of (slot, channel) pairs.
    # "None" will take all channels configured in the DAQ.
    channels_to_plot = None
    nBins = 100
    updateAfterHowManyEvents = 5
    verticalSpaceAdjustment = 0.4
    adcHisto = ADCHisto(nBins, updateAfterHowManyEvents,
                        verticalSpaceAdjustment, channels_to_plot)
    tdcHisto = TDCHisto(nBins, updateAfterHowManyEvents,
                        verticalSpaceAdjustment, channels_to_plot)

    plotUpdater = plotDiagnostics(doPlot, adcHisto, tdcHisto)
    n, t, s, err = runCAMAC(configModule, maxEvents, maxTimeSec, runNumber,
                            outputFile, plotUpdater)

    print('Processed %d events in %g sec' % (n, t))
    print('Run status is', s)
    if s == "Error":
        print('Error message:', err)
    if not (outputFile == "None" or outputFile == "none"):
        print('Run %d data is stored in the file "%s"' %
              (runNumber, outputFile))
    return outputFile


def updateEnvVar():
    r = csv.reader(open('daq_env_var.csv'))  # Here your csv file
    lines = list(r)
    test_num = int(lines[0][1])
    lines[0][1] = test_num + 1
    writer = csv.writer(open('daq_env_var.csv', 'w'))
    writer.writerows(lines)
    return test_num


def plotDiagnostics(doPlot, adcHisto, tdcHisto):
    if doPlot:
        return MultipleUpdater(adcHisto, tdcHisto)
    else:
        return None


if __name__ == "__main__":
    MUONRATE = 0.003298866666666666
    totalEvents = int(sys.argv[1])
    doPlot = sys.argv[2]
    if doPlot == "True":
        doPlot = True
    elif doPlot == "False":
        doPlot = False
    testNum = updateEnvVar()
    in1 = takeData(totalEvents, testNum, doPlot)
    main(["junk", in1])