import time
import json
import os
import shutil

from scrimmage.utilities import Thread


class DB:
    def __init__(self):
        self.data = None
        if not os.path.exists('db.json'):
            self.data = list()
        else:
            with open('db.json', 'r') as f:
                self.data = json.load(f)

        self.lock = False

        self.save_thread = Thread(self.live_saving, ())
        self.save_thread.start()

    def add_entry(self, **kwargs):
        entry = {
            'tid': kwargs['tid'] if 'tid' in kwargs else None,
            'teamname': kwargs['teamname'] if 'teamname' in kwargs else None,
            'vis_logs': kwargs['vis_logs'] if 'vis_logs' in kwargs else None,
            'code_file': kwargs['code_file'] if 'code_file' in kwargs else None,
            'submissions': 0,
        }

        if not os.path.exists(f'scrimmage/scrim_clients/{kwargs["teamname"]}'):
            os.mkdir(f'scrimmage/scrim_clients/{kwargs["teamname"]}')

        self.data.append(entry)

    def delete_entry(self, tid=None, teamname=None):
        for entry in self.data:
            if tid is not None and entry['tid'] == str(tid):
                self.data.remove(entry)
                shutil.rmtree(f'scrimmage/scrim_clients/{entry["teamname"]}')
                break
            if teamname is not None and entry['teamname'] == teamname:
                self.data.remove(entry)
                shutil.rmtree(f'scrimmage/scrim_clients/{entry["teamname"]}')
                break

    def query(self, tid=None, teamname=None):
        self.await_lock()

        results = list()
        for entry in self.data:
            if tid is not None and entry['tid'] != tid:
                continue
            if teamname is not None and entry['teamname'] != teamname:
                continue

            results.append(entry)

        self.lock = False
        return results

    def dump(self):
        self.await_lock()

        self.lock = False
        return self.data

    def await_lock(self):
        while self.lock:
            time.sleep(1)
        self.lock = True

    def live_saving(self):
        while True:
            time.sleep(5)

            self.await_lock()
            with open('db.json', 'w+') as f:
                json.dump(self.data, f)

            self.lock = False
