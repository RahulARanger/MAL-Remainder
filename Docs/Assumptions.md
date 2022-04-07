---
layout: default
title: Assumptions
nav_order: 4
permalink: /docs/assumptions
---

I have used certain techniques or methods which i believe would work without any proper tests.
Please feel free to correct me or suggest any other efficient method.

# Global Lock

I hope this is one of the way to create Global lock in python

This can was used in _[common_utils.py's EnsurePort](https://github.com/RahulARanger/MAL-Remainder/blob/933c3e2bffcafd667ac6b24ed13fd7824888531a/MAL_Remainder/common_utils.py#L27)_

```python
import pathlib
import sqlite3
import os

class GlobalLock:
    def __init__(self, prefix="lock"):
        self.root = pathlib.Path(os.getcwd()) / (prefix + ".db")
        self.connection = None
    
    def is_locked(self):  # considering that this function is called from another processes
        """
        returns True if locked else False
        """
        before = self.root.exists()
        self.connection = sqlite3.connect(self.root)
        if not before:
            return False
        self.connection.close()
        try:
            # in case if the previous file is not deleted
            self.root.unlink()
        except PermissionError:
            self.connection.close()
            return True
        
        return False

if __name__ == "__main__":
    sample = GlobalLock()
    locked = sample.is_locked()

    if not locked:
        input("Press to Close")
        sample.connection.close()
        print("closed")
        # sample.root.unlink()
        # system might fail to execute the above line. 
    else:
        print("Process is locked !")
```
