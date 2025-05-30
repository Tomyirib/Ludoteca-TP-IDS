import subprocess

a = subprocess.Popen(["python3", "backend/app.py"])

b = subprocess.Popen(["python3", "frontend/app.py"])

try:
    a.wait()
    b.wait()
except KeyboardInterrupt:
    print("Deteniendo servicios...")
    a.terminate()
    b.terminate()