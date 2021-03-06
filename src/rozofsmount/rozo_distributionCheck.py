#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import subprocess
import time
import re
import shlex


clusters = []

#____________________________________
# Class sid
#____________________________________
class cluster:
  def __init__(self, cid): 
    if len(clusters) == 0 and cid != 0: cluster(0) 
    self.cid = cid
    self.nbFiles = 0
    self.sidMax = 0
    self.inverse=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    self.forward=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    self.spare=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    clusters.append(self)
  	
  @staticmethod
  def get_cluster(cid):
    global clusters
    for c in clusters: 
	  if cid == c.cid: return c
    cluster(cid)
    for c in clusters: 
	  if cid == c.cid: return c	  
    return None
	
  def add_file(self,dist):
    c0 = cluster.get_cluster(0)
    c0.nbFiles = c0.nbFiles + 1
    self.nbFiles = self.nbFiles + 1
    nb=int(0)
    for id in dist.split('-'):
      id=int(id)
      if id > self.sidMax: self.sidMax = id
      if id > c0.sidMax: c0.sidMax = id
      if nb<inv :  
        self.inverse[id] = self.inverse[id] +1
        c0.inverse[id]   = c0.inverse[id] +1
      if nb<fwd :  
        self.forward[id] = self.forward[id] +1
        c0.forward[id]   = c0.forward[id] +1		
      if nb>=fwd : 
        self.spare[id] = self.spare[id] +1
        c0.spare[id]   = c0.spare[id] +1		
      nb=nb+1
	  
  @staticmethod
  def display_cluster():  
    for c in  clusters: 	
      i = 1
      if c.cid == 0:
        print "\n  %s files in all clusters"%(c.nbFiles)	  
      else:
        print "\n  %s files in cluster %d"%(c.nbFiles,int(c.cid))
      print "   ____ _______ _______ _______"
      print "  |SID |  Read | Write | Spare |"
      print "  |____|_______|_______|_______|"
      while i <= c.sidMax:
        print "  | %2d | %5d | %5d | %5d |"%(i,c.inverse[i],c.forward[i],c.spare[i])
        i=i+1
      print "  |____|_______|_______|_______|"

#___________________________________________    

if len(sys.argv) < 2:
  path=os.getcwd()
else:
  path=sys.argv[1]
  if path[0] != '/':path="%s/%s"%(os.getcwd(),path)
path=os.path.abspath(path)

layout=255
string="attr -g rozofs %s"%(path)
parsed = shlex.split(string)
cmd = subprocess.Popen(parsed, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
for line in cmd.stdout:
  if not "LAYOUT" in line: continue
  layout=int(line.split(':')[1])
  break
  
if layout == 255:
  print "%s seems not to be a mounted RozoFS path"%(path) 
  sys.exit(1)
   
if layout == 0:
  inv=2
  fwd=3
  safe=4
elif layout == 1:     
  inv=4
  fwd=6
  safe=8
elif layout == 2:
  inv=8
  fwd=12
  safe=16
  
nbFiles=0  
sidMax=int(0)
for f in os.listdir(path):  
  string="attr -g rozofs %s/%s"%(path,f)
  nbFiles=nbFiles+1
  parsed = shlex.split(string)
  cmd = subprocess.Popen(parsed, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  for line in cmd.stdout:
    if "CLUSTER" in line: cid=line.split(':')[1]
    if not "STORAGE" in line: continue
    dist=line.split(':')[1]
#    print "%2d: %s"%(i,dist)
    c = cluster.get_cluster(cid)
    c.add_file(dist)
    break

print "%s files under %s"%(nbFiles,path)
cluster.display_cluster()
