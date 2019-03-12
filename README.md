# fastq_filt
This python script is used for seperating fastq reads according index or barcode from raw reads. The raw reads can be unziped or gziped file.
This script can seperate beads by multi-index or multi-barcode at same time, so it saves time compare with other scripts.

## Requirements
To run this script, you just need a raw reads file and indexs or barcode.

## Usage
$ python fastq_filt.py --Index -f raw_input.fq.gz -s ATCTAC,CGATCA,CATCGC -o index_1.fq,index_2.fq,index_3.fq -l 10 -r 50 
$ python fastq_filt.py --Barcode -f raw_input.fq.gz -s ATCTACGCCG,CGATCATATCTTTCGCA -o barcode_1.fq,barcode_2.fq -l 20 -r 50 

### The options
#### Required:
##### --Index
If you use index to seperate reads, you should chose this options.
##### --Barcode
If you use Barcode to seperate reads, you should chose this options. It can not appear with "--Index" options at same time.
##### -f, --input
This is your raw input reads file, it can be unziped file or gziped file.
##### -o, --ofile
This is your output file, you can name it by yourself
##### -l, --reference
If you need cut the reads at left position, you should set this options 
##### -r, --min_num
If you need cut the reads at right position, you should set this options 

