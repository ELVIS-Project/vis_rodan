#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           vis-rodan
# Program Description:    Job wrappers that allows vis-framework to work in Rodan.
#
# Filename:               vis-rodan/indexers/horizontal_interval_indexer.py
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

from pandas import DataFrame
from rodan.jobs.base import RodanTask
from vis.analyzers.indexers.interval import HorizontalIntervalIndexer

import logging
logger = logging.getLogger('rodan')

class VRHorizontalIntervalIndexer(RodanTask):

    name = 'vis-rodan.indexer.VF_horizontal_interval_indexer'
    author = "Ryan Bannon"
    description = "Index horizontal intervals"
    settings = {}

    enabled = True
    category = "Indexer"
    interactive = False

    input_port_types = [{
        'name': 'Horizontal Interval Indexer - indexed piece (Pandas DataFrame csv)',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Horizontal Interval Indexer - Pandas DataFrame csv',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        infile = inputs['Horizontal Interval Indexer - indexed piece (Pandas DataFrame csv)'][0]['resource_path']
        outfile = outputs['Horizontal Interval Indexer - Pandas DataFrame csv'][0]['resource_path']
        data = DataFrame.from_csv(infile, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        #execution_settings = dict( [(k, settings[k]) for k in ('simple or compound', 'quality')] )
        horizontal_intervals = HorizontalIntervalIndexer(data, settings).run()
        horizontal_intervals.to_csv(outfile)

        return True