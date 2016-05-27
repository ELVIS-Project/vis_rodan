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
from pandas import concat, DataFrame
from rodan.jobs.base import RodanTask
from vis.analyzers.indexers.ngram import NGramIndexer

import logging
logger = logging.getLogger('rodan')

class VRFiguredBassIndexer(RodanTask):

    name = 'Figured Bass Indexer'
    author = "Ryan Bannon"
    description = "Creates figured bass N-Grams. Please note that this indexer is not currently in the vis-framework as it is simply an N-Gram indexing job that places the horizontal voice in its own column."
    settings = {}

    enabled = True
    category = "VIS - Indexer"
    interactive = False

    input_port_types = [
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
        'name': 'Figured Bass Indexer Result',
        'resource_types': ['application/x-vis_figuredbass_pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        # Get files
        horizontal_intervals_file = inputs['Horizontal Interval Indexer Result'][0]['resource_path']
        vertical_intervals_file = inputs['Vertical Interval Indexer Result'][0]['resource_path']
        outfile = outputs['Figured Bass Indexer Result'][0]['resource_path']

        # De-serialize the DataFrames.
        horizontal_intervals = DataFrame.from_csv(horizontal_intervals_file, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        vertical_intervals = DataFrame.from_csv(vertical_intervals_file, header = [0, 1]) # We know the first two rows constitute a MultiIndex

        # Get the horizontal voice if not provided.
        voice_count = len(horizontal_intervals.columns)
        horizontal_voice = voice_count - 1
        settings['horizontal'] = [('interval.HorizontalIntervalIndexer', str(horizontal_voice))]

        # Get all possible pairs
        settings['vertical'] = []
        suffix = ',' + str(horizontal_voice)
        index_pairs = ''
        for voice in xrange(horizontal_voice):
            pair = str(voice) + suffix
            settings['vertical'].append(('interval.IntervalIndexer', pair))
            if index_pairs == '':
                index_pairs += '[' + pair
            else:
                index_pairs += ' ' + pair
        index_pairs += '] (' + str(horizontal_voice) + ')'

        # We also need a default for 'n'.
        settings['n'] = 1

        # Turn off multiprocessing.
        settings['mp'] = False

        # Index.
        all_intervals = concat([horizontal_intervals, vertical_intervals], axis=1)
        ngrams = NGramIndexer(all_intervals, settings).run()
        pieces = {'Figured bass': ngrams['ngram.NGramIndexer'].T.loc[[index_pairs]].T,
                  'Basso seguente': horizontal_intervals['interval.HorizontalIntervalIndexer'][str(horizontal_voice)]}
        result = concat(pieces, axis = 1)

        # Write results.
        result.to_csv(outfile)

        return True
