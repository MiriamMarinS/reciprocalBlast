# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 09:17:48 2020

@author: Miriam Marin Sanz
"""


from Bio import SeqIO
import argparse


# Arguments.
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-f', '--fasta', help = "Relative path and file name of the fasta file")
parser.add_argument('-d', '--directory_out', help = "Relative path of the output directory")

args = parser.parse_args()

fasta_file = args.fasta
directory = args.directory_out

# Iterate across sequences in fasta and create individual fasta files.
for record in SeqIO.parse(fasta_file, "fasta"):
    fasta_new = open(directory + str(record.id) + ".fasta", "w+")
    fasta_new.write(">" + str(record.id) + "\n")
    fasta_new.write(str(record.seq) + "\n")
