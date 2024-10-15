# fasta to csv (beta)
***
Converting a .fasta to a .csv takes a lot of steps and a lot of attention. This program creates a list of commands you can copy paste into your terminal to streamline this process. 

This project is in `beta`, it functions, but is still being worked on for clarity and ease of use
# prerequirements
- Python: Runs the program
- bowtie2
- samtools
- igvtools

## prerequirement instilation
**Recommend to create a new conda environment first**

`conda create -n YOUR_ENV_NAME python`

`conda activate YOUR_ENV_NAME`

```
conda install bioconda::bowtie2
conda install bioconda::samtools
conda install bioconda::igvtools
```

# Set Up
## Create your "working directory"
This program assumes a specific file organization format. There should be a folder, here to referred as the "working directory", which contains two folders: `index` and `input`. Every time the program is ran, the files created will be stored in a newly created `output` folder inside the "working directory".

\*Note, title of "working directory" is irrelevant. 
\*\*There can be other files inside the "working directory"

```
your_working_directory
  |
  + input
  + index
  |
  . misc
  . misc
```

## Locate Working Directory
Inside the `fasta_2_csv` folder there is a folder called `routing.txt`
Replace the placeholder working directory with the location of file path of the working directory you are using
## Using Working Directory
`index`: Includes all genomic indexes
- Bowtie2 will look for indexes to create inside this folder
- Bowtie2 will store created indexes inside this folder
`input`: Includes all .fasta files to convert 
- Ex:
	- `1_S201_R1_001.fastq.gz`
	- `1_S201_R2_001.fastq.gz`
# Procedure
## Create New Index with Bowtie2
This step should be performed once per index file. Once initialized, this step does not need to be performed again. 

Run `python sort_csv.py -i YOUR_INDEX_NAME`

Bowtie2 will try find the file `YOUR_INDEX_NAME.fasta` inside the `index` folder, and create the index inside the `index` folder.
## Running sort_csv.py
1. `python sort_csv.py`
2. Prompt: `Index Name? `
	- Type name of index you are using
3. Prompt: `Output Name? `
	- Type name for the created output files
4. Confirm Input
	- List of input files read by program is given
5. Paste Commands into Terminal
