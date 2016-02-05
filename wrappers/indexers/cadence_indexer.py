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

class VRCadenceIndexer(RodanTask):

    name = 'vis-rodan.indexer.VF_cadence_indexer'
    author = "Ryan Bannon"
    description = "Index cadences"
    settings = {}

    enabled = True
    category = "Indexer"
    interactive = False

    input_port_types = [{
        'name': 'Cadence Indexer - fermata indices (Pandas DataFrame csv)',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    },
    {
        'name': 'Cadence Indexer - figured bass (Pandas DataFrame csv)',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Cadence Indexer - Pandas DataFrame csv',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        # Get files.
        fermata_indices_file = inputs['Cadence Indexer - fermata indices (Pandas DataFrame csv)'][0]['resource_path']
        infile = inputs['Cadence Indexer - figured bass (Pandas DataFrame csv)'][0]['resource_path']
        outfile = outputs['Cadence Indexer - Pandas DataFrame csv'][0]['resource_path']

        # De-serialize the DataFrames.
        fermata_indices = DataFrame.from_csv(fermata_indices_file, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        figured_bass = DataFrame.from_csv(infile, header = [0, 1]) # We know the first two rows constitute a MultiIndex

        # Added fermatas to DataFrame.
        cadence_marker = fermata_indices.apply(lambda x: 'Fermata' in x.values, axis = 1)
        pieces = {'Basso seguente': figured_bass['Basso seguente']['3'],
                  'Figured bass': figured_bass['Figured bass'].T.loc[['[0,3 1,3 2,3] (3)']].T,
                  'Cadence': cadence_marker}
        figured_bass = concat(pieces, axis = 1)

        # Find cadences.
        marker_column = 'Cadence'
        cadence_size = 4
        indices = figured_bass[figured_bass[marker_column][0] == True].index
        cadences = []
        for index in indices:
            cadenceEndLocation = figured_bass.index.get_loc(index)
            harmonies = []
            for cadenceStep in range(cadenceEndLocation - cadence_size + 1, cadenceEndLocation + 1):
                harmonies.append(figured_bass.iloc[cadenceStep])
            cadence = DataFrame(harmonies)
            cadences.append(cadence)  

        # Output.   
        self.write_cadences_to_file(cadences, outfile)

        return True

    def write_cadences_to_file(self, cadences, write_filepath):

        write_file = open(write_filepath, 'a+')
        #write_file.write('Index, Basso seguente, Intervals' + '\n')
        for cadence in cadences:
            serialized_cadence = ""
            records = cadence.to_records()
            for record in records:
                serialized_cadence += str(record[1]) + " "
                serialized_cadence += str(record[3]) + " "
            logger.error(serialized_cadence)
            write_file.write(serialized_cadence + '\n')