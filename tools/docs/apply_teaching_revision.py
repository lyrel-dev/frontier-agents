"""Apply the reviewed diagram correction once, then remove the migration."""
from pathlib import Path
import runpy
here=Path(__file__).resolve().parent
runpy.run_path(str(here/'polish_teaching_views.py'),run_name='__main__')
Path(__file__).unlink()
