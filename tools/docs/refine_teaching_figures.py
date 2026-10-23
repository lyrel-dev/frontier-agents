from pathlib import Path
p=Path(__file__).resolve().parent/'teaching_diagrams.py'
s=p.read_text().replace('Configured review or issue destination','Review or issue')
p.write_text(s)
Path(__file__).unlink()
