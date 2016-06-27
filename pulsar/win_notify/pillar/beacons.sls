beacons:
  win_notify:
    C:/Windows:
      exclude:
        - C:/Windows/MEMORY.DMP
        - C:/Windows/System

    C:/temp:
      mask:
        - Write
      wtype: Success
      
