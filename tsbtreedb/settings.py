#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# CS207 Group Project Part 7
# Created by Team 2 (Jonne Seleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah) for Team 4

# Central place to store a couple of global variables

import os
import sys

# Hacky solution to import array time series from sister directory by inserting it into system path
# should fix once time series library is turned into a proper python model

from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.insert(0,d + '/timeseries')
import ArrayTimeSeries as ats

LIGHT_CURVES_DIR = "light_curves/"
DB_DIR = "vp_dbs/"
SAMPLE_DIR = "sample_data/"
TEMP_DIR = "temp/"
TS_LENGTH = 100 #Number of data points for generated time series
