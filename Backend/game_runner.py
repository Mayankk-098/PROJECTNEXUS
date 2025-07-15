import subprocess
import threading

class GameRunner:
    def __init__(self, exe_path, on_output):
        self.exe_path = exe_path
        self.on_output = on_output
        self.process = None
        self.thread = None

    def start_game(self):
        self.process = subprocess.Popen(
            self.exe_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )

        self.thread = threading.Thread(target=self.read_output)
        self.thread.daemon = True
        self.thread.start()

    def read_output(self):
        for line in self.process.stdout:
            self.on_output(line)

    def send_input(self, user_input):
        if self.process:
            self.process.stdin.write(user_input + '\n')
            self.process.stdin.flush()

    def stop_game(self):
        if self.process:
            self.process.terminate()
            self.process = None
