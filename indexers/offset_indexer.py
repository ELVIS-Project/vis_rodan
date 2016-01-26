#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           vis-rodan
# Program Description:    Job wrappers that allows vis-framework to work in Rodan.
#
# Filename:               vis-rodan/indexers/noterest_indexer.py
# Purpose:                Wrapper for NoteRest Indexer.
#
# Copyright (C) 2015 DDMAL
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------
import numpy
from pandas import concat, DataFrame
from rodan.jobs.base import RodanTask

import logging
logger = logging.getLogger('rodan')

class VROffsetIndexer(RodanTask):

	name = 'Offset Indexer'
	author = 'Marina Borsodi-Benson'
	description = 'Filters by offset'
	settings = {
		'title': 'Offset Indexer Settings',
		'type': 'object',
		'properties': {
			'Quarternote length': {
				'type': 'float',
				'default': 1.0,
				'minimum': 0.001,
				'description': 'The quarternote length duration between observations desired in the output.'
			},
			'Forward Fill': {
				'type': 'boolean',
				'default': True,
				'description': 'Forward fill fills in the missing indices with the previous value. This is useful for vertical intervals, but not for horizontal.'
			}
		}
	}

	enabled = True
	category = 'Indexer'
	interactive = False

	input_port_types = [{
		'name': 'NoteRest Indexer Result',
		'resource_types': ['application/x-vis_noterest_pandas_series+csv'],
		'minimum': 1,
		'maximum': 1,
	}]
	output_port_types = [{
		'name': 'Offset Indexer Result',
		'resource_types': ['application/x-vis_noterest_pandas_series+csv'],
		'minimum': 1,
		'maximum': 1
	}]

	def run_my_task(self, inputs, settings, outputs):

		infile = inputs['NoteRest Indexer Result'][0]['resource_path']
		outfile = outputs['Offset Indexer Result'][0]['resource_path']

		wrapper_settings = dict([(k, settings[k]) for k in ('Quarternote length', 'Method')])
		execution_settings = dict()
		execution_settings['quarterLength'] = wrapper_settings['Quarternote length']
		if wrapper_settings['Forward Fill'] == True:
			execution_settings['method'] = 'ffill'
		else:
			execution_settings['method'] = 'None'
		execution_settings['mp'] = False

		noterest = DataFrame.from_csv(noterest_file, header = [0, 1])
		offset_indexed = OffsetIndexer(noterest, execution_settings).run()
		offset_indexed.to_csv(outfile)

		return True