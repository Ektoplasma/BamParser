import windows
from windows.generated_def import KEY_READ, REG_QWORD
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
    bamreg = registry(r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bam\UserSettings')
    sids = bamreg.subkeys
    bam = []
    for phkey_sid in sids:
        bam_entry = BamEntry(phkey_sid)
        bam.append(bam_entry.__dict__)
    bam_json = json.dumps(bam, sort_keys=True, indent=4)
    with open("results.json","wb") as results:
        results.write(bam_json)
