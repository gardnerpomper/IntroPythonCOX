#!/usr/bin/env python
import sys
import csv
import os.path

def loadSolarWinds(fp):
    """
    load the SolarWinds dump, keyed by IP address
    """
    solarD = {}
    csvR = csv.DictReader(fp)
    for record in csvR:
        solarD[record['Exporter']] = record
    return solarD

def loadStealthWatch(fp):
    """
    load the distinct IP addresses from the StealthWatch dump
    """
    stealthIPs = set()
    csvR = csv.reader(fp)
    for ii,record in enumerate(csvR):
        if ii == 0: continue
        stealthIPs.add(record[0])
    return stealthIPs

def find_missing(solarWindsFname, stealthWatchFname):
    """
    find the IPs that in solarWinds, but not stealthWatch
    """
    stealthIPs = set()
    with open('/Users/gardner/Downloads/RCStealthWatchExport.csv','r') as fp:
        stealthIPs = loadStealthWatch(fp)
    print ('%d distinct IPs in StealthWatch' % len(stealthIPs))
    """
    solarD = {}
    with open('/Users/gardner/Downloads/RCSolarWindsExport.csv','r') as fp:
        solarD = loadSolarWinds(fp)
    print ('%d SolarWinds records' % len(solarD.keys()))

    solarIPs = set(solarD.keys())
    missing = solarIPs - steathIPs
    print( '%d IPs missing from StealthWatch' % len(missing))
    print( missing)
    """

if __name__ == '__main__':
    solarFname = '/Users/gardner/Downloads/RCSolarWindsExport.csv'
    stealthFname = '/Users/gardner/Downloads/RCStealthWatchExport.csv'

    find_missing(solarFname,stealthFname)
