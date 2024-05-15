from typing import Sequence, List
import time

from .game_info import *
from .stream_info import *
from .recorder import *


class MultiRecorder:
    _recorders: List[StreamRecorder] = []
    now_match_id: str | None = None

    def get_filename(self, match_info: dict, timestamp: float, name: str) -> str:
        return f"{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(timestamp))}" \
            f"_{match_info['matchType']}_{name}_" \
            f"{match_info['blueSide']['player']['team']['collegeName']}_{match_info['blueSide']['player']['team']['name']}" \
            "_vs_" \
            f"{match_info['redSide']['player']['team']['collegeName']}_{match_info['redSide']['player']['team']['name']}" \
            ".mkv"

    def start(self, match_info: dict ,streams: Sequence[StreamInfo]):
        print(f"Now Recording:" \
              f"{match_info['blueSide']['player']['team']['collegeName']}_{match_info['blueSide']['player']['team']['name']}" \
              " vs " \
              f"{match_info['redSide']['player']['team']['collegeName']}_{match_info['redSide']['player']['team']['name']}")
        self.now_match_id = match_info['id']
        ts = time.time()
        for s in streams:
            self._recorders.append(StreamRecorder(
                s.name, s.url, self.get_filename(match_info, ts, s.name)))

    def stop(self):
        self.now_match_id = None
        for r in self._recorders:
            r.stop()

if __name__ == "__main__":
    print("Welcome to RoboMaster live recorder.")
    m_recorder = MultiRecorder()
    try:
        while True:
            try:
                matches = get_matches()
                if m_recorder.now_match_id is None or check_done(matches, m_recorder.now_match_id):
                    m_recorder.stop()
                    m_recorder.start(get_now_match(matches), get_streams())
                else:
                    print("Still Matching...")
            except Exception as err:
                print(f"Error: {err}")
            finally:
                time.sleep(config.CHECK_TIME)
    except KeyboardInterrupt:
        print("Stopping...")
        m_recorder.stop()
