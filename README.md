# BookRoll Annotator

## Overview
BookRoll Annotator merges PDF file and log data and returns the annotated version of the files.

Original PDF

![original](docs/original_img.png)

Annotated PDF 

![annotated](docs/annotated_img.png)

## Requirements
+ Python 3.6.9
+ Ubuntu 18.04

## Get Started

1. COPY PDF Files in `pdfs` directory.
2. COPY BookRoll EventStream as `eventstream.csv` in `logdata` directory. 
3. Install the libraries.
4. Run `python main.py`
5. After running the script, the annotated pdfs should be in `output_pdf` directory.

## Contributors
Nozomi Kuromu, Hiroyuki Kuromiya