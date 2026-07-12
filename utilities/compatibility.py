# utilities/compatibility.py

from .time_utils import timestp as stamp
from .error_extractor import extract_error_details
from .sys_logger import log_system_info
from .error_handler import log_critical_error
from .log_config import get_sys_logger

# Legacy Wrappers
def message(text): get_sys_logger().info(text)
def timestp(): return stamp()
def error(e): return extract_error_details(e)
def errhandler(e, log, **k): return log_critical_error(e, log, k.get("path"))
def syshandler(m, log, **k): return log_system_info(m, log, k.get("path"))