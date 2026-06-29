from pathlib import Path
import sys

from tui.app import App
from core.logger import set_logger, TUILogger

set_logger(TUILogger())


def main():

    if len(sys.argv) != 2:

        print()

        print("Uso:")

        print()

        print("    pdfvoice archivo.pdf")

        print()

        return

    app = App(

        Path(sys.argv[1])

    )

    app.run()


if __name__ == "__main__":

    main()
