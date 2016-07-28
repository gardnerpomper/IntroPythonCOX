
# coding: utf-8

# In[112]:

import sys
import csv
import os.path
import re
from collections import defaultdict
import logging


# In[137]:

def loadSolarWinds(fp):
    """
    load the SolarWinds dump, keyed by IP address
    but only selected records (*_(R|VR)*)
    """
    solarD = {}
    csvR = csv.DictReader(fp)
    for ii,record in enumerate(csvR):
        m = re.match('[A-Z]+_(?P<group>R|VR)',record['Node'])
        if m == None: continue
        record['group'] = m.groupdict()['group']
        solarD[record['IP Address']] = record
    return solarD


# In[73]:

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


# In[74]:

def load(solarFname, stealthFname):
    """
    return the set of IPs in stealthWatch
    and the full records from solarWinds
    """
    stealthIPs = set()
    with open(stealthFname,'r') as fp:
        stealthIPs = loadStealthWatch(fp)

    solarD = {}
    with open(solarFname,'r') as fp:
        solarD = loadSolarWinds(fp)

    return solarD, stealthIPs


# In[75]:

def find_missing(solarD, stealthIPs):
    """
    return the IPs that in solarWinds, but not stealthWatch
    """
    solarIPs = set(solarD.keys())
    missing = solarIPs - stealthIPs
    return missing


# In[76]:

def report(solarD,missing):
    """
    generate a report (list of formatted strings) showing
    the IPs that are missing, grouped by the owning org
    """
    reportL = []
    groupD = defaultdict(list)
    #
    # ----- put each missing IP into the correct
    # ----- group
    #
    for ip in missing:
        solar = solarD[ip]
        groupD[solar['group']].append(solar)
    #
    # ----- list of strings has the group name and count
    # ----- and then an indented list of detail records 
    # ----- for each group
    #
    for group, groupL in sorted(groupD.items()):
        reportL.append( '{0} is missing {1} entries in StealthWatch'.format(group,len(groupL)))
        reportL.append('\t' + '\n\t'.join(
                ['{0}\t{1}'.format(
                        record['Node'],record['IP Address']
                    ) for record in sorted(groupL,key=lambda rec:rec['Node'])]
            ))
    return reportL


# In[125]:

def main(solarFname,stealthFname,fp):
    """
    top level routine that calls out to the subroutines
    that do the actual work:
        load - load the files
        find_missing - compare the IPs in each file
        report - generate the output
    """
    solarD, stealthIPs = load(solarFname, stealthFname)
    logging.info('%d distinct IPs in StealthWatch' % len(stealthIPs))
    logging.info('%d SolarWinds records' % len(solarD.keys()))

    missing = find_missing(solarD,stealthIPs)
    logging.info( '%d IPs missing from StealthWatch' % len(missing))
    fp.write( '%d IPs missing from StealthWatch\n' % len(missing))

    reportL = report(solarD,missing)
    fp.write('\n'.join(reportL)+'\n')


# In[126]:

def inJupyter():
    """
    check to see if we are running in teh jupyter notebook or
    from regular python
    """
    try:
        get_ipython()
        in_notebook = True
    except NameError as e:
        in_notebook = False
    return in_notebook


# In[139]:

if __name__ == '__main__':
    from argparse import ArgumentParser
    import sys

    parser = ArgumentParser(description='Find mismatches between SolarWinds and Stealth')
    parser.add_argument('solarFname')
    parser.add_argument('stealthFname')
    parser.add_argument('-o','--output',action='store')
    parser.add_argument('-d','--debug',action='store_true')
    #
    # ------ can't use actual command line if we are in Jupyter notebook
    #
    cmd_args = sys.argv
    if inJupyter():
        cmd_args = ['/Users/gardner/Downloads/Solar.csv'
                    ,'/Users/gardner/Downloads/RCStealthWatchExport.csv'
                    #,'-d'
                    ,'-o', 'missing.out'
                    ]
    args = parser.parse_args(cmd_args)
    #
    # ----- configure based on command line args
    #
    level = logging.DEBUG if args.debug else logging.INFO
    if inJupyter():
        import importlib
        importlib.reload(logging)
    logging.basicConfig(filename='missing.log',level=level,filemode='w')

    if args.output is None:
        main(args.solarFname,args.stealthFname,sys.stdout)
    else:
        with open(args.output,'w') as fp:
            main(args.solarFname,args.stealthFname,fp)


# In[ ]:



