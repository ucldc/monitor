#!/usr/bin/env python3
import argparse
import time
import sys
import os
import logging
import logging.handlers
import boto3
from botocore.client import Config
from pprint import pprint as pp
import errno

from appdirs import user_data_dir
import appdirs
import toml
import daemonocle

from potto import check, restart

DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG = toml.loads(open(os.path.join(DIR, "config.toml")).read())


def check_loop():
    while True:
        for env in CONFIG['iiif'].values():
            if check(env.get('url')):
                # looks good
                logging.debug('{} looks good'.format(env.get('url')))
            else:
                logging.warning('{} looks wrong, restarting'.format(
                    env.get('url')))
                restart(env)
        time.sleep(60)


def main(argv=None):
    pid = os.path.join(appdirs.user_data_dir(), 'monitor.pid')
    log = os.path.join(appdirs.user_log_dir(), 'monitor.log')
    parser = argparse.ArgumentParser()
    parser.add_argument('--detach', dest='detach', action='store_true')
    parser.add_argument('--no-detach', dest='detach', action='store_false')
    parser.add_argument('--pid', default=pid)
    parser.add_argument('--log', default=log)
    parser.set_defaults(detach=True)

    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.add_parser('start')
    subparsers.add_parser('stop')
    subparsers.add_parser('status')
    subparsers.add_parser('restart')

    parser.add_argument('--loglevel', default='ERROR', required=False)
    if argv is None:
        argv = parser.parse_args()

    try:
        os.mkdir(appdirs.user_log_dir())
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
        pass

    # set debugging level
    numeric_level = getattr(logging, argv.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % argv.loglevel)

    # logging to root logger, why not?
    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    rh = logging.handlers.TimedRotatingFileHandler(
        argv.log,
        when='midnight', )
    rh.setLevel(numeric_level)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    rh.setFormatter(formatter)
    logger.addHandler(rh)

    logging.info('Daemon is starting')

    if len(sys.argv) == 1:  # http://stackoverflow.com/a/4042861/1763984
        parser.print_help()
        sys.exit(1)

    daemon = daemonocle.Daemon(
        worker=check_loop,
        workdir=os.getcwd(),
        pidfile=argv.pid,
        detach=argv.detach, )

    logging.info(argv.subcommand)
    daemon.do_action(argv.subcommand)


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
