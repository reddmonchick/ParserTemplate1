import os
from pathlib import Path
from loguru import logger

from custom_exceptions.stop_id_exceptions import NoDefaultStopId, NoStopIdFilePath


class StopId:

    def __init__(self, default_stop_id: str=None):
        self.stop_id_file_path: str | None = self._get_stop_id_file_path()
        self.default_stop_id = default_stop_id
        self.stop_id = self._get_stop_id()

    def update_stop_id(self, new_stop_id: str | int):
        if not self.stop_id_file_path:
            raise NoStopIdFilePath('no right stop id file path')
        with open(self.stop_id_file_path, 'w', encoding='utf-8') as file:
            file.write(f"{new_stop_id}")

    def check_stop_condition(self, url):
        if self.stop_id == url:
            return True
        else:
            return False

    def _get_stop_id(self):
        if os.path.exists(self.stop_id_file_path):
            with open(self.stop_id_file_path, 'r', encoding='utf-8') as f:
                 stop_id = f.read().strip()
            return stop_id

        elif not self.default_stop_id:
            msg = 'No default stop id'
            logger.error(msg)
            raise NoDefaultStopId(msg)

        else:
            return self.default_stop_id

    def _get_stop_id_file_path(self):
        base_dir = Path(__file__).resolve().parent.parent
        file_path = os.path.join(base_dir, 'stopId.txt')
        return file_path
