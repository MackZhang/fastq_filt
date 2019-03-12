# fastq_filt
This python script is used for seperating fastq reads according index or barcode from raw reads. The raw reads can be unziped or gziped file.
This script can seperate reads by multi-index or multi-barcode at same time, so it saves time compare with other scripts.

## Requirements
To run this script, you just need a raw reads file and indexs or barcode. Although this script can seperate reads from gziped file, but unziped file will be much more faster than gziped file.

### Notes: The index sequences should be same with the sequence in p7 primer. 

## Usage

```
Usage: fastq_filt.py [options]

Options:
  -h, --help            show this help message and exit
  -f, --input		INPUT_FILE
                        File for processing
  -o, --output		OUTPUT_FILE
                        File for output
  --Barcode             using barcode for selection
  --Index               using index for selection
  -s, --barcodeindex	BARCODE_OR_INDEX_SEQUENCE
                        fastq barcode or index sequence
  -l, --left		LEFT_CUT
                        sequence for cut in left sides
  -r, --right		RIGHT_CUT
                        sequence for cut in right sides
Example: python fastq_filt.py --Index -f Raw.fq.gz -s TAATAC,TGTGTC -o index-1.fq,index-2.fq -l 10 -r 40
Example: python fastq_filt.py --Barcode -f Raw.fq -s TAATACCCATCG,TGTGTCCAG -o barcode-1.fq,barcode-2.fq -l 10 -r 40
```
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

