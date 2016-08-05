beacons:
  pulsar:
    /etc: { recurse: True, auto_add: True }
    /lib: { recurse: True, auto_add: True }
    /bin: { recurse: True, auto_add: True }
    /sbin: { recurse: True, auto_add: True }
    /boot: { recurse: True, auto_add: True }
    /lib64: { recurse: True, auto_add: True }
    /usr/lib: { recurse: True, auto_add: True }
    /usr/bin: { recurse: True, auto_add: True }
    /usr/sbin: { recurse: True, auto_add: True }
    /usr/lib64: { recurse: True, auto_add: True }
    /usr/local/etc: { recurse: True, auto_add: True }
    /usr/local/bin: { recurse: True, auto_add: True }
    /usr/local/lib: { recurse: True, auto_add: True }
    /usr/local/sbin: { recurse: True, auto_add: True }
    /var:
      exclude:
        - /var/log
        - /var/spool
        - /var/cache
        - /var/lock
        - /var/lib/ntp
        - /var/lib/mlocate
        - /var/lib/logrotate.status
      recurse: True
      audo_add: True
    return: slack_pulsar
    checksum: sha256
    stats: True
    batch: False
