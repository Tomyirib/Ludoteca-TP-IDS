import sys
sys.path.append('./backend')
import subprocess
from backend.iniciar_db import init_db

a = subprocess.Popen(["python3", "backend/app.py"])

b = subprocess.Popen(["python3", "frontend/app.py"])


try:
    #init_db()
    a.wait()
    b.wait()
except KeyboardInterrupt:
    print("Deteniendo servicios...")
    a.terminate()
    b.terminate()