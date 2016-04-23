# -*- coding: utf-8 -*-
'''
Generic hashing script. Supports files & directories
'''
from __future__ import absolute_import

import os
import json
import shutil
import difflib
import logging
from time import strftime

LOG = logging.getLogger(__name__)

__virtualname__ = 'fim'


def __virtual__():
    if ('file.get_hash' and 'file.stats') in __salt__:
        return __virtualname__


def _hasher(algo, target):
    '''
    Convenience function to handle hashing
    '''
    return __salt__['file.get_hash'](target, algo)


def _stats(target):
    '''
    Convenience function to handle stats
    '''
    return __salt__['file.stats'](target)


def checksum(algo='sha256', targets=[], excludes=[], filename='', *args, **kwargs):
    '''
    Generate dictionary of hashes and corresponding filenames.

    Supports file paths and or directories.
    '''
    checksums = {}
    hostname = __salt__['grains.get']('fqdn')

    ## check for preconfigured algos
    if not algo:
        try:
            if __salt__['config.get']('fim:algo'):
                algo = __salt__['config.get']('fim:algo')
        except KeyError:
            LOG.debug('No algorithm defined. Defaulting to sha256')

    ## check for preconfigured targets
    if not targets:
        try:
            if __salt__['config.get']('fim:targets'):
                targets = __salt__['config.get']('fim:targets')
        except KeyError:
            return 'No targets defined. Exiting'

    ## check for preconfigured exclusions. this can be a file or a directory
    if not excludes:
        try:
            if __salt__['config.get']('fim:exclude'):
                excludes = __salt__['config.get']('fim:excludes')
        except KeyError:
            LOG.debug('No targets to exclude. Defaulting to empty list')

    ## iterate through list of targets and generate checksums
    for target in targets:
        if os.path.isdir(target):
            for root, dirs, files in os.walk(target):
                dirs[:] = [d for d in dirs if d not in excludes]
                for file_ in files:
                    target = os.path.join(root, file_)
                    if os.path.isfile(target) and target not in excludes:
                        checksums[target] = {'stats': {}}
                        checksums[target]['stats'] = _stats(target)
                        checksums[target]['stats'].update({'checksum': _hasher(algo, target)})
                        checksums[target]['stats'].update({'hostname': hostname})
        elif os.path.isfile(target) and target not in excludes:
            checksums[target] = {'stats': {}}
            checksums[target]['stats'] = _stats(target)
            checksums[target]['stats'].update({'checksum': _hasher(algo, target)})
            checksums[target]['stats'].update({'hostname': hostname})

    return checksums


def diff():
    '''
    Generate unified diff of two most recent fim.dat files
    '''
    diff = []

    timestamp = strftime("%Y-%m-%d")

    new_path = __salt__['config.get']('fim:new_path')
    old_path = __salt__['config.get']('fim:old_path')

    root_dir = '/var/cache/salt/master/minions/'

    for minion in os.listdir(root_dir):
        try:
            for line in difflib.unified_diff(open(root_dir + minion + '/' + 'files' + old_path).readlines(),
                                             open(root_dir + minion + '/' + 'files' + new_path).readlines(), n=0):

                prefix_line = False
                for prefix in ('---', '+++', '@@'):
                    if line.startswith(prefix):
                        prefix_line = True
                if not prefix_line:
                    line = line.strip()
                    char = line[0]
                    line = line[1:]
                    line = line.replace("'", "\"")
                    line = json.loads(line)
                    line['diff'] = char
                    line['timestamp'] = timestamp
                    diff.append(line)
        except IOError:
            LOG.error('No previous run to compare. Run fim.rotate.')

    ret = '\n'.join([json.dumps(s) for s in diff])
    return ret


def rotate():
    '''
    Rotate the fim data files to .old
    '''
    new_path = __salt__['config.get']('fim:new_path')
    old_path = __salt__['config.get']('fim:old_path')

    root_dir = '/var/cache/salt/master/minions/'

    for minion in os.listdir(root_dir):
        shutil.copy(root_dir + minion + '/' + 'files' + new_path,
                    root_dir + minion + '/' + 'files' + old_path)

    return 'FIM data rotated.'

