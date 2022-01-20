# reciprocalBlast
Protocol to perform a reciprocal blast for comparison of two genome annotation versions based on different genome assemblies.

Reciprocal Best Hits (RBH) blast is a common method for infering putative orthologs.

*Requisites:*
* python version 3.6 or higher
  * Libraries: biopython and progressbar
    ```
    pip install biopython
    pip install progressbar
    ```
* blast+: download from https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download

# **Forward blastn**

Create a database with genome2 gene sequences.

```
mkdir reciprocal_blast
cd ./reciprocal_blast

# DB of genes in genome2.
mkdir genome2_db
makeblastdb -in <path/to/genome2_seq.fasta> -dbtype nucl -out <path/to/genome2_db
```

Create a directory with a fasta file for each gene in genome1.

```
mkdir genome1_genes

python parse_genes.py -f <path/to/genome1_seq.fasta> -d <path/to/genome1_genes>

ls | wc -l # check that there are as many fasta as there are genes in genome1.
```

Blastn of genes in genome1 to genome2.

```
mkdir blast_forward
cd blast_forward/
nohup ../blast_forward.sh &
```

# **Backward blastn**

Create a database with genome1 gene sequences.

```
# DB of genes in genome1.
mkdir genome1_db
makeblastdb -in <path/to/genome1_seq.fasta> -dbtype nucl -out <path/to/genome1_db
```

Create a directory with a fasta file for each gene in genome2.

```
mkdir genome2_genes

python parse_genes.py -f <path/to/genome2_seq.fasta> -d <path/to/genome2_genes>

ls | wc -l # check that there are as many fasta as there are genes in genome2.
```

Blastn of genes in genome2 to genome1 with only one alignment. because you only want to record the best alignment partner in the genome.


```
mkdir blast_backward
cd blast_backward/
nohup ../blast_backward.sh &
```

# **RBH analysis**

Anlaysis of results from forward and backward blastn.

Parse xml files from both blastn to get the correspondence between genes in both genomes.
A RBH is considered when genome1 gene's hit (genome2 gene) in forward blast has as best hit the genome1 gene in backward blast.

```
nohup python -u ../parse_xml_reciprocal_blast.py -blastf < /path/to/ blast forward xml files directory > -blastb < /path/to/  blast backward xml files directory > -o < /path/to/ output directory > &
```

*Output:*
* tab separated table with the following columns:

| Genome1 gene | Corresponding genome2 gene | RBH
| ---          | ---                        | ---
| \<str\>        | \<str\>                      | \<str\>
 
> "RBH" string in RBH column indicates genome1 gene has a corresponding genome2 gene indicated in "Corresponding genome2 gene" column.
