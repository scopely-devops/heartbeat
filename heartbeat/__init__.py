# Copyright (c) 2014 Scopely, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import time
import logging
import json

import boto.ec2
import boto.utils

from datadog import initialize, api
from datadog.api.constants import CheckStatus
import time

LOG = logging.getLogger(__name__)


class HeartBeat(object):
    """
    This class will look up a tag on the instance it is running on
    and will then use that tag to create a custom metric that will
    be written to Datadog for a heartbeat metric.
    """

    def __init__(self, api_key, app_key, tag_name='Name'):
        self.api_key = api_key
        self.app_key = app_key
        self.tag_name = tag_name

    def send_to_datadog(self, tag, instance_id):
        options = {
            'api_key': self.api_key,
            'app_key': self.app_key
        }
        initialize(**options)
        api.ServiceCheck.check(check='jenkins.ok', host_name=tag + '_' + instance_id, status=CheckStatus.OK, message='Jenkins {} OK'.format(tag))

    def ping(self):
        metadata = boto.utils.get_instance_metadata()
        instance_id = metadata['instance-id']
        LOG.debug('instance_id=%s', instance_id)
        az = metadata['placement']['availability-zone']
        # hacky - is there a better way to find the region name?
        region_name = az[0:-1]
        LOG.debug('region=%s', region_name)
        ec2 = boto.ec2.connect_to_region(region_name)
        tags = ec2.get_all_tags(filters={'resource-id': instance_id})
        LOG.debug(tags)
        for tag in tags:
            if tag.name == self.tag_name:
                self.send_to_datadog(tag.value, instance_id)
                return
        LOG.error('Did not find requested tag: %s', self.tag_name)
        raise KeyError('Requested tag not found on instance')
