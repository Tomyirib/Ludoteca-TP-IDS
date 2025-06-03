import subprocess
from backend.iniciar_db import main

#a = subprocess.Popen(["python3", "backend/app.py"])

#b = subprocess.Popen(["python3", "frontend/app.py"])


try:
    main()
 #   a.wait()
    #b.wait()
except KeyboardInterrupt:
    print("Deteniendo servicios...")
  #  a.terminate()
    #b.terminate()