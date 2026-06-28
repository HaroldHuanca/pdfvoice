"""
main.py

CLI de PDFVoice.
"""

from __future__ import annotations

import sys

from pathlib import Path

from controller import PDFController


def help():

    print()

    print("Comandos disponibles")

    print("------------------------------")

    print("play [n]")

    print("pause")

    print("resume")

    print("stop")

    print("next")

    print("prev")

    print("seek SEGUNDOS")

    print("speed VALOR")

    print("volume VALOR")

    print("list")

    print("status")

    print("generate N")

    print("generate-all")

    print("quit")

    print()


def main():

    if len(sys.argv) != 2:

        print()

        print("Uso:")

        print()

        print("    pdfvoice archivo.pdf")

        return

    pdf = Path(sys.argv[1])

    if not pdf.exists():

        print("No existe el PDF.")

        return

    controller = PDFController(pdf)

    controller.list()

    print()

    print("Escriba 'help' para ver los comandos.")

    while True:

        try:

            cmd = input("> ").strip()

        except (KeyboardInterrupt, EOFError):

            break

        if not cmd:

            continue

        parts = cmd.split()

        command = parts[0].lower()

        try:

            if command == "help":

                help()

            elif command == "play":

                if len(parts) == 1:

                    controller.play()

                else:

                    controller.play(int(parts[1]))

            elif command == "pause":

                controller.pause()

            elif command == "resume":

                controller.resume()

            elif command == "stop":

                controller.stop()

            elif command == "next":

                controller.next()

            elif command == "prev":

                controller.previous()

            elif command == "speed":

                controller.speed(parts[1])

            elif command == "volume":

                controller.volume(parts[1])

            elif command == "seek":

                controller.seek(parts[1])

            elif command == "generate":

                controller.generate(int(parts[1]))

            elif command == "generate-all":

                controller.generate_all()

            elif command == "list":

                controller.list()

            elif command == "status":

                controller.status()

            elif command in ("quit", "exit", "q"):

                break

            else:

                print("Comando desconocido.")

        except Exception as e:

            print()

            print("ERROR:")

            print(e)

            print()

    controller.close()


if __name__ == "__main__":

    main()
