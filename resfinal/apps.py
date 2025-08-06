from django.apps import AppConfig
import threading
import time
import subprocess
import os
from django.conf import settings

def run_exe_files_every_30s():
    exe_dir = os.path.join(settings.BASE_DIR, 'bin')
    output_dir = os.path.join(settings.BASE_DIR, 'csv_outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    exe_files = [
        'temperature_sensor.exe',
        'sound_sensor.exe',
        'pressure_sensor.exe',
        'smoke_sensor.exe',
        'motion_sensor.exe'
    ]

    while True:
        for exe in exe_files:
            exe_path = os.path.join(exe_dir, exe)
            output_file = os.path.join(output_dir, exe.replace('.exe', '.csv'))

            try:
                with open(output_file, 'w') as csv_file:
                    subprocess.run([exe_path], stdout=csv_file, stderr=subprocess.PIPE, cwd=exe_dir, check=True)
                print(f"{exe} ran successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error running {exe}: {e}")
        time.sleep(30)  # wait before running the next batch

class ResfinalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resfinal'

    def ready(self):
        import resfinal.signal  # keep your existing signal import
        threading.Thread(target=run_exe_files_every_30s, daemon=True).start()  # run exe task

