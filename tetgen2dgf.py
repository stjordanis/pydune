#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,math,os,time

## global defines

# about the correctness of the triangle files
triangle_nodefile_incorrect = 0
triangle_polyfile_incorrect = 0
triangle_elefile_incorrect = 0

def assert_line(line):
	for el in line:
		assert el >= -1,'line has element with negative index: %s'%' '.join(line)

# write the dgf header into the dgf file
def write_dgf_header( file ) :
	file.write( 'DGF\t\t\t\t\t\t%s %s, generated by %s on %s \n' %( '%', file.name, sys.argv[0],time.strftime('%Y/%m/%d %H:%M:%S') ) )
	#file.write( '% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n' )
	#file.write( '%s %s\n' %( '%', file.name ) )
	#file.write( '%s written by triangle2dgf.py on %s\n' %( '%', time.strftime('%Y/%m/%d %H:%M:%S') ) )
	#file.write( '% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n' )

# write vertices to dgf file
def write_vertices( file, node_file_name ) :
	print 'writing vertices to %s...' %( file.name ),
	file.write( 'VERTEX\t\t\t\t\t% the vertices of the grid\n' )
	with open( node_file_name, 'r' ) as node_file:
		vertex_number = 0
		for line in node_file.readlines():
			if vertex_number != 0:
				if line.startswith( '#' ):
					continue
				line = [ float(el) for el in line.split() ]
				assert len(line) > 3
				file.write( '%f\t%f\t%f\t%% vertex %i\n' %( line[1], line[2], line[3], line[0] - 1 ) )
			vertex_number += 1
		file.write( '#\n' )

# write simplices to dgf file
def write_simplices( file, ele_file_name ) :
	print 'writing simplices to %s...' %( file.name ),
	file.write( 'SIMPLEX\t\t\t\t\t% the simplices of the grid\n' )
	with open( ele_file_name, 'r' ) as ele_file:
		vertex_number = 0
		for line in ele_file.readlines():
			if vertex_number != 0:
				if line.startswith( '#' ):
					continue
				offset = -1
				line = [ int(el) + offset for el in line.split() ]
				assert len(line) > 4 , line
				assert_line(line)
				file.write( '%i\t%i\t%i\t%i\t%% simplex %i\n' %( line[1] , line[2], line[3], line[4], line[0]))
			vertex_number += 1
	file.write( '#\n' )

# write boundary segments to dgf file
def write_boundary_segments( file, face_file_name ) :
	print 'writing boundary segments to %s...' %( file.name ),
	file.write( 'BOUNDARYSEGMENTS\t\t% the boundary segments of the grid\n' )
	with open( face_file_name, 'r' ) as face_file:
		vertex_number = 0
		for line in face_file.readlines():
			if vertex_number != 0:
				if line.startswith( '#' ):
					continue
				line = [ int(el) for el in line.split() ]
				assert len(line) > 4 , line
				file.write( '%i\t%i\t%i\t%i\t%% segment %i\n' %( line[4], line[1] - 1 , line[ 2 ] - 1, line[3] - 1, line[0] - 1 ))
			vertex_number += 1
	file.write( '#\n' )
	file.write( '#\n' )
	file.write( 'BOUNDARYDOMAIN\n' )
	file.write( 'default 1\n' )
	file.write( '#\n')

## done with function definitions


## main
filename_prefix = sys.argv[ 1 ]
dgf_filename = '%s.dgf' %( filename_prefix )
nodefile_filename = filename_prefix + '.node'
facefile_filename = filename_prefix + '.face'
elefile_filename = filename_prefix + '.ele'

with open( dgf_filename, 'w' ) as dgf_file:
	write_dgf_header( dgf_file )
	write_vertices( dgf_file, nodefile_filename )
	write_simplices( dgf_file, elefile_filename )
	write_boundary_segments( dgf_file, facefile_filename )
