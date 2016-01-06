__version__ = "0.0.1"

from rodan.jobs import module_loader

#module_loader('rodan.jobs.vis-rodan.indexers.cadence_indexer')
#module_loader('rodan.jobs.vis-rodan.indexers.dissonance_indexer')
#module_loader('rodan.jobs.vis-rodan.indexers.figuredbass_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.fermata_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.horizontal_interval_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.ngram_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.noterest_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.vertical_interval_indexer')