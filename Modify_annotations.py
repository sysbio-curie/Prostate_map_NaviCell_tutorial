#!/usr/bin/env python
#coding: utf-8

import argparse

##########################
### HELP Section START ###
##########################

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
					argparse.ArgumentDefaultsHelpFormatter): pass

parser = argparse.ArgumentParser(prog='Modify_annotations',
								formatter_class=CustomFormatter,
								description=
"""

#----------------------------------------#
# Modify_annotations                     #
#                                        #
# Author  : SOMPAIRAC Nicolas            #
# Contact : nicolas.sompairac@gmail.com  #
# Version : (March 2018); Institut Curie #
#----------------------------------------#

This script allows to modify annotation links in a CellDesigner's XML format 
map taking as input a table of correspondance between node names and their IDs 
used in wanted databases. As a result, it will modify the references of the
nodes and allow to create a link to these databases clickable on NaviCell.

""")

file_locations = parser.add_argument_group('Location of different files')


file_locations.add_argument('--corresp', metavar='Corresp_table', type=str,
							default=None,
							help=("Location of the table with corresponding "
								"node names and their correct ID. First column "
								"contains Node names and the Second column "
								"contains their IDs."))
file_locations.add_argument('--origin-file', metavar='Original_map', type=str,
							default=None,
							help=("Location and name of the original map file "
								"in CellDesigner XML format."))
file_locations.add_argument('--result-file', metavar='Res_outfile', type=str,
							default=None,
							help=("Location and name of the resulting map file "
								"in CellDesigner XML format."))


options = parser.add_argument_group('Options to use')

options.add_argument('--link-type', metavar='Link_type', type=str,
					default='HUGO',
					help=("Type of link to convert to. Can be the following: "
						"HUGO, HGNC, ENTREZ, UNIPROT, PUBCHEM, KEGGCOMPOUND, "
						"CAS, CHEBI, KEGGDRUG, REACTOME, KEGG, GENECARDS, "
						"ATLASONC, ATONC."))

args = parser.parse_args()


#########################
### HELP Section STOP ###
#########################


def Read_correspondance_table(filename):

	corresp_dict = {}

	with open(filename, 'rU') as infile:

		for line in infile:

			tmp = line.split()

			corresp_dict[tmp[0]] = tmp[1]

	return corresp_dict


def Modify_annotations(filename_in, filename_out, corresp_dict, link):

	with open(filename_in, 'rU') as infile:

		infile_read = infile.readlines()

		with open(filename_out, 'w') as outfile:

			for line in infile_read:

				if "HUGO:" in line:

					if line[5:-1] in corresp_dict:

						outfile.write(link+":"+corresp_dict[line[5:-1]]+"\n")
					else:
						outfile.write(line)
				else:

					outfile.write(line)

	return


print "\n"
############
### MAIN ###
############

Corresp_dict = Read_correspondance_table(args.corresp)

Modify_annotations(args.origin_file, args.result_file, Corresp_dict, args.link_type)

print "\n"