import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Run .exe files to generate CSV"

    def handle(self, *args, **kwargs):
        exe_dir = os.path.join(settings.BASE_DIR, 'bin')
        output_dir = os.path.join(settings.BASE_DIR, 'csv_outputs')  # Ensure this is correct
        
        os.makedirs(output_dir, exist_ok=True)

        exe_files = ['temperature_sensor.exe', 'sound_sensor.exe','pressure_sensor.exe','smoke_sensor.exe','motion_sensor.exe']

        for exe in exe_files:
            exe_path = os.path.join(exe_dir, exe)
            output_file = os.path.join(output_dir, exe.replace('.exe', '.csv'))  # CSV file name based on the exe

            try:
                # Ensure the exe runs in the correct directory, using 'cwd' argument in subprocess.run()
                with open(output_file, 'w') as csv_file:
                    result = subprocess.run([exe_path], stdout=csv_file, stderr=subprocess.PIPE, cwd=exe_dir, check=True)
                    
                self.stdout.write(self.style.SUCCESS(f"Executed {exe} successfully and created {output_file}"))
            except subprocess.CalledProcessError as e:
                self.stderr.write(self.style.ERROR(f"Error executing {exe}: {e}"))
