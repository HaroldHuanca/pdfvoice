from core.project_manager import ProjectManager
from core.tts.manager import TTSManager

project = ProjectManager("TecnicasPromptFinalPDF.pdf").prepare()

tts = TTSManager(project.audio_dir)

tts.generate(project.chapters[0])

print()

print(project.chapters[0].audio_file)
