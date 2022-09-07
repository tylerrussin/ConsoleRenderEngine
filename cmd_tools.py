'''Using ctypes to run C functions changing font in command line'''

import sys
import ctypes
import ctypes.wintypes


LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11

class COORD(ctypes.Structure):
    '''C structure for coordinate information'''
    _fields_ = [
        ("X", ctypes.wintypes.SHORT),
        ("Y", ctypes.wintypes.SHORT),
    ]

class CONSOLE_FONT_INFO_EX(ctypes.Structure):
    '''C structure for font information'''
    _fields_ = [
        ("cbSize", ctypes.wintypes.ULONG),
        ("nFont", ctypes.wintypes.DWORD),
        ("dwFontSize", COORD),
        ("FontFamily", ctypes.wintypes.UINT),
        ("FontWeight", ctypes.wintypes.UINT),
        ("FaceName", ctypes.wintypes.WCHAR * LF_FACESIZE)
    ]

def cmd_font(font_size=16):
    ''' Using python's ctypes to change the font size of the command prompt'''

    kernel32_dll = ctypes.WinDLL("kernel32.dll")

    get_last_error = kernel32_dll.GetLastError
    get_last_error.argtypes = []
    get_last_error.restype = ctypes.wintypes.DWORD

    get_std_handle = kernel32_dll.GetStdHandle
    get_std_handle.argtypes = [ctypes.wintypes.DWORD]
    get_std_handle.restype = ctypes.wintypes.HANDLE

    get_current_console_font_ex = kernel32_dll.GetCurrentConsoleFontEx
    get_current_console_font_ex.argtypes = [ctypes.wintypes.HANDLE,
                                            ctypes.wintypes.BOOL,
                                            ctypes.POINTER(CONSOLE_FONT_INFO_EX)]
    get_current_console_font_ex.restype = ctypes.wintypes.BOOL

    set_current_console_font_ex = kernel32_dll.SetCurrentConsoleFontEx
    set_current_console_font_ex.argtypes = [ctypes.wintypes.HANDLE,
                                            ctypes.wintypes.BOOL,
                                            ctypes.POINTER(CONSOLE_FONT_INFO_EX)]
    set_current_console_font_ex.restype = ctypes.wintypes.BOOL

    # Get stdout handle
    stdout = get_std_handle(STD_OUTPUT_HANDLE)
    if not stdout:
        print(f"{get_std_handle.__name__} error: {get_last_error()}")
        return

    # Get current font characteristics
    font = CONSOLE_FONT_INFO_EX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFO_EX)

    if not get_current_console_font_ex(stdout, 0, font):
        print(f"{get_current_console_font_ex.__name__} error: {get_last_error()}")
        return

    font.dwFontSize.Y = font_size

    # Apply changes
    if not set_current_console_font_ex(stdout, 0, font):
        print(f"{set_current_console_font_ex.__name__} error: {get_last_error()}")
        return


if __name__ == "__main__":
    print(f"Python {sys.version} on {sys.platform}\n")
    cmd_font(16)
