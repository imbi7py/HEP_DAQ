"""                                                                             
This example config file tells which ADC channels are connected
"""

def configureDAQ(h):
    config = dict()
    config["connected_channels"] = ((17, 0), (17, 1), (17, 2))
    return config
