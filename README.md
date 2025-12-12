
# HMMER for annotated whole genomes

This shows how to make the HMM profile for the gene/protein of interest, and then scan the target .faa files for the presence of HMM sequence
### 1. Obtain known sequences corresponding to the protein of interest from UniProt database
	
  a. Go to Uniprot

  b. Type in the protein that you are looking for in the search bar and select the reviewed entries of interest.
The limit of download is 100 sequence at a time, if you have more download as several files and then concatenatet the sequences into one fasta file.

  c. Download the sequences as "canonical" fasta.  (Isoforms are relevant only in eukaryotes)

  d. It will be downloaded as a zip file with a protein.fasta sequences, extract the content.

### 2. Building the HMM profile

	
  a. The extracted .fasta may contain duplicated sequences, remove duplicates:
		in wsl:
```bash
	seqkit rmdup 1.uniprot_seq.fasta > 2.clean_seq.fasta
```
  b. Align the cleaned sequences
		in wsl:

```bash
   	mafft --auto 2.clean_seq.fasta > 3.seq_aligned.fasta
   ```
	
  c. Build the HMMprofile
```bash
    hmmbuild 4.seq.hmm 3.nifH_seq.fasta
   ```
		

### 3. searching the whole genomes for the presence of target protein.
	  
  a. Annotate all the genomes and move all the .faa files into one directory.
	  
  b. HMM search for the target protein using the ```1.nifH_pipeline.py```     script and making the matrix using ```2.nifH_matrix_scores.py script```.The input/output has to be changed based ion the target sequence

  HMM_search_on_WholeGenomes


```bash
    #generate the hmm result tables, and compile them into candidate csv and presence absence csv.
		python3 1.nifH_pipeline.py path/to/.faa/file/folder/

    #generate the matrix to build the heatmap for the hits. 
		python3 2.nifH_matrix_scores.py --infile nifH_candidates_allgenomes.cs
```



