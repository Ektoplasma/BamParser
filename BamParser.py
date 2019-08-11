import windows
import json
import time
import struct
from datetime import datetime

class BamEntry(object):
    # executable = KeyValue('name','value','type')
    def __init__(self, pyhkey_sid):
        self.sid = pyhkey_sid.name
        self.executable = []
        for executable in pyhkey_sid.values:
            if executable[2] == 3:
                self._add_executable(executable)

    def _add_executable(self, executable):
        path = executable[0]
        timestamp = struct.unpack("<Q", executable[1][0:8])[0]
        date = self._convert_timestamp(timestamp)
        self.executable.append(
            {'path' : path,
            'date' : date})

    def _convert_timestamp(self, timestamp):
        s=float(timestamp)/1e7 # convert to seconds
        seconds = s-11644473600 # number of seconds from 1601 to 1970
        newtime = time.ctime(seconds)
        date_object = datetime.strptime(newtime, '%a %b %d %H:%M:%S %Y')
        date = date_object.strftime('%Y-%m-%d %H:%M:%S')

        return date



if __name__ == "__main__":
    registry = windows.system.registry
    win_build = windows.system.build_number
    if ("10.0.16299" in win_build) or ("10.0.17134" in win_build):
        bamreg = registry(r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bam\UserSettings')
    elif ("10.0.17763" in win_build) or ("10.0.18362" in win_build):
        # TODO: we could still get the old entries before the update, if they still exist
        bamreg = registry(r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bam\State\UserSettings')
    else:
        print("Version not supported.")
        exit()
    
    sids = bamreg.subkeys
    bam = []
    for phkey_sid in sids:
        bam_entry = BamEntry(phkey_sid)
        bam.append(bam_entry.__dict__)
    bam_json = json.dumps(bam, sort_keys=True, indent=4)
    with open("results.json","wb") as results:
        results.write(bam_json)
