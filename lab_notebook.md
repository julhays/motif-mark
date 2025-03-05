# BI625 Motif Mark - Lab Notebook
Jules Hays
## Due: 3/6/25

Python version: 3.12.9

Environments used: motif (pycairo 1.27.0)

---

### 2/25/25
Goal: Create a python script using object oriented code that will input a fasta file and a list of motifs, and output a graphic of each sequence with the motif positions labeled on the sequence.

I logged into Talapas and cloned the motif-mark repo in new directory for this assignment, located at
```
/projects/bgmp/jkhay/bioinfo/Bi625/motif-mark
```

For this assignment, I need pycairo. I previously made a conda environment called ```motif``` with pycairo so I am going to use this conda environment. To install pycairo into the environment I used the following command: ```mamba install pycairo```.

I made a script called ```motif-mark-oop.py``` to write my code for this assignment. I will begin the script.

### 3/3/25
I have created a first draft of the script for this assignment. I need to go through the assignment and make sure it meets all the criteria. I started by making rough outlines of what classes I wanted. Then, I began filling in the details and individual functions for each class. Then, I wrote my code body where I handled reading in the files and creating the objects. Finally, after all my objects were created I wrote up the cairo code to output the drawing.

I will test my script with the following command:
```
./motif-mark-oop.py -f Figure_1.fasta -m Fig_1_motifs.txt
```
The script takes 0.06 seconds to run.

I am now going to go through the assignment directions to ensure I meet the requirements. I have documented further changes below:
* I changed the name of my python script from ```motifs.py``` to ```motif-mark-oop.py```.
* I changed the name of the output .png to match the prefix of the fasta input.
* I adjusted my motif regex dictionary to account for all ambiguous nucleotides, not just Y's

### 3/4/25

I am updating my readme to be more detailed.

Now, I will attempt the bonuses.

I added a random stagger of motifs along the y-axis to better see overlaps. I also parsed the header of each fasta record to make a better figure title.


Here is the output for the sample files provided in the assignment:
![alt text](Figure_1.png)


