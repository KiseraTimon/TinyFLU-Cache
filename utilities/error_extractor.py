# utilities/error_extractor.py

import traceback

def extract_error_details(e: Exception) -> str:
    err_type = type(e).__name__
    err_msg = str(e)
    tb_list = traceback.extract_tb(e.__traceback__) if getattr(e, "__traceback__", None) else []

    filename, line_no = (tb_list[-1].filename, tb_list[-1].lineno) if tb_list else (None, None)

    return (
        f"ERROR TYPE:\n{err_type}\n\n"
        f"ERROR MESSAGE:\n{err_msg if err_msg else 'None'}\n\n"
        f"ERROR ORIGIN:\n{filename}\n\n"
        f"ERROR LINE:\n{line_no}"
    )