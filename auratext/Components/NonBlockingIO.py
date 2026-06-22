import subprocess
import queue
import threading
import sys
import os
import platform

# Platform-specific imports
if platform.system() != "Windows":
    import fcntl

# 1024 bytes was way too small, and with this chunk size, it
# still sometimes takes two reads to get everything (that's fine)
CHUNK_SIZE = 64 * 1024


class NonBlockingIO:
    def __init__(self, process: subprocess.Popen[bytes]) -> None:
        self._process = process

        # Reads can obviously block, but flushing can block too, see #635
        # Nonblock flags don't help with writing, it raises error if it would block
        self._write_queue: queue.Queue[bytes] = queue.Queue()
        threading.Thread(target=self._write_queue_to_stdin, daemon=True).start()

        if sys.platform == "win32":
            self._read_queue: queue.Queue[bytes] = queue.Queue()
            self._reader_thread = threading.Thread(target=self._stdout_to_read_queue, daemon=True)
            self._reader_thread.start()
        else:
            # this works because we don't use .readline()
            # https://stackoverflow.com/a/1810703
            assert process.stdout is not None
            fileno = process.stdout.fileno()
            old_flags = fcntl.fcntl(fileno, fcntl.F_GETFL)
            new_flags = old_flags | os.O_NONBLOCK
            fcntl.fcntl(fileno, fcntl.F_SETFL, new_flags)

    def _write_queue_to_stdin(self) -> None:
        while self._process.poll() is None:
            # Why timeout: if process dies and no more to write, stop soon
            try:
                chunk = self._write_queue.get(timeout=5)
            except queue.Empty:  # timed out
                continue

            # Process can exit while waiting, but clean shutdown involves
            # writing messages before the process exits, so here it should
            # be still alive
            assert self._process.stdin is not None
            self._process.stdin.write(chunk)
            self._process.stdin.flush()

    if sys.platform == "win32":

        def _stdout_to_read_queue(self) -> None:
            while True:
                # for whatever reason, nothing works unless i go ONE BYTE at a
                # time.... this is a piece of shit
                #
                # TODO: read1() method?
                assert self._process.stdout is not None
                one_fucking_byte = self._process.stdout.read(1)
                if not one_fucking_byte:
                    break
                self._read_queue.put(one_fucking_byte)

    # Return values:
    #   - nonempty bytes object: data was read
    #   - empty bytes object: process exited
    #   - None: no data to read
    def read(self) -> bytes | None:
        if sys.platform == "win32":
            buf = bytearray()
            while True:
                try:
                    buf += self._read_queue.get(block=False)
                except queue.Empty:
                    break

            if self._reader_thread.is_alive() and not buf:
                return None
            return bytes(buf)

        else:
            assert self._process.stdout is not None
            return self._process.stdout.read(CHUNK_SIZE)

    def write(self, bytez: bytes) -> None:
        self._write_queue.put(bytez)