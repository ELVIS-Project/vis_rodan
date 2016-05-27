#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           vis-rodan
# Program Description:    Job wrappers that allows vis-framework to work in Rodan.
#
# Filename:               vis-rodan/indexers/ngram_indexer.py
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
from pandas import concat, DataFrame
from rodan.jobs.base import RodanTask
from vis.analyzers.indexers.ngram import NGramIndexer

import logging
logger = logging.getLogger('rodan')

class VRNGramIntervalIndexer(RodanTask):

    name = 'N-Gram Indexer'
    author = "Ryan Bannon"
    description = "Creates N-Grams for given vertical and horizontal indices for a piece of music."
    settings = {
        'title': 'N-Gram Indexer Settings',
        'type': 'object',
        'properties': {
            'Horizontal voice': {
                'description': 'If you know which voice will act as the horizontal voice, choose "integer" from above then input the voice number. Voice numbering starts at 0 for the top voice, 1 for the voice below that, and so on.<br><br>You can also choose "string" to select "top" or "bottom".',
                'oneOf': [
                    {
                        'enum': [ 'bottom'],
                        'default': 'bottom',
                        'type': 'string'
                    },
                    {
                        'type': 'integer',
                        'default': 1,
                        'minimum': 1
                    }
                ],
                'default': 'bottom'
            },
            'N-Gram size': {
                'description': 'Set the desired N-Gram size.',
                'type': 'integer',
                'minimum': 1,
                'default': 2
            }
        }
    }

    enabled = True
    category = "VIS - Indexer"
    interactive = False

    input_port_types = [{
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
        'name': 'N-Gram Indexer Result',
        'resource_types': ['application/x-vis_ngram_pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        # Get files
        horizontal_intervals_file = inputs['Horizontal Interval Indexer Result'][0]['resource_path']
        vertical_intervals_file = inputs['Vertical Interval Indexer Result'][0]['resource_path']
        outfile = outputs['N-Gram Indexer Result'][0]['resource_path']

        # De-serialize the DataFrames.
        horizontal_intervals = DataFrame.from_csv(horizontal_intervals_file, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        vertical_intervals = DataFrame.from_csv(vertical_intervals_file, header = [0, 1]) # We know the first two rows constitute a MultiIndex

        # Set execution settings.
        voice_count = len(horizontal_intervals.columns)
        horizontal_voice = voice_count - 1
        wrapper_settings = dict( [(k, settings[k]) for k in ('Horizontal voice', 'N-Gram size')] )
        execution_settings = dict()
        if wrapper_settings['Horizontal voice'] == 'top':
            horizontal_voice = 0
        elif wrapper_settings['Horizontal voice'] != 'bottom':
            horizontal_voice = wrapper_settings['Horizontal voice']
        execution_settings['horizontal'] = [('interval.HorizontalIntervalIndexer', str(horizontal_voice))]
        execution_settings['n'] = wrapper_settings['N-Gram size']
        execution_settings['mp'] = False

        # Get all possible intervals
        execution_settings['vertical'] = []
        suffix = ',' + str(horizontal_voice)
        for voice in xrange(horizontal_voice):
            pair = str(voice) + suffix
            execution_settings['vertical'].append(('interval.IntervalIndexer', pair))

        # Index.
        all_intervals = concat([horizontal_intervals, vertical_intervals], axis=1)
        ngrams = NGramIndexer(all_intervals, execution_settings).run()

        # Write results.
        ngrams.to_csv(outfile)

        return True
