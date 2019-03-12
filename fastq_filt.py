#!/usr/bin/env python

import gzip
import re
import os, sys
from os import system
from optparse import OptionParser
import datetime

parser = OptionParser()
parser.add_option("-f", "--input", action="store", type="string", dest="input_file", help="File for processing")
parser.add_option("-o", "--output", action="store", type="string", dest="output_file", help="File for output")
parser.add_option("--Barcode", action="store_true", dest="barcode_selection", help="using barcode for selection")
parser.add_option("--Index", action="store_true", dest="index_selection", help="using index for selection")
parser.add_option("-s", "--barcodeindex", action="store", type="string", dest="barcode_or_index_sequence", help="fastq barcode or index sequence")
parser.add_option("-l", "--left", action="store", type="int", dest="left_cut", default="0", help="sequence for cut in left sides")
parser.add_option("-r", "--right", action="store", type="int", dest="right_cut", default="150", help="sequence for cut in right sides")
(options, args) = parser.parse_args()
if not(options.input_file and options.barcode_or_index_sequence and options.output_file and (options.barcode_selection or options.index_selection)):
  print
  parser.print_help()
  print 'Example:','\033[1;31mpython fastq_filt.py --Index -f Raw.fq -s TAATAC,TGTGTC -o index-1.fq,index-2.fq -l 10 -r 40\033[0m'
  print 'Example:','\033[1;31mpython fastq_filt.py --Barcode -f Raw.fq -s TAATACCCATCG,TGTGTCCAG -o barcode-1.fq,barcode-2.fq -l 10 -r 40\033[0m'
  sys.exit(0)
if options.barcode_selection and options.index_selection:
  print
  print '\033[1;31mCan NOT choice "--Barcode" and "--Index" at same time!\033[0m'
  parser.print_help()
  print 'Example:','\033[1;31mpython fastq_filt.py --Index -f Raw.fq -s TAATAC,TGTGTC -o index-1.fq,index-2.fq -l 10 -r 40\033[0m'
  print 'Example:','\033[1;31mpython fastq_filt.py --Barcode -f Raw.fq -s TAATACCCATCG,TGTGTCCAG -o barcode-1.fq,barcode-2.fq -l 10 -r 40\033[0m'
  sys.exit(0)


def index_rc(index_seq):
  RC_index = []
  for i in range(index_num):
    index = index_seq[i].strip()
    index = index.replace('A','{A}').replace('T','{T}').replace('C','{C}').replace('G','{G}').replace('N','{N}')
    rc_index = index.format(A='T',T='A',C='G',G='C', N='N')[::-1]
    RC_index.append(rc_index)
  return RC_index

def open_method(rawfile, op):
  if rawfile.split('.')[-1] != 'gz':
    op = open
  else:
    op = gzip.open
  return op

op = ''
op = open_method(options.input_file, op)

def index_filt(rawfile, index_seq, dic, left, right):
  pattern = '@.+ \d:\D:\d:(\D+)'
  i = 0
  with op(rawfile, 'r') as fi:
    for line in fi:
      if i%40000000 == 0:
        now_time = datetime.datetime.now()
        now_time = str(now_time).split(' ')[1]
        print '%s Reads: %s million' %(str(now_time).split('.')[0], i/4000000)
      if i%4 == 0:
        INDEX = re.match(pattern, line).group(1).strip()
        for index in index_seq:
          if INDEX[0:len(index)] == index:
            dic[index].write(line+fi.next()[left:right]+'\n'+fi.next()+fi.next()[left:right]+'\n')
            i += 3
      i += 1 

def barcode_filt(rawfile, index_seq, dic, left, right):
  i = 0
  with op(rawfile, 'r') as fi:
    for line in fi:
      if i%40000000 == 0:
        now_time = datetime.datetime.now()
        now_time = str(now_time).split(' ')[1]
        print '%s Reads: %s million' %(str(now_time).split('.')[0], i/4000000)
      if i%4 == 0:
        dress = line
        seq = str(fi.next())
        read = str(dress+seq[left:right]+'\n'+fi.next()+fi.next()[left:right]+'\n')
        i += 3
        for index in index_seq:
          if seq[0:len(index)] == index:
            dic[index].write(read)
      i += 1

dic = {}
index_seq = (options.barcode_or_index_sequence).split(',')
output = (options.output_file).split(',')
index_num = len(index_seq)

begin = datetime.datetime.now()
if options.index_selection:
  index_seq = index_rc(index_seq)
  for i in range(0, index_num):
    index = index_seq[i]
    dic[index] = open(output[i].strip(), 'w')
  index_filt(options.input_file, index_seq, dic, options.left_cut, options.right_cut)

if options.barcode_selection:
  for i in range(0, index_num):
    index = index_seq[i]
    dic[index] = open(output[i].strip(), 'w')
  barcode_filt(options.input_file, index_seq, dic, options.left_cut, options.right_cut)     
end = datetime.datetime.now()
time = end -begin
print '\033[1;31mTotal running time: %s\033[0m' %(str(time).split('.')[0])       

for index in index_seq:
  dic[index].close()


