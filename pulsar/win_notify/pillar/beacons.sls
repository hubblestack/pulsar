beacons:
  win_notify:
    C:\Users: {}
    C:\Windows:
      mask:
        - Write
        - Delete
        - DeleteSubdirectoriesAndFiles
        - ChangePermissions
        - TakeOwnership
      exclude:
        - C:\Windows\System32
    C:\temp: {}

    win_notify_interval: 30 # MUST be the same as interval
    interval: 30 # MUST be the same as win_notify_interval
      
