import logging, os, sys, time, ConfigParser
import requests
import mediameter.cliff
import mediacloud

GEONAMES_TAG_PREFIX = 'geonames_'

start_time = time.time()
current_dir = os.path.dirname(os.path.abspath(__file__))

# set up logging
logging.basicConfig(filename=os.path.join(current_dir,'labeller.log'),level=logging.INFO)
log = logging.getLogger(__name__)
log.info("---------------------------------------------------------------------------")
start_time = time.time()
requests_logger = logging.getLogger('requests')
requests_logger.setLevel(logging.WARN)

# load up settings
settings = ConfigParser.ConfigParser()
settings_file_path = os.path.join(current_dir,'settings.config')
settings.read(settings_file_path)
geo_tag_sets_id = settings.get('mediacloud','geo_tag_sets_id')
tags_to_get = int(settings.get('mediacloud','tags_to_label'))
last_tags_id = settings.get('mediacloud','last_tags_id')
log.info("Labelling %s tags from tag set %s (starting at %s)" % (tags_to_get,geo_tag_sets_id,last_tags_id) )

# connect to stuff
mc = mediacloud.api.AdminMediaCloud(settings.get('mediacloud','key'))
cliff = mediameter.cliff.Cliff(settings.get('cliff','host'),settings.get('cliff','port'))
log.info("  Connected to cliff at %s:%s" % (settings.get('cliff','host'), settings.get('cliff','port')))

tagged_count = 0
tags = mc.tagList(geo_tag_sets_id,last_tags_id,tags_to_get)
new_last_tag_id = last_tags_id
for tag in tags:
    log.debug("  tag %d %s" % (tag['tags_id'],tag['tag']) )
    if tag['tag'].startswith(GEONAMES_TAG_PREFIX):
        geonames_id = tag['tag'].replace(GEONAMES_TAG_PREFIX,"")
        tagged_count = tagged_count + 1
        geoname = cliff.geonamesLookup(geonames_id)
        tag_label = geoname['name']
        tag_description = geoname['name'] + " | " + geoname['featureClass'] + " | " + geoname['countryCode']
        mc.updateTag(tag['tags_id'],tag['tag'],tag_label,tag_description)
        log.info("  updated tag %s for %s (%s)" % (tag['tags_id'],tag_label,geonames_id))
    else:
        log.info("  doesn't start with '%s'... ignoring" % GEONAMES_TAG_PREFIX)
    new_last_tag_id = tag['tags_id']
    # and save that we've made progress (doing this after every one for better re-entry)
    settings.set('mediacloud','last_tags_id',new_last_tag_id)
    with open(settings_file_path, 'wb') as configfile:
        settings.write(configfile)

# log some stats about the run
duration_secs = float(time.time() - start_time)
log.info("  modified %d tags" % tagged_count)
log.info("  took %d seconds total" % duration_secs)
log.info("Done")
