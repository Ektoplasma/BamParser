# BamParser
Python parser for Background Activity Moderator  
BAM is a Windows service that Controls activity of background applications.  
This service exists in Windows 10 only after Fall Creators update – version 1709. 

It provides full path of the executable file that was run on the system and last execution date/time, and its located in this registry path:

HKLM\SYSTEM\CurrentControlSet\Services\bam\UserSettings\\{SID}

It contains a list of paths and executables, and the value of each of those is the time last executed in Filetime (64bit little Endian) format in UTC.

Since Win10 version 1809 and 1903, BAM stopped updating "\bam\UserSettings" (old entries may still be found there) and now updates "bam*State*\UserSettings" (source: [https://github.com/kacos2000/Win10/blob/master/Bam/readme.md](https://github.com/kacos2000/Win10/blob/master/Bam/readme.md))

Current version supports v1709 to 1903. Might work on Windows Server 2016 (TODO).

Python 2.7 only because it's using [hakril's PythonForWindows](https://github.com/hakril/PythonForWindows) which is only Python 2 compatible atm.

