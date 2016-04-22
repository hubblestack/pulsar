beacons:
  inotify:
    /etc: {}
    /lib: {}
    /bin: {}
    /sbin: {}
    /boot: {}
    /lib64: {}
    /usr/lib: {}
    /usr/bin: {}
    /opt/bin: {}
    /usr/sbin: {}
    /opt/sbin: {}
    /usr/lib64: {}
    /usr/local/etc: {}
    /usr/local/bin: {}
    /usr/local/lib: {}
    /usr/local/sbin: {}
    /var:
      exclude:
        - /var/log
        - /var/spool
        - /var/cache
        - /var/lock

    recurse: True
    auto_add: True
    disable_during_state_run: True
