import subprocess
import sys


def test_import_time():
    """import xgi should complete in under 3 seconds."""
    result = subprocess.run(
        [sys.executable, "-X", "importtime", "-c", "import xgi"],
        capture_output=True,
        text=True,
    )
    # last line of importtime stderr: "import time: self | cumulative | xgi"
    last_line = result.stderr.strip().splitlines()[-1]
    cumulative_us = int(last_line.split("|")[1].strip())
    cumulative_s = cumulative_us / 1_000_000
    assert cumulative_s < 3, f"import xgi took {cumulative_s:.2f}s, expected < 3s"
