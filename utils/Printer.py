class Printer:
  def __init__(self):
    """
    Initializes a new instance of the Printer class.
    """
    self.name = "Printer"

  def print_red(self, text: str) -> None:
    """
    Prints text in red color.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[31m{text}\033[0m")

  def print_green(self, text: str) -> None:
    """
    Prints text in green color.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[32m{text}\033[0m")

  def print_yellow(self, text: str) -> None:
    """
    Prints text in yellow color.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[33m{text}\033[0m")

  def print_blue(self, text: str) -> None:
    """
    Prints text in blue color.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[34m{text}\033[0m")

  def print_reset(self, text: str) -> None:
    """
    Prints text with default color.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[0m{text}\033[0m")

  def print_bold(self, text: str) -> None:
    """
    Prints text in bold.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[1m{text}\033[0m")

  def print_underline(self, text: str) -> None:
    """
    Prints text with underline.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[4m{text}\033[0m")

  def print_blink(self, text: str) -> None:
    """
    Prints text with blink effect.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[5m{text}\033[0m")

  def print_reverse(self, text: str) -> None:
    """
    Prints text with reverse color.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[7m{text}\033[0m")

  def print_invisible(self, text: str) -> None:
    """
    Prints invisible text.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[8m{text}\033[0m")

  def print_black(self, text: str) -> None:
    """
    Prints text in black color.

    Args:
      text (str): The text to be printed.
    """
    print(f"\033[30m{text}\033[0m")
