# utilities/error_handler.py

from pathlib import Path
from .log_config import get_error_logger, write_to_file
from .time_utils import timestp
from .error_extractor import extract_error_details

def log_critical_error(e: Exception, log: str = "critical", path: str = None):
    logger = get_error_logger()
    header = f"CRITICAL ERROR @ {timestp()}. CHECK *{log.upper()}*"
    logger.error(header)

    details = extract_error_details(e)
    base_folder = Path("logs") / "errors"
    folder = base_folder / path if path else base_folder

    formatted_entry = f"TIME: {timestp()}\n{details}\n"
    write_to_file(folder, log, formatted_entry, is_error=True)