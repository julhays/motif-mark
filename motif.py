#!/usr/bin/env python

# Author: Jules Hays

# OOP - Motif Mark

import argparse

#Define classes
class Gene:
    '''This class represents a record in a FASTA file. It will
    create Motif object.'''
    def __init__(self, header, sequence):
        
        ## Data ##
        self.name = 
        self.sequence = 
        self.length = the_sex
        self.rev_comp = None
        
    ## Methods ##
    def parse_header(self):
        print("Meeeooowwwww")
    
    def rev_comp(self, thing):
        print(f'I love {thing}!')
    
    def parse_sequence(self, person):
        self.speak()
        self._owner = person

class Motif:
    '''This class represents a motif.
    It will interact with Human objects'''
    def __init__(self, the_name, the_color, the_sex):
        '''This is how a dog is made.'''
        
        ## Data ##
        self.name = the_name
        self.color = the_color
        self.sex = the_sex
        self._owner = None
        
    ## Methods ##
    def speak(self):
        print("Woof")
    
    def i_love(self, thing):
        print(f'I love {thing}!')
    
    def get_adopted(self, person):
        self.speak()
        self._owner = person


class Human:
    '''This class represents a human.
    It will interact with pets'''
    def __init__(self, the_name):
        '''This is how a dog is made.'''
        
        ## Data ##
        self.name = the_name
        self._pets = []
        
    ## Methods ##
    def adopt(self, pet):
        print("yay")
        pet.get_adopted(self)
        self._pets.append(pet)

    def feed_pet(self, pet):
        print("eat kibble")
        pet.i_love("kibble")



chicken = Cat("chicken", "brown", "female")
nugget = Dog("nugget", "golden", "male")
mcdonald = Human("Donald")

#commands
mcdonald.adopt(chicken)
mcdonald.adopt(nugget)
mcdonald.feed_pet(chicken)













# ADD ARGPARSE
#define arg inputs, defaults are for the actual files we are demultiplexing for this assignment
#making the files for this specific assignment the default for ease of use
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Establish criteria for k-merizing fastq data")
    parser.add_argument("-r1", "--R1", help="Specify the R1 file", type=str, default ='/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz')
    parser.add_argument("-r2", "--R2", help="Specify the R2 file", type=str, default ='/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz')
    parser.add_argument("-r3", "--R3", help="Specify the R3 file", type=str, default ='/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz')
    parser.add_argument("-r4", "--R4", help="Specify the R4 file", type=str, default ='/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz')
    parser.add_argument("-i", "--index", help="Specify the index file", type=str, default ='/projects/bgmp/shared/2017_sequencing/indexes.txt')
    return parser.parse_args()

#call get_args to create args object
args = get_args()

#set path variables and assign them to the user inputted values at the function call
r1_path: str = args.R1
r2_path: str = args.R2
r3_path: str = args.R3
r4_path: str = args.R4
index_file: str = args.index

#hard code paths for test files
# index_file: str = '/projects/bgmp/shared/2017_sequencing/indexes.txt'

# r1_path: str = '/projects/bgmp/jkhay/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/test_R1.fastq'
# r2_path: str = '/projects/bgmp/jkhay/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/test_R2.fastq'
# r3_path: str = '/projects/bgmp/jkhay/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/test_R3.fastq'
# r4_path: str = '/projects/bgmp/jkhay/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/test_R4.fastq'