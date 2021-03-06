# $Id: get_machines.py 2016-12-17 $
# Author: Coen Meerbeek <coen@buzzardlabs.com>
# Copyright: BuzzarLabs 2016

"""
This file retrieves machines from an Octopus application
"""

import logging, json, requests, time, sys
import ConfigParser
import splunk.Intersplunk as isp
import octopus_common

# Parse octopus.conf for configuration settings
stanza = octopus_common.getSelfConfStanza("octopus")
protocol = stanza['protocol']
hostname = stanza['hostname']
apikey 	 = stanza['apikey']

# Setup logger object
logger = octopus_common.setup_logging()
logger.info(time.time())

try:
  octopus_url = protocol + "://" + hostname + "/api/machines/all"

  # Setup response object and execute GET request
  response = requests.get(
    url = octopus_url,
    headers = {
      "X-Octopus-ApiKey": apikey,
    },
  )
  response.raise_for_status()

  # Handle response
  json_response = json.loads(response.content)

  # Iterate projects and print results to Splunk
  for machine in json_response:
    print json.dumps(machine)

  sys.exit(0)

# Catch exceptions if needed
except Exception as e:
  logger.exception("Exception: " + str(e))
  isp.generateErrorResults(str(e))