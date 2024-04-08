# Code Review 10 April 2024. 
This repo contains scripts to calculate Linkage Disequilibirum (LD) measures. Info on LD:
https://docs.google.com/presentation/d/1I6e-q22om6AiI-cYjlJ7pJ3f5w0gQTDE/edit?usp=sharing&ouid=115928088663191390220&rtpof=true&sd=true 

## Requirements
* csv
* pandas 
* matplotlib.pyplot 
* numpy
* itertools

## Scripts 
1. PyLD.py - contains functions to read a VCF, obtain genotype, obtain haplotype, calculate LD measures, outputs a dictionary of LD measures for each rs ID pair, and can create a CSV file of the output.
2. heatmaps.py - contains functions to create a heatmap each of the LD measures.

## Examples
* example.ipynb - An example of how to run the code.
* toy_data.vcf - Example data. This is actually a subset of the British population VCF from 1000 Genomes Project
* toy_data_output.csv - Example output from the PyLD.py script. 
* r2.png, dprime.png - Example outputs from the heatmaps.py script.

## PyPi scripts
* setup.py - set up code to set up as a PyPi packed - stil to do.

## Things I'd like feedback/advice on
* structure of repo
* setting up a PyPi package
* any code advice - e.g my use of functions and classes?
* tests?
* poetry?
* anything else :)
