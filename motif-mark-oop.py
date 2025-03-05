#!/usr/bin/env python

# Author: Jules Hays

# OOP - Motif Mark

#load necessary packages
import argparse
import re
import cairo
import random

#Define classes
class Gene:
    '''This class represents a record in a FASTA file. It will create Motif and Exon objects.'''
    def __init__(self, header, sequence, motif_list):
        
        ## Data ##
        self.header = header #stores fasta record header
        self.title = self.parse_title()
        self.sequence = sequence #sequence
        self.upper_seq = sequence.upper() #all caps version of sequence
        self.length = len(sequence) #sequence length
        self.motifs = self.find_motifs(motif_list) #list of associated motif objects
        self.exons = self.find_exons() #list of associated exon objects
        
    ## Methods ##
    def parse_title(self):
        gene_name = re.findall('>([A-Z0-9]+)', self.header)[0]
        chromosome = re.findall('chr([0-9]+)', self.header)[0]
        position = re.findall(':([0-9]+-[0-9]+)', self.header)[0]

        new_title = f'Gene: {gene_name}, Chromosome: {chromosome}, Nucleotide Position: {position}'
        return new_title

    def find_motifs(self, motif_list):
        '''Finds all instances of each motif in the motif list file and creates a Motif object for each. Stores in 
        motifs list for the associated Gene object.'''
        #create list to store motif objects
        motif_objects = []

        #go through each motif in inputted .txt list
        for motif in motif_list:

            #convert the motif into regex searchable string
            regex_motif = self.convert_motif(motif)

            #search for matches in the sequence
            for match in re.finditer(regex_motif, self.upper_seq):

                #initialize a new motif object for each match
                motif_object = Motif(motif, match.start(), len(match.group(1)))

                #append object to list of objects
                motif_objects.append(motif_object)
        
        return motif_objects #returns list of associated motif objects
                

    def find_exons(self):
        '''Finds all instances of exons in the gene sequence file and creates an Exon object for each. Stores in 
        exon list for the associated Gene object.'''
        #create list to store exon objects
        exon_objects = []

        #regex for all caps areas in the string
        for match in re.finditer("[A-Z]+", self.sequence):

            #initialize a new exon object for each match
            exon_object = Exon(match.start(), len(match.group()))

            #append object to list of objects
            exon_objects.append(exon_object)

        return exon_objects #returns list of associated motif objects
    
    def convert_motif(self, motif):
        '''Converts a motif from the motif list into the regex searchable version, accounting for Y's being any pyrimadine.
        Inputs a single motif sequence, returns the regex searchable string of that motif.'''

        #define a dictionary that converts each "wildcard" character into a regex searchable form
        regex_dict = {'A': 'A', 
                    'T': '[T|U]',
                    'C': 'C',
                    'G': 'G',
                    'U': '[T|U]',
                    'Y': '[C|T|U]',
                    'R': '[A|G]',
                    'W': '[A|T|U]',
                    'S': '[C|G]',
                    'M': '[C|A]',
                    'K': '[G|T|U]',
                    'B': '[C|T|U|G]',
                    'D': '[A|T|U|G]',
                    'H': '[A|T|U|C]',
                    'V': '[A|G|C]',
                    'N': '[A|T|U|C|G]',
                    }

        #make the motif uppercase
        motif = motif.upper()

        #make an empty string to build the regex searchable string
        regex_motif = ""

        #go through each character in the motif
        for char in motif:

            #add regex searchable form to regex string
            regex_motif += regex_dict[char]

        #returns the regex searchable version of the string
        return "(?=(" + regex_motif + "))" #?= allows for characters to not be consumed to overlaps can be accounted for


class Motif:
    '''This class represents a motif.'''
    def __init__(self, motif_seq, start_pos, length):
        
        ## Data ##
        self.seq = motif_seq
        self.start = start_pos
        self.length = length
        self.color = color_map[motif_seq]


class Exon:
    '''This class represents a exon. Introns are just the regions that are not exons.'''
    def __init__(self, start_pos, length):
        
        ## Data ##
        self.start = start_pos
        self.length = length      


##### MAIN SCRIPT BODY #####
#argparse
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a visual of motifs on gene sequences")
    parser.add_argument("-f", "--fasta", help="Specify the fasta file", type=str, required = True)
    parser.add_argument("-m", "--motifs", help="Specify the text fle with the list of motifs", type=str, required = True)
    return parser.parse_args()

#call get_args to create args object
args = get_args()

#set path variables and assign them to the user inputted values at the function call
fasta_file: str = args.fasta
motif_file: str = args.motifs

#get file path prefix for output name
output = fasta_file.split('.')[0]


#read in motifs and append to a list
motif_list = []

with open(motif_file, "rt") as fh:
    for line in fh:
        line = line.strip('\n')
        motif_list.append(line)


#make color map for motifs
color_map = {}

#define 5 colors since we will get max 5 motifs
colors = [(106, 76, 147), #purple
          (25, 130, 196), #blue
          (138, 201, 38), #green
          (255, 89, 94), #pink  
          (255, 202, 58), #yellow
         ]

#divide everything by 255 because pycairo colors are RGB on a scale of 0 to 1
for i in range(len(colors)):
    r, g, b = colors[i]
    colors[i] = r/255, g/255, b/255     

#make a dictionary of motifs and corresponding rgb color
for i, motif in enumerate(motif_list):
    color_map[motif] = colors[i]


#read in fasta records and parse to make gene objects
gene_list = [] #list to store gene objects
header = ""
sequence = ""
with open(fasta_file, "rt") as fh:
    line1 = True #boolean to indicate first line in the file
    for line in fh:
        line = line.strip('\n')

        #handle the first record
        if line1:
            header = line
            line1 = False
        
        #if encounter a new fasta record
        elif line[0] == '>':
            #make object out of previous record and append to list
            new_gene = Gene(header, sequence, motif_list)
            gene_list.append(new_gene)

            #reset variables
            header = ""
            sequence = ""

            #continue parsing
            header = line
        
        #append sequence information
        else:
            sequence += line

#make object out of last record and append to list
new_gene = Gene(header, sequence, motif_list)
gene_list.append(new_gene)


# Create the drawing out of gene objects

#count the number of genes and longest gene to establish drawing size
longest = 0
count = 0

for gene in gene_list:
    count += 1
    if gene.length > longest:
        longest = gene.length

#set space between each record as well as space between the sequence ends and the edge of the drawing
space_between = 150
buffer = 200

#set drawing size, add an additional 200 at the end for the legend
width, height = longest + buffer, count * space_between + 200

#create the coordinates to display graphic
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
context = cairo.Context(surface)

#make a white background
context.set_source_rgb(1, 1, 1)
context.rectangle(0,0,width+10,height+10)        #(x0,y0,x1,y1)
context.fill()

#establish where sequence drawings will start
seq_start_x = buffer/2
curr_y = space_between/2 + 50

#parse through each gene to draw
for gene in gene_list:
    
    #plot gene sequence with proportional length
    context.set_source_rgb(0, 0, 0) #set color black
    context.set_line_width(4)
    context.move_to(seq_start_x,curr_y)
    context.line_to(seq_start_x+gene.length,curr_y)
    context.stroke()

    #plot sequence name over the sequence
    context.set_font_size(22)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL) 
    context.move_to(seq_start_x, curr_y-55) 
    context.show_text(gene.title) 

    #plot the exons as thicker black regions overlaid on the sequence, introns are just the thinner regions
    for exon in gene.exons:

        #extract necessary info from object
        exon_start = exon.start
        exon_length = exon.length

        #draw
        context.set_line_width(20)
        context.move_to(seq_start_x+exon_start,curr_y)       
        context.line_to(seq_start_x+exon_start+exon_length,curr_y)
        context.stroke()

    #plot the motifs as colored regions overlaid on the sequences
    for motif in gene.motifs:
        red, green, blue = motif.color #set color based on which motif in the list it is
        context.set_source_rgba(red, green, blue, .7) #.7 makes it translucent so you can see overlapping motifs
        context.set_line_width(40)

        #extract necessary info
        motif_start = motif.start
        motif_length = motif.length

        #draw
        stagger = random.randint(-20, 21)
        context.move_to(seq_start_x+motif_start, curr_y + stagger)       
        context.line_to(seq_start_x+motif_start+motif_length, curr_y + stagger)
        context.stroke()
    
    #increment y position by the set space between each sequence drawing
    curr_y += space_between


#make legend for the drawing to show what colors are what motifs and exons

#add legend title
context.set_source_rgb(0, 0, 0)
context.set_font_size(22)
context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL) 
context.move_to(seq_start_x, curr_y-50) 
context.show_text("Legend")

#establish start x and section increments based on how many motifs there are
section = width/(len(color_map)+2)
legend_start = seq_start_x

#draw black box for the exon label key
context.set_line_width(40)
context.move_to(legend_start,curr_y)
context.line_to(legend_start+20,curr_y)
context.stroke()

#write exon label
context.set_font_size(18)
context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL) 
context.move_to(legend_start+25, curr_y+5) 
context.show_text("Exon") 

#increment x position
legend_start += section

#loop through each motif to make a legend entry
for motif in color_map:

    #make color block
    red, green, blue = color_map[motif]
    context.set_source_rgba(red, green, blue, .7)
    context.set_line_width(40)
    context.move_to(legend_start,curr_y)
    context.line_to(legend_start+20,curr_y)
    context.stroke()
    
    #add motif label next to color block key
    context.set_source_rgb(0, 0, 0)
    context.set_font_size(18)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL) 
    context.move_to(legend_start+25, curr_y+6) 
    context.show_text(motif) 
    
    #increment x position
    legend_start += section

#write out drawing
surface.write_to_png(f'{output}.png', )
