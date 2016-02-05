"""
This distributor was generated from a template
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           vis-rodan
# Program Description:    Job wrappers that allows vis-framework to work in Rodan.
#
# Filename:               vis-rodan/resource_distributors/pandas_serialized_dataframe_csv_distributor.py.py
# Purpose:                Pandas serialized DataFrame csv Distributor
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

from rodan.jobs.base import RodanTask
from shutil import copyfile

import logging
logger = logging.getLogger('rodan')

class VRPandasserializedDataFramecsvDistributor(RodanTask):

    name = 'Pandas serialized DataFrame csv Distributor'
    author = "Marina Borsodi-Benson"
    description = "Pandas serialized DataFrame csv Distributor"
    settings = {}

    enabled = True
    category = "Resource Distributor"
    interactive = False

    input_port_types = [{
        'name': 'Pandas serialized DataFrame csv ',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Pandas serialized DataFrame csv ',
        'resource_types': ['application/x-pandas_dataframe+csv'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        infile = inputs['Pandas serialized DataFrame csv Distributor'][0]['resource_path']
        outfile = outputs['Pandas serialized DataFrame csv Distributor'][0]['resource_path']
        copyfile(infile, outfile)

        return True