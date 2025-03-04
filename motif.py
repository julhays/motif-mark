#!/usr/bin/env python

# Author: Jules Hays

# OOP - Motif Mark

#load necessary packages
import argparse
import re
import cairo

#Define classes
class Gene:
    '''This class represents a record in a FASTA file. It will create Motif and Exon objects.'''
    def __init__(self, header, sequence):
        
        ## Data ##
        self.name = header
        self.sequence = sequence
        self.upper_seq = sequence.upper()
        self.length = len(sequence)
        self.motifs = []
        self.exons = []
        
    ## Methods ##
    def find_motifs(self, motif_list):
        '''Finds all instances of each motif in the motif list file and creates a Motif object for each. Stores in 
        motifs list for the associated Gene object.'''
        for motif in motif_list:
            regex_motif = convert_motif(motif)
            for match in re.finditer(regex_motif, self.upper_seq):
                motif_object = Motif(motif, match.start(), len(match.group(1)))
                self.motifs.append(motif_object)
                
    def find_exons(self):
        '''Finds all instances of exons in the gene sequence file and creates an Exon object for each. Stores in 
        exon list for the associated Gene object.'''
        for match in re.finditer("[A-Z]+", self.sequence):
            exon_object = Exon(match.start(), len(match.group()))
            self.exons.append(exon_object)


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


#Define necessary functions
def convert_motif(motif):
    '''Converts a motif from the motif list into the regex searchable version, accounting for Y's being any pyrimadine.
    Inputs a single motif sequence, returns the regex searchable string of that motif.'''
    regex_dict = {'A': 'A', 
                  'T': 'T',
                  'C': 'C',
                  'G': 'G',
                  'U': 'T',
                  'Y': '[C|T|U]',
                 }
    motif = motif.upper()
    regex_motif = ""
    for char in motif:
        regex_motif += regex_dict[char]
        
    return "(?=(" + regex_motif + "))"


# MAIN SCRIPT BODY
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
            new_gene = Gene(header, sequence)
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
new_gene = Gene(header, sequence)
gene_list.append(new_gene)

#loop through each gene object to make corresponding motif and exon objects
for record in gene_list:
    record.find_motifs(motif_list)
    record.find_exons()



# Create the drawing

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
    context.move_to(seq_start_x, curr_y-50) 
    context.show_text(gene.name) 

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
        context.set_source_rgba(red, green, blue, .6) #.6 makes it translucent so you can see overlapping motifs
        context.set_line_width(40)

        #extract necessary info
        motif_start = motif.start
        motif_length = motif.length

        #draw
        context.move_to(seq_start_x+motif_start,curr_y)       
        context.line_to(seq_start_x+motif_start+motif_length,curr_y)
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
section = width/(len(color_map)+3) #+3 was so the final motif didn't run over the border
legend_start = seq_start_x

#draw black box for the exon label key
context.set_line_width(40)
context.move_to(legend_start,curr_y)
context.line_to(legend_start+40,curr_y)
context.stroke()

#write exon label
context.set_font_size(20)
context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL) 
context.move_to(legend_start+45, curr_y+5) 
context.show_text("Exon") 

#increment x position
legend_start += section

#loop through each motif to make a legend entry
for motif in color_map:

    #make color block
    red, green, blue = color_map[motif]
    context.set_source_rgba(red, green, blue, .6)
    context.set_line_width(40)
    context.move_to(legend_start,curr_y)
    context.line_to(legend_start+40,curr_y)
    context.stroke()
    
    #add motif label next to color block key
    context.set_source_rgb(0, 0, 0)
    context.set_font_size(20)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL) 
    context.move_to(legend_start+46, curr_y+6) 
    context.show_text(motif) 
    
    #increment x position
    legend_start += section

#write out drawing
surface.write_to_png("motif_drawing.png", )