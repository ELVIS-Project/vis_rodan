#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           vis-rodan
# Program Description:    Job wrappers that allows vis-framework to work in Rodan.
#
# Filename:               vis-rodan/indexers/dissonance_indexer.py
# Purpose:                Wrapper for Dissonance Indexer.
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

from pandas import DataFrame
from rodan.jobs.base import RodanTask
from vis.analyzers.indexers.dissonance import DissonanceIndexer

import logging
logger = logging.getLogger('rodan')

class VRDissonanceIndexer(RodanTask):

    name = 'Dissonance Indexer'
    author = "Ryan Bannon"
    description = "Identifies dissonances for the given intervals."
    settings = {}

    enabled = True
    category = "Indexer"
    interactive = False

    input_port_types = [{
        'name': 'Note Beat Strength Indexer Result',
        'resource_types': ['application/x-vis_nbs_pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    },
    {
        'name': 'Duration Indexer Result',
        'resource_types': ['application/x-vis_duration_pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    },
    {
        'name': 'Horizontal Interval Indexer Result',
        'resource_types': ['application/x-vis_horizontal_pandas_series+csv'],
        'minimum': 1,
        'maximum': 1
    },
    {
        'name': 'Vertical Interval Indexer Result',
        'resource_types': ['application/x-vis_vertical_pandas_series+csv'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Dissonance Indexer Result',
        'resource_types': ['application/x-vis_dissonance_pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        infileBeat = inputs['Note Beat Strength Indexer Result'][0]['resource_path']
        infileDuration = inputs['Duration Indexer Result'][0]['resource_path']
        infileHorizontal = inputs['Horizontal Interval Indexer Result'][0]['resource_path']
        infileVertical = inputs['Vertical Interval Indexer Result'][0]['resource_path']
        outfile = outputs['Dissonance Indexer Result'][0]['resource_path']
        beat = DataFrame.from_csv(infileBeat, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        duration = DataFrame.from_csv(infileDuration, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        horizontal = DataFrame.from_csv(infileHorizontal, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        vertical = DataFrame.from_csv(infileVertical, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        indexer = DissonanceIndexer([beat, duration, horizontal, vertical])
        results = indexer.run()
        results.to_csv(outfile)

        return True
