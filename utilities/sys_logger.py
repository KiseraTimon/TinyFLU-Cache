# utilities/sys_logger.py

from pathlib import Path
from .log_config import get_sys_logger, write_to_file
from .time_utils import timestp

def log_system_info(msg: str, log: str = "general", path: str = None):
    logger = get_sys_logger()
    header = f"SYSTEM INFORMATION @ {timestp()}. CHECK *{log.upper()}*"
    logger.info(header)

    base_folder = Path("logs") / "system"
    folder = base_folder / path if path else base_folder

    formatted_entry = f"TIME: {timestp()}\nMESSAGE:\n---\n{msg}\n---\n"
    write_to_file(folder, log, formatted_entry)