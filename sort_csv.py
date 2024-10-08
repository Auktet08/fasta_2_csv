import os
import sys
from datetime import datetime

def main():
    # change working directory : PROMPT
    with open ("Routing.txt", "r") as infile:
        _, wd = infile.readline().strip().replace(" ","").split("=")
    # update input and index directories
    global input_path
    global index_path
    input_path = f"{wd}/input"
    index_path = f"{wd}/index"

    # list of all files in input
    dir_list = os.listdir(input_path)
    r1,r2 = pairing(dir_list)

    # initializing index
    index = indexer()

    # initializing outputs
    output_file = input("Output Name? ")              
    output_path = f"{wd}/{datetime.today().strftime('%Y-%m-%d_%H%M%S')}_{output_file}"
    temp_path = f"{output_path}/temp"

    # proceed? 
    output_confirmation(output_path, output_file, r1, r2)
    
    # create same files in temp folder
    bowtie_sam(output_path, output_file, temp_path, index, r1, r2, offset=1)

    samtools(output_path, output_file, temp_path, r1, offset=1)

    igvtools(output_path, output_file, index, r1, offset=1)


def pairing(dir_list):
    r1 = []
    r2 = []

    dir_list.remove(".DS_Store")
    dir_list.sort()

    # creates pairs
    for i in range(len(dir_list)):
        file = dir_list[i]
        if not file.startswith("."):
            # even
            if i % 2 == 0:
                r1.append(file)
            # odd
            if i % 2 == 1:
                r2.append(file)

    if len(r1) != len(r2):
        print(r1)
        print(r2)
        sys.exit("check input folder, odd number detected")
    return(r1, r2)

def indexer():
    try:
        if sys.argv[1] == "-i":
            index = bowtie(sys.argv[2])
        elif sys.argv[1] is not None:
            index = sys.argv[1]
    except IndexError:
        index = input("Index Name? ")
    
    if not os.path.isfile(f"{index_path}/{index}.fasta.fai"):
        # create fasta.fai
        print("===create .fasta.fai samtools===")
        print(f"samtools faidx {index_path}/{index}.fasta")
    return index

def bowtie(index):
    print("=== create bowtie index ===")
    index_genome_file = f"{index_path}/{index}.fasta"   
    # create index inside index folder then leave index folder
    print(f"cd {index_path} \\")
    print(f"&& bowtie2-build {index_genome_file} {index} \\")
    print(f"&& cd ..")               

def output_confirmation(output_path, output_file, r1, r2, offset=1):
    print(f"\n=== output location ===")
    print(output_path)
    print("=== list of outputs ===")
    for i in range(len(r1)):
        id_num = i + offset
        print("\t",
            f"{output_file}_{id_num}:", 
            f"R1 = {r1[i]} |",f"R2 = {r2[i]}")

    proceed = input("\nPROCEED? [Y/N]: ")
    if proceed.casefold() == "n":
        sys.exit("sorry")

def bowtie_sam(output_path, output_file, temp_path, index, r1, r2, offset=1):
    print("\n=== create .sam from bowtie ===\n")
    # sets output folders
    print(f"mkdir {output_path} \\")
    print(f"&& mkdir {temp_path} \\")

    # create bowtie thing inside input with name output_file_1.sam inside temp folder
    print(f"&& cd {input_path} \\")
    for i in range(len(r1)):
        id_num = i + offset
        print(
                f"&& bowtie2 -x ", 
                f"{index_path}/{index}", 
                f"-1 {r1[i]}", f"-2 {r2[i]}", 
                f"-S {temp_path}/{output_file}_{id_num}.sam \\"
            )
    print(f"&& ls \\")
    print("&& cd ..")

def samtools(output_path, output_file, temp_path, r1, offset=1):
    print("\n=== samtools ===\n")
    # work in temp path
    print(f"cd {temp_path} \\")
    # for every file in list
    for i in range(len(r1)):
        id_num = i + offset
        sam_output = f"{output_file}_{id_num}"
        # run samtools -> .bam
        print(
                f"&& samtools view", 
                f"-bS {sam_output}.sam > {sam_output}.bam \\"
            )
        # -> sorted.bam
        print(
                f"&& samtools sort", 
                f"{sam_output}.bam", 
                f"-o {output_path}/{sam_output}.sorted.bam \\"
            )
        # -> sorted.bam.bai
        print(
                f"&& samtools index", 
                f"-b {output_path}/{sam_output}.sorted.bam \\"
            )
    print(f"&& cd .. \\")
    print(f"&& ls")

def igvtools(output_path, output_file, index, r1, offset=1):
    print("\n=== igvtools ===\n")
    print(f"cd {output_path}")
    window_size = 1000
    for i in range(len(r1)):
        id_num = i + offset
        sam_output = f"{output_file}_{id_num}"
        print(
                f"&& igvtools count", 
                f"-w {window_size} -f mean",
                f"{sam_output}.sorted.bam", 
                f"{sam_output}.wig",
                f"{index_path}/{index}.fasta.fai \\"
            )
    print('&& for file in *.wig; do mv "$file" "${file%.wig}.csv"; done \\')
    print('&& ls \\')
    print("&& cd")

if __name__ == '__main__':
    main()

