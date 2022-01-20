# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 08:00:59 2022

@author: Miriam Marin Sanz
"""

#Parse xml of reciprocal blast for genome1 genes and genome2 genes.



from Bio.Blast import NCBIXML
from os import listdir
from os.path import isfile, join
from progressbar import *
import argparse


# Arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-blastf', '--blast_forward', help = "/path/to/ blast forward xml files directory")
parser.add_argument('-blastb', '--blast_backward', help = "/path/to/ blast backward xml files directory")
parser.add_argument('-o', '--output', help = "/path/to/ output directory")

args = parser.parse_args()

widgets = ['Test: ', Percentage(), ' ', Bar(marker='0',left='[',right=']'),
           ' ', ETA(), ' ', FileTransferSpeed()] #see docs for other options

#%% Functions and classes.

class Blastparse():
    def __init__(self, path, xmlFile):
        self.path = path
        self.xmlFile = xmlFile
        self.parse()
        
    def parse(self):
        try:
            result_handle = open(self.path + self.xmlFile)
        except:
            print("File " + xmlFile + " could not be opened.")
        blast_record = NCBIXML.read(result_handle)
        self.alignments_list = []
        # Loop through the XML file
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                gene_id = alignment.title.split(" ")[1].strip()
                score = hsp.score
                evalue = hsp.expect
                if (gene_id, score, evalue) not in self.alignments_list: self.alignments_list.append((gene_id, score, evalue))
        
        result_handle.close()

class Filterhits():
    def __init__(self, geneBlastF_id, geneBlastF_features, dict_BlastB):
        self.geneBlastF_id = geneBlastF_id
        self.geneBlastF_features = geneBlastF_features
        self.dict_BlastB = dict_BlastB
        self.filterRBH()
    
    def filterRBH(self):
        self.RBH = "NO"
        self.geneblastB = "NO"
        for alignment in self.geneBlast1_features.alignments_list:
            geneB_id = alignment[0]
            
            try:
                if self.dict_BlastB[geneB_id].alignments_list[0][0] == self.geneBlastF_id:
                    self.RBH = "RBH"
                    self.geneblastB = geneB_id
                    # Keep the first hit of blast forward: with best score and evalue.
                    break
            except:
                print("No file with genome2 gene ID " + geneB_id)

#%% Path.

path_blastF = args.blast_forward
path_blast_backward = args.blast_backward
path_output = args.output

#%% Parse xml of blast forward.

#List of files in directory blast forward.
xml_blastF = [f for f in listdir(path_blastF) if isfile(join(path_blastF, f)) and f.endswith(".xml")]

print("Start parse of xml from blast forward.")


#Dict of xml results for each gene of genome1 in blast forward: the dict contain list of tuples: gene_id, score and evalue for each hit per gene in genome1.
blastF_dict = {}
count = 0
pbar = ProgressBar(widgets=widgets, maxval=len(xml_blastF))
pbar.start()
for xmlFile in xml_blastF:
    file_name = xmlFile.split("/")[-1].split(".")[0].strip()
    blastF_dict[file_name] = Blastparse(path_blastF, xmlFile)
    count += 1
    pbar.update(count)

pbar.finish()    

print("Parse of " + str(len(blastF_dict)) + " xml files in blast forward.")

#%% Parse xml of blast_backward.

#List of files in directory blast_backward.
xml_blast_backward = [f for f in listdir(path_blast_backward) if isfile(join(path_blast_backward, f)) if f.endswith(".xml")]

print("Start parse of xml from blast backward.")

#Dict of xml results for each gene of genome2 in blast forward: the dict contain list of tuples: gene_id, score and evalue for each hit per gene in genome2.
blastB_dict = {}
count = 0
pbar = ProgressBar(widgets=widgets, maxval=len(xml_blast_backward))
pbar.start()
for xmlFile in xml_blast_backward:
    file_name = xmlFile.split("/")[-1].split(".")[0].strip()
    blastB_dict[file_name] = Blastparse(path_blast_backward, xmlFile)
    count += 1
    pbar.update(count)

pbar.finish()   

print("Parse of " + str(len(blastB_dict)) + " xml files in blast backward.")

#%% Comparation of blast results.

print("Comparative analysis starts.")
result_dict = {}
count = 0
pbar = ProgressBar(widgets=widgets, maxval=len(blast1_dict))
pbar.start()
for geneblastF, features in blastF_dict.items():
    result_dict[geneblastF] = Filterhits(geneblastF, features, blastB_dict)
    count += 1
    pbar.update(count)

pbar.finish()

print("Comparative analysis done.")

#%% Write results.

print("The results are being writed.")
blastFile = open(path_output + "results_reciprocal_blast.txt", "w+")

blastFile.write("Genome1_gene" + "\t" + "Genome2_gene" + "\t" + "RBH" + "\n")

count = 0
pbar = ProgressBar(widgets=widgets, maxval=len(result_dict))
pbar.start()
for geneblastF, values in result_dict.items():
    geneblastB = values.geneblastB
    RBH = values.RBH
    blastFile.write(geneblastF + "\t" + geneblastB + "\t" + RBH + "\n")
    count += 1
    pbar.update(count)

pbar.finish()

print("Writing results done.")
