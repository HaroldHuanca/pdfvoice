from core.project_manager import ProjectManager
from core.tts.manager import TTSManager
from player.mpv_player import MPVPlayer

project = ProjectManager("TecnicasPromptFinalPDF.pdf").prepare()

tts = TTSManager(project.audio_dir)

audio = tts.generate(project.chapters[0])

player = MPVPlayer()

player.play(audio)

input("\nENTER para cerrar...")

player.quit()
