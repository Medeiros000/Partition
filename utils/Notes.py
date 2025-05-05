import os
import datetime


class Notes:

  date = datetime.date.today()
  date_hour = datetime.datetime.now()
  directory = ''

  def __init__(self, directory: str = "files", response: bool = False) -> None | bool:
    """
    Initializes a new instance of the Notes class.

    Args:
      directory (str): The directory in which to store notes. Default is 'files'.
      response (bool): If True, returns a boolean indicating success.
    """
    self.directory = directory
    self.name = "Notes"
    # Ensure the directory exists
    try:
      os.makedirs(self.directory, exist_ok=True)
      return True if response else None
    except Exception as e:
      return False if response else None

  def write_note(self, name: str, content, type='txt', date=True) -> None:
    """
    Writes a note to a file in the specified directory.

    Args:
      name (str): The name of the note file.
      content (str): The content that will be written to the file.
      type (str): The file type of the note. Default is 'txt'.
      date (bool): If True, includes the current date in the note.
    """
    filename = os.path.join(self.directory, f"{name}_{self.date}.{type}")
    with open(filename, "a", encoding="utf8") as file:
      content_date = f"[{str(self.date_hour.strftime('%Y-%m-%d %H:%M:%S'))}]: " if date else ""
      file.write(content_date + str(content) + "\n")

  def read_note(self, name, type='txt') -> str:
    """
    Reads a note from a file in the specified directory.

    Args:
      name (str): The name of the note file.
      type (str): The file type of the note. Default is 'txt'.

    Returns:
      str: The content of the note.
    """
    filename = os.path.join(self.directory, f"{name}_{self.date}.{type}")
    with open(filename, 'r') as file:
      return file.read()
