dirGenes=$1 # Path/to/fasta with all genes of genome.
dirDB=$2 # Path/to/database.
for f in "$dirGenes"*.fasta
do
	file_name=$(basename -- "$f")
	blastn -query "$f" -db $dirDB -out "${file_name}_fasta_blast.xml" -outfmt 5 -num_alignments 1
	echo "${f} done."
done
