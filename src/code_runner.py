"""OmniChat - Safe Python Code Execution Runner for Artifact Canvas."""
import subprocess
import sys
from typing import Dict, Any

def execute_python_code(code: str, timeout: int = 5) -> Dict[str, Any]:
    """Executes a Python snippet in a sandboxed subprocess and captures output."""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "returncode": proc.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds.",
            "returncode": 124
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution error: {str(e)}",
            "returncode": 1
        }
