import sys
import traceback


def error_message_details(error, error_detail: sys):
    """
    Creates a detailed error message including:
    - Python error message
    - File name where error occurred
    - Line number of error
    """

    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"\nError occurred in python script: [{file_name}] \n"
        f"Line number: [{line_number}] \n"
        f"Error message: [{error}]"
    )

    return error_message


class Heart(Exception):
    """
    Custom exception class for the Network Security project.
    It formats the exception with filename, line number, and message.
    """

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_details(
            error_message, error_detail
        )

    def __str__(self):
        return self.error_message
