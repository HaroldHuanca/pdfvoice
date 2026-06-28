from pathlib import Path
import time

from player.mpv_player import MPVPlayer

# --------------------------------------------------

# Cambia esta ruta por cualquier WAV que tengas

AUDIO = Path(
    "/home/HaroldUser/PDFVoice/cache/8bd798f92f50d4a16cdea4ad9bef8cf7b7be67ca9f51317639fd291a8ee97216/audio/001/final.wav"
)

# --------------------------------------------------

player = MPVPlayer()

try:

    print("\n========== INICIANDO ==========\n")

    player.start()

    print(player.status())

    print("\n========== PLAY ==========\n")

    player.play(AUDIO)

    time.sleep(2)

    print(player.status())

    print("\n========== PAUSE ==========\n")

    player.pause()

    time.sleep(2)

    print(player.status())

    print("\n========== RESUME ==========\n")

    player.resume()

    time.sleep(2)

    print(player.status())

    print("\n========== SPEED 1.5 ==========\n")

    player.speed(1.5)

    time.sleep(3)

    print(player.status())

    print("\n========== SEEK +10 ==========\n")

    player.seek(10)

    time.sleep(2)

    print(player.status())

    print("\n========== SEEK -5 ==========\n")

    player.seek(-5)

    time.sleep(2)

    print(player.status())

    print("\n========== VOLUME ==========\n")

    player.volume(40)

    time.sleep(2)

    print(player.status())

    print("\n========== POSITION ==========\n")

    print(player.position())

    print("\n========== DURATION ==========\n")

    print(player.duration())

    print("\n========== REMAINING ==========\n")

    print(player.remaining())

    print("\n========== WAIT ==========\n")

    player.wait_until_finished()

    print(player.status())

finally:

    print("\n========== QUIT ==========\n")

    player.quit()
