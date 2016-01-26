__version__ = "0.0.1"

from rodan.jobs import module_loader

module_loader('rodan.jobs.vis-rodan.indexers.dissonance_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.duration_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.figuredbass_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.fermata_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.horizontal_interval_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.measure_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.ngram_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.noterest_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.notebeatstrength_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.offset_indexer')
module_loader('rodan.jobs.vis-rodan.indexers.vertical_interval_indexer')

module_loader('rodan.jobs.vis-rodan.resource_distributors.musicxml_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.noterest_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.dissonance_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.duration_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.fermata_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.figured_bass_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.horizontal_interval_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.measure_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.nbs_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.ngram_distributor')
module_loader('rodan.jobs.vis-rodan.resource_distributors.vertical_interval_distributor')