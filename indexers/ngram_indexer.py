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

class VRHorizontalIntervalIndexer(RodanTask):

    DEFAULT_NGRAM_SIZE = 2

    name = 'vis-rodan.indexer.VF_ngram_indexer'
    author = "Ryan Bannon"
    description = "Index n-grams"
    settings = {}

    enabled = True
    category = "Indexer"
    interactive = False

    input_port_types = [{
        'name': 'NGram Indexer - horizontal intervals (Pandas DataFrame csv)',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    },
    {
        'name': 'NGram Indexer - vertical intervals (Pandas DataFrame csv)',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'n-grams - Pandas DataFrame csv',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        # Get files
        horizontal_intervals_file = inputs['NGram Indexer - horizontal intervals (Pandas DataFrame csv)'][0]['resource_path']
        vertical_intervals_file = inputs['NGram Indexer - vertical intervals (Pandas DataFrame csv)'][0]['resource_path']
        outfile = outputs['n-grams - Pandas DataFrame csv'][0]['resource_path']

        # De-serialize the DataFrames.
        horizontal_intervals = DataFrame.from_csv(horizontal_intervals_file, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        vertical_intervals = DataFrame.from_csv(vertical_intervals_file, header = [0, 1]) # We know the first two rows constitute a MultiIndex

        # Get the horizontal voice if not provided.
        voice_count = len(horizontal_intervals.columns)
        horizontal_voice = voice_count - 1
        if 'horizontal' in settings:
            horizontal_voice = int(settings['horizontal'][0][1])
        else:
            settings['horizontal'] = [('interval.HorizontalIntervalIndexer', str(horizontal_voice))]

        # Get all possible pairs if not provided
        if 'vertical' not in settings:
            settings['vertical'] = []
            suffix = ',' + str(horizontal_voice)
            for voice in xrange(horizontal_voice):
                pair = str(voice) + suffix
                settings['vertical'].append(('interval.IntervalIndexer', pair))

        # We also need a default for 'n'.
        if 'n' not in settings:
            settings['n'] = self.DEFAULT_NGRAM_SIZE

        # Index.
        all_intervals = concat([horizontal_intervals, vertical_intervals], axis=1)
        ngrams = NGramIndexer(all_intervals, settings).run()

        # Write results.
        ngrams.to_csv(outfile)

        return True
