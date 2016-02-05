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

from music21 import converter
from rodan.jobs.base import RodanTask
from vis.analyzers.indexers.fermata import FermataIndexer

import logging
logger = logging.getLogger('rodan')

class VRFermataIndexer(RodanTask):

    name = 'Fermata Indexer'
    author = "Ryan Bannon"
    description = "Generate indices for all fermatas in a given piece of music."
    settings = {}

    enabled = True
    category = "Indexer"
    interactive = False

    input_port_types = [{
        'name': 'MusicXML',
        'resource_types': ['application/x-musicxml+xml'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Fermata Indexer Result',
        'resource_types': ['application/x-vis_fermata_pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        infile = inputs['MusicXML'][0]['resource_path']
        outfile = outputs['Fermata Indexer Result'][0]['resource_path']
        score = [converter.parse(infile, format='musicxml')][0]
        indexer = FermataIndexer(score)
        results = indexer.run()
        results.to_csv(outfile)

        return True
