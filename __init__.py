from rodan.jobs import module_loader

from vis.analyzers.indexers.fermata import FermataIndexer
from vis.analyzers.indexers.interval import HorizontalIntervalIndexer, IntervalIndexer
from vis.analyzers.indexers.ngram import NGramIndexer
from vis.analyzers.indexers.noterest import NoteRestIndexer

module_loader('rodan.jobs.vis-rodan.indexers.fermata_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.horizontal_interval_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.ngram_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.noterest_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.vertical_interval_indexer')