#win_notify
'''
This will setup your computer to enable auditing for specified folders inputted into a yaml file. It will
then scan the event log for changes to those folders every 5 minutes and report when it finds one.
'''


from __future__ import absolute_import

import collections
import datetime
import fnmatch
import logging
import os

import salt.ext.six

LOG = logging.getLogger(__name__)
DEFAULT_MASK = ['ExecuteFile', 'Write', 'Delete', 'DeleteSubdirectoriesAndFiles', 'ChangePermissions', 'Takeownership']
DEFAULT_TYPE = 'all'

__virtualname__ = 'win_notify'

def __virtual__():
    if not salt.utils.is_windows():
        return False, 'This module only works on windows'
    return __virtualname__

def validate(config):
    '''
    Validate the beacon configuration.
    Once that is done it will return a successful validation
    :param config:
    :return:
    '''
<<<<<<< HEAD
    VALID_MASK = [
        'ExecuteFile',
        'ReadData',
        'ReadAttributes',
        'ReadExtendedAttributes',
        'CreateFiles',
        'AppendData',
        'WriteAttributes',
        'WriteExtendedAttributes',
        'DeleteSubdirectoriesAndFiles',
        'Delete',
        'ReadPermissions',
        'ChangePermissions',
        'TakeOwnership',
        'Write',
        'Read',
        'ReadAndExecute',
        'Modify'
    ]

    VALID_TYPE = [
        'all',
        'success',
        'fail'
    ]

=======
>>>>>>> a0f805608b185cfdb429bfef921045462594ae4f
    # Configuration for win_notify beacon should be a dict of dicts
    log.debug('config {0}'.format(config))
    if not isinstance(config, dict):
        return False, 'Configuration for win_notify beacon must be a dictionary.'
    else:
        for config_item in config:
            if not isinstance(config[config_item], dict):
                return False, 'Configuration for win_notify beacon must be a dictionary of dictionaries.'
            else:
                if not any(j in ['mask', 'recurse'] for j in config[config_item]):
                    return False, 'Configuration for win_notify beacon must contain mask, recurse or auto_add items.'

            if 'recurse' in config[config_item]:
                if not isinstance(config[config_item]['recurse'], bool):
                    return False, 'Configuration for win_notify beacon recurse must be boolean.'

            if 'mask' in config[config_item]:
                if not isinstance(config[config_item]['mask'], list):
                    return False, 'Configuration for win_notify beacon mask must be list.'
                for mask in config[config_item]['mask']:
                    if mask not in VALID_MASK:
                        return False, 'Configuration for win_notify beacon invalid mask option {0}.'.format(mask)

            if 'wtype' in config[config_item]:
                if not isinstance(config[config_item]['wtype'], str):
                    return False, 'Configuration for win_notify beacon type must be str.'
                for wtype in config[config_item]['wtype']:
                    if wtype not in VALID_TYPE:
                        return False, 'Configuration for win_notify beacon invalid type option {0}'.format(wtype)
        return True, 'Valid beacon configuration'


def beacon(config):
    '''
    Watch the configured files

    Example Config

    .. code-block:: yaml

      beacons:
        win_notify:
          /path/to/file/or/dir:
            mask:
              - Write
              - ExecuteFile
              - Delete
              - DeleteSubdirectoriesAndFiles
            wtype: all
            recurse: True
            exclude:
              - /path/to/file/or/dir/exclude1
              - /path/to/file/or/dir/exclude2

    The mask list can contain the following events (the default mask is create, delete, and modify):

        1.  ExecuteFile                     - Traverse folder / execute file
        2.  ReadData                        - List folder / read data
        3.  ReadAttributes                  - Read attributes of object
        4.  ReadExtendedAttributes          - Read extended attributes of object
        5.  CreateFiles                     - Create files / write data
        6.  AppendData                      - Create folders / append data
        7.  WriteAttributes                 - Write attributes of object
        8.  WriteExtendedAttributes         - Write extended attributes of object
        9.  DeleteSubdirectoriesAndFiles    - Delete subfolders and files
        10. Delete                          - Delete an object
        11. ReadPermissions                 - Read Permissions of an object
        12. ChangePermissions               - Change permissions of an object
        13. TakeOwnership                   - Take ownership of an object
        14. Write                           - Combination of 5, 6, 7, 8
        15. Read                            - Combination of 2, 3, 4, 11
        16. ReadAndExecute                  - Combination of 1, 2, 3, 4, 11
        17. Modify                          - Combination of 1, 2, 3, 4, 5, 6, 7, 8, 10, 11

       *If you want to monitor everything (A.K.A. Full Control) then you want options 9, 12, 13, 17

    recurse:
        Recursively watch files in the directory
    wtype:
        Type of Audit to watch for:
            1. Success  - Only report successful attempts
            2. Fail     - Only report failed attempts
            3. All      - Report both Success and Fail
    exclude:
        Exclude directories or files from triggering events in the watched directory

    :return:
    '''
    ret = []

<<<<<<< HEAD
=======
    VALID_MASK = [
        'ExecuteFile',
        'ReadData',
        'ReadAttributes',
        'ReadExtendedAttributes',
        'CreateFiles',
        'AppendData',
        'WriteAttributes',
        'WriteExtendedAttributes',
        'DeleteSubdirectoriesAndFiles',
        'Delete',
        'ReadPermissions',
        'ChangePermissions',
        'TakeOwnership',
        'Write',
        'Read',
        'ReadAndExecute',
        'Modify'
    ]

    VALID_TYPE = [
        'all',
        'success',
        'fail'
    ]

>>>>>>> a0f805608b185cfdb429bfef921045462594ae4f
    # Validate ACLs on watched folders/files and add if needed
    for path in config:
        if isinstance(config[path], dict):
            mask = config[path].get('mask', DEFAULT_MASK)
            wtype = config[path].get('wtype', DEFAULT_TYPE)
            recurse = config[path].get('recurse', True)
<<<<<<< HEAD
            if isinstance(mask, list) and isinstance(wtype, str) and isinstance(recurse, bool):
                success = _check_acl(path, mask, wtype, recurse)
                if not success:
                    confirm = _add_acl(path, mask, wtype, recurse)
                if config[path].get('exclude', False):
                    _remove_acl(path)
=======
            if isinstance(mask, list) and isinstance(wtype, str) and isinstance('recurse', bool):
                success = _check_acl(path, mask, wtype, recurse)
            if not success:
                _add_acl(path, mask, wtype, recurse)
            if config[path].get('exclude', False):
                _remove_acl(path)
>>>>>>> a0f805608b185cfdb429bfef921045462594ae4f

    #Read in events since last call.  Time_frame in minutes
    ret = _pull_events('-5')
    return ret


def _check_acl(path, mask, wtype, recurse):
    audit_dict = {}
    success = True
    if 'all' in wtype.lower():
        wtype = ['Success', 'Failure']
    else:
        wtype = [wtype]

    audit_acl = __salt__['cmd.run']('(Get-Acl {0} -Audit).Audit | fl'.format(path), shell='powershell',
                                    python_shell=True)
    if not audit_acl:
        success = False
        return success
    audit_acl = audit_acl.replace('\r','').split('\n')
    for line in audit_acl:
        if line:
            d = line.split(':')
            audit_dict[d[0].strip()] = d[1].strip()
    for item in mask:
        if item not in audit_dict['FileSystemRights']:
            success = False
    for item in wtype:
        if item not in audit_dict['AuditFlags']:
            success = False
    if 'Everyone' not in audit_dict['IdentityReference']:
        success = False
    if recurse:
        if 'ContainerInherit' and 'ObjectInherit' not in audit_dict['InheritanceFlags']:
            success = False
    else:
        if 'None' not in audit_dict['InheritanceFlags']:
            success = False
    if 'None' not in audit_dict['PropagationFlags']:
        success = False
    return success


def _add_acl(path, mask, wtype, recurse):
    '''
    This will apply the needed audit ALC to the folder in question using PowerShell with the code below:
      $AccessRule = New-Object System.Security.AccessControl.FileSystemAuditRule($AuditUser,$AuditRules,$InheritType,
                    $PropagationFlags,$AuditType)
      $ACL = Get-Acl -Audit $TargetFolder
      $ACL.SetAuditRule($AccessRule)
      $ACL | Set-Acl $TargetFolder

    :return:
    '''
    audit_user = 'Everyone'
    audit_rules = ','.join(mask)
    if recurse:
        inherit_type = 'ContainerInherit,ObjectInherit'
    else:
        inherit_type = 'None'
    if 'all' in wtype:
        audit_type = 'Success,Failure'
    else:
        audit_type = wtype
    propagation_flags = 'None'
    __salt__['cmd.run']('$accessrule = New-Object System.Security.AccessControl.FileSystemAuditRule('
                                  '"{0}","{1}","{2}","{3}","{4}"); $acl = Get-Acl {5}; $acl.SetAuditRule($accessrule); '
                                  '$acl | Set-Acl {5}'.format(audit_user, audit_rules, inherit_type, propagation_flags,
                                                              audit_type, path), shell='powershell', python_shell=True)
    return 'ACL set up for {0} - with {1} user, {2} rules, {3} audit_type, and recurse is {4}'.format(path, audit_user, 
                                                                                                      audit_rules,
                                                                                                      audit_type, recurse)


def _remove_acl(path):
    '''
    This will remove a currently configured ACL on the folder submited as item.  This will be needed when you have
    a sub file or folder that you want to explicitly ignore within a folder being monitored.  You need to pass in the
    full folder path name for this to work properly
    :param item:
    :return:
    '''
    command = __salt__['cmd.run']('$acl = Get-Acl ${0}; $acl.GEtAuditRules($True, $False, '
                                '[System.Security.Principal.SecurityIdentifier]) | Foreach-Object '
                                '{ $acl.RemoveAuditRule($_); }); Set-Acl ${0} $acl'.format(path), shell='powershell',
                                python_shell=True)



def _pull_events(time_frame):
    events_list = []
    events_output = __salt__['cmd.run_stdout']('Get-EventLog -LogName Security -After ((Get-Date).AddMinutes({0})) '
                                        '-InstanceId 4663 | fl'.format(time_frame), shell='powershell',
                                        python_shell=True)
    events = events_output.split('\n\n')
    for event in events:
        if event:
            event_dict = {}
            items = event.split('\n')
            for item in items:
                if ':' in item:
                    item.replace('\t', '')
                    k, v = item.split(':', 1)
                    event_dict[k.strip()] = v.strip()
            event_dict['Accesses'] = _get_access_translation(event_dict['Accesses'])
            event_dict['Hash'] = _get_item_hash(event_dict['Object Name'])
            #needs hostname, checksum, filepath, time stamp, action taken
            events_list.append({k: event_dict[k] for k in ('EntryType', 'Accesses', 'TimeGenerated', 'Object Name', 'Hash')})
    return events_list

def _get_access_translation(access):
    '''
    This will take the access number within the event, and return back a meaningful translation.
    These are all the translations of accesses:
        1537 DELETE - used to grant or deny delete access.
        1538 READ_CONTROL - used to grant or deny read access to the security descriptor and owner.
        1539 WRITE_DAC - used to grant or deny write access to the discretionary ACL.
        1540 WRITE_OWNER - used to assign a write owner.
        1541 SYNCHRONIZE - used to synchronize access and to allow a process to wait for an object to enter the signaled state.
        1542 ACCESS_SYS_SEC
        4416 ReadData
        4417 WriteData
        4418 AppendData
        4419 ReadEA (Extended Attribute)
        4420 WriteEA (Extended Attribute)
        4421 Execute/Traverse
        4423 ReadAttributes
        4424 WriteAttributes
        4432 Query Key Value
        4433 Set Key Value
        4434 Create Sub Key
        4435 Enumerate sub-keys
        4436 Notify about changes to keys
        4437 Create Link
        6931 Print
    :param access:
    :return access_return:
    '''
    access_dict = {'1537': 'Delete', '1538': 'Read Control', '1539': 'Write DAC', '1540': 'Write Owner',
                   '1541': 'Synchronize', '1542': 'Access Sys Sec', '4416': 'Read Data', '4417': 'Write Data',
                   '4418': 'Append Data', '4419': 'Read EA', '4420': 'Write EA', '4421': 'Execute/Traverse',
                   '4423': 'Read Attributes', '4424': 'Write Attributes', '4432': 'Query Key Value',
                   '4433': 'Set Key Value', '4434': 'Create Sub Key', '4435': 'Enumerate Sub-Keys',
                   '4436': 'Notify About Changes to Keys', '4437': 'Create Link', '6931': 'Print', }

    access = access.replace('%%', '').strip()
    ret_str = access_dict.get(access, False)
    if ret_str:
        return ret_str
    else:
        return 'Access number {0} is not a recognized access code.'.format(access)


def _get_item_hash(item):
    if '.' in item:
        hashy = __salt__['file.get_hash']('{}'.format(item))
        return hashy
    else:
        return 'Item is a directory'

