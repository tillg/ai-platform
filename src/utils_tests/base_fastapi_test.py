import unittest
import subprocess
import time
import httpx


class BaseTest(unittest.TestCase):
    server_process = None
    server_host = "localhost"  # "127.0.0.1"
    server_port = 0  # 8000
    server_app = "your_fastapi_app:app"

    @classmethod
    def setUpClass(cls):
        # Check if the FastAPI server is already running
        try:
            response = httpx.get(f"http://{cls.server_host}:{cls.server_port}")
            if response.status_code == 200:
                print("FastAPI server is already running.")
                cls.server_process = None
                return
        except httpx.RequestError:
            pass

        # Start the FastAPI server
        cls.server_process = subprocess.Popen([
            "uvicorn",
            cls.server_app,
            "--host",
            cls.server_host,
            "--port",
            str(cls.server_port),
        ])
        time.sleep(5)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Terminate the FastAPI server if it was started by the test
        if cls.server_process:
            cls.server_process.terminate()
            cls.server_process.wait()
