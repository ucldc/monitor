#!/usr/bin/env python3
import argparse
import sys
import logging

from pprint import pprint as pp
from botocore.client import Config

import requests

import boto3


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--loglevel', default='ERROR', required=False)
    if argv is None:
        argv = parser.parse_args()

    # set debugging level
    numeric_level = getattr(logging, argv.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % argv.loglevel)
    logging.basicConfig(level=numeric_level, )

    status = check(argv.url)
    print(status)
    if status:
        return 0
    else:
        return 1


def restart(environment):
    #{'application': 'potto-loris',
    #'environment': 'pottoLoris-env-clone',
    #'url': 'http://pottoloris-env-clone.us-west-2.elasticbeanstalk.com/'}
    logging.debug(environment)
    client = boto3.client(
        'elasticbeanstalk', config=Config(region_name='us-west-2'))

    response = client.describe_environments(
        EnvironmentNames=[environment.get('environment')], )['Environments'][0]

    if response['AbortableOperationInProgress']:
        logger.info('AbortableOperationInProgress')
        return False

    if not 'http://{}/'.format(response.get('CNAME')) == environment.get(
            'url'):
        logger.info('{} does not match {}'.format(
            response.get('CNAME'), environment.get('url')))
        return False

    response = client.restart_app_server(
        EnvironmentName=environment.get('environment'), )
    print(response)


def check(url):
    logging.info('checking {} ...'.format(url))
    try:
        result = requests.get(url, timeout=1)
    except requests.exceptions.ConnectTimeout:
        return False

    if result.text == 'potto-loris status okay':
        return True
    else:
        return False


if __name__ == "__main__":
    sys.exit(main())
"""
Copyright © 2016, Regents of the University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
