# -*- coding:utf-8 -*-

from flask import Flask, request
from tulip import *
import math
import json
import csv


class GraphBuilder(object):
	'''
	This class builds a graph from the ANR project csv file
	'''
	def __init__(self):
		super(GraphBuilder, self).__init__()
		self.partner_hashmap = {}
		self.program_hashmap = {}
		self.graph = tlp.newGraph()

	def set_headers(self, header_line):
		self.project_headers = [header_line[i] for i in range(6)]
		self.programme_headers = [header_line[i] for i in range(6, 9)]
		for i in range(9, 13):
			self.project_headers.append(header_line[i])
		for i in range(14, 17):
			self.project_headers.append(header_line[i])
		self.partners_headers = [header_line[i] for i in range(17, 23)]

	def set_graph_properties(self):
		'''
		Sets graph properties based on header line
		storing external data onto node and edge properties
		set_headers need to be called first

		All properties are stored as string except one ('Montant')
		'''
		self.node_type = self.graph.getStringProperty('type')
		self.graph.getDoubleProperty('Montant')
		self.graphProperties = {}
		for h in self.partners_headers:
			self.graphProperties[h] = self.graph.getStringProperty(h)
		for h in self.project_headers:
			self.graphProperties[h] = self.graph.getStringProperty(h)
		for h in self.programme_headers:
			self.graphProperties[h] = self.graph.getStringProperty(h)

	def set_view_properties(self):
		'''
		Sets graph view properties (color, labels, etc.)
		'''
		label = self.graph.getStringProperty('viewLabel')
		color = self.graph.getColorProperty('viewColor')
		for n in self.graph.getNodes():
			if self.node_type[n] == 'project':
				label[n] = self.graph[self.project_headers[2]][n]
				color[n] = tlp.Color.Blue
			if self.node_type[n] == 'partner':
				label[n] = self.graph[self.partners_headers[2]][n]
				color[n] = tlp.Color.Red
			if self.node_type[n] == 'program':
				label[n] = self.graph[self.programme_headers[0]][n]
				color[n] = tlp.Color.Green

	def create_project(self, row):
		'''
		Creates project nodes
		'''
		project = self.graph.addNode()
		self.node_type[project] = 'project'
		for h in self.project_headers:
			self.graphProperties[h][project] = row[h].decode('utf-8')
		self.graph['Montant'][project] = float(row['Montant'])
		return project

	def create_and_link_partners(self, row, project):
		'''
		Creates partner nodes and links them to the project
		extracted from same row
		'''
		partner_properties\
			= map(lambda x: row[x].decode('utf-8').split(';'), self.partners_headers)
		partner_codes = partner_properties[4]
		for i, c in enumerate(partner_codes):
			if c not in self.partner_hashmap.keys():
				partner = self.graph.addNode()
				self.node_type[partner] = 'partner'
				for j, h in enumerate(self.partners_headers):
					self.graphProperties[h][partner] = partner_properties[j][i]
				self.partner_hashmap[c] = partner
			self.graph.addEdge(self.partner_hashmap[c], project)

	def create_and_link_program(self, row, project):
		'''
		Creates program node and links it to the project
		extracted from same row
		'''
		program_code = row[u'Code du programme']
		if not program_code in self.program_hashmap.keys():
			programme = self.graph.addNode()
			self.node_type[programme] = 'program'
			for h in self.programme_headers:
				self.graphProperties[h][programme] = row[h]
			self.program_hashmap[program_code] = programme
		self.graph.addEdge(self.program_hashmap[program_code], project)

	def parse(self):
		with open('ANR_projets.csv',u'rU') as csvfile:
			ANRreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
			self.set_headers(ANRreader.fieldnames)
			self.set_graph_properties()
			i = 0
			for row in ANRreader:
				project = self.create_project(row)
				self.create_and_link_partners(row, project)
				self.create_and_link_program(row, project)
				if i == 5:
					break
				i += 1

		self.set_view_properties()
		tlp.saveGraph(self.graph, '/Users/melancon/Documents/Enseignements/CMI ISI/CMI_ISI_M1_Visualisation/Flask_dessin_graphes/model/graph.tlp')

if __name__ == '__main__':

	gb = GraphBuilder()
	gb.parse()
