'''Windows Console API with ctypes'''

import ctypes

class WindowsConsoleException(Exception):
    '''Error class for Windows Console Function errors'''

class Char(ctypes.Union):
    '''
    UTF-16 code unit representation of a character
    '''
    _fields_ = [('UnicodeChar', ctypes.c_wchar),
                ('AsciiChar', ctypes.c_char),
                ]

# Windows Console API Structures

class ConsoleCursorInfo(ctypes.Structure):
    '''
    Stores information about the console curser
    '''
    _fields_ = [('dwSize', ctypes.c_ulong),
                ('bVisible', ctypes.c_bool),
                ]

class CharInfo(ctypes.Structure):
    '''
    Specifies a Unicode or ANSI character and its attributes
    '''
    _fields_ = [('Char', Char),
                ('Attributes', ctypes.c_ushort),
                ]

class Coord(ctypes.Structure):
    '''
    Defines the coordinates of a character cell in a console screen buffer
    '''
    _fields_ = [('X', ctypes.c_short),
                ('Y', ctypes.c_short),
                ]

class SmallRect(ctypes.Structure):
    '''Defines the upper left and lower right coordinates of console'''
    _fields_ = [('Left', ctypes.c_short),
                ('Top', ctypes.c_short),
                ('Right', ctypes.c_short),
                ('Bottom', ctypes.c_short),
                ]

class ConsoleFontInfoex(ctypes.Structure):
    '''Contains extended information for a console font'''
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("nFont", ctypes.c_ulong),
        ("dwFontSize", Coord),
        ("FontFamily", ctypes.c_uint),
        ("FontWeight", ctypes.c_uint),
        ("FaceName", ctypes.c_wchar * 32)
    ]

# Windows Console API Functions

def set_console_title_w(console_title: ctypes.c_wchar) -> None:
    '''
    Sets the title of the console
    '''

    if not ctypes.windll.kernel32.SetConsoleTitleW(console_title):
        print('Error with SetConsoleTitleW')
        raise WindowsConsoleException()


def get_std_handle(std_handle: ctypes.c_ulong) -> int:
    '''
    Retrieves a standard output, standard input, or standarderror handle
    to the specified standard device
    '''
    return ctypes.windll.kernel32.GetStdHandle(std_handle)


def set_console_window_info(console_output: ctypes.c_void_p,
                            absolute: ctypes.c_bool,
                            console_window: SmallRect) -> None:
    '''
    Sets the current size and position of a console screen buffer's window.
    '''
    ctypes.windll.kernel32.SetConsoleWindowInfo(console_output, absolute,
                                                ctypes.byref(console_window))


def set_console_screen_buffer_size(console_output: ctypes.c_void_p, coord: Coord) -> None:
    '''
    Changes the buffer size of a specifed console
    '''
    if not ctypes.windll.kernel32.SetConsoleScreenBufferSize(console_output, coord):
        print('Error with SetConsoleScreenBufferSize')
        raise WindowsConsoleException()


def set_console_active_screen_buffer(console_output: ctypes.c_void_p) -> None:
    '''
    Sets the specified screen buffer to be the currently displayed console screen buffer
    '''
    if not ctypes.windll.kernel32.SetConsoleActiveScreenBuffer(console_output):
        print('Error with SetConsoleActiveScreenBuffer')
        raise WindowsConsoleException()


def set_current_console_fontex(console_output: ctypes.c_void_p, maximum_window: ctypes.c_bool,
                                console_current_fontex: ConsoleFontInfoex) -> None:
    '''
    Sets extended information for current console font
    '''
    if not ctypes.windll.kernel32.SetCurrentConsoleFontEx(console_output, maximum_window,
                                                            ctypes.byref(console_current_fontex)):
        print('Error with SetCurrentConsoleFontEx')
        raise WindowsConsoleException()


def write_console_output_w(console_output: ctypes.c_void_p, buffer: CharInfo,
                            buffer_size: Coord, buffer_coord: Coord,
                            write_region: SmallRect) -> None:
    '''
    Writes character and color attribute data to a specified rectangular
    structure of character cells in a console screen buffer
    '''
    ctypes.windll.kernel32.WriteConsoleOutputW(console_output, buffer, buffer_size,
                                                buffer_coord, ctypes.byref(write_region))
