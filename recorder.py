import av
from threading import Thread, Event


class StreamRecorder:
    _thread: Thread
    _stop_event: Event
    name: str

    def __init__(self, name, input_url, output_filename):
        print(f"Recording {name} to {output_filename}")
        self.name = name
        self._stop_event = Event()
        self._thread = Thread(name=name, target=self.stream_worker, args=(input_url, output_filename))
        self._thread.start()

    def stream_worker(self, input_url, output_filename):
        # Open the input stream
        input_container = av.open(input_url)

        # Open the output stream
        output_container = av.open(output_filename, mode='w')

        # Copy the streams from input to output
        output_streams = {}
        for stream in input_container.streams:
            output_stream = output_container.add_stream(template=stream)
            output_streams[stream.index] = output_stream

        # Read from the input and write to the output
        for packet in input_container.demux():
            packet.stream = output_streams[packet.stream.index]
            output_container.mux(packet)
            if self._stop_event.is_set():
                print(f"Recorder {self.name} Exiting...")
                break

        output_container.close()
        input_container.close()

    def stop(self):
        if self._thread.is_alive():
            self._stop_event.set()

    def __del__(self):
        self.stop()
        self._thread.join()


if __name__ == "__main__":
    input_url = "https://rtmp.djicdn.com/robomaster/ual2024-beibu.m3u8?auth_key=1714034239-0-0-58bb9500239eec501606d2dab3004f66"
    output_filename = "output.mkv"
    sr = StreamRecorder('test', input_url, output_filename)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        sr.stop()
