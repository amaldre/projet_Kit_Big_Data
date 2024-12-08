import subprocess
import sys

python_executable = sys.executable

subprocess.run([python_executable, "-m", "streamlit", "run", "src/MangeTaData.py", "--server.fileWatcherType", "none"])
