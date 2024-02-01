
import subprocess

# Comando para activar el entorno virtual (ajusta según tu sistema operativo)
activate_command = ".\\ENV\\Scripts\\activate"

# Comando para ejecutar el script sopa.py
script_command = ["python", "..\\sopa.py"]

# Combina ambos comandos en uno solo usando el operador "&" (Windows) o "&&" (Linux/Unix)
combined_command = f"{activate_command} & {' '.join(script_command)}"

# Ejecuta el comando combinado
subprocess.run(combined_command, shell=True)
