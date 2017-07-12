##  evoware/py -- python modules for Evoware scripting
##   Copyright 2014 Raik Gruenberg
##
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##       http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.

"""TK / Windows user-notifications and dialog boxes"""

import tkinter
from tkinter import filedialog
from tkinter import messagebox
import sys, traceback, inspect
import os
import unittest

from . import fileutil as F

## create package-wide hidden window for unattached dialog boxes
root = tkinter.Tk()
root.withdraw()

class PyDialogError(Exception):
    pass

## see: http://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
def askForFile(defaultextension='*.csv', 
               filetypes=(('Comma-separated values (CSV)', '*.csv'),
                          ('Text file', '*.txt'),
                          ('All files', '*.*')), 
               initialdir='', 
               initialfile='', 
               multiple=False,
               newfile=False,
               title=None):
    """present simple Open File Dialog to user and return selected file."""
    options = dict(defaultextension=defaultextension, 
               filetypes=filetypes,
               initialdir=initialdir, 
               initialfile=initialfile, 
               multiple=multiple, 
               title=title)
    
    if not newfile:
        r = filedialog.askopenfilename(**options)
    else:
        del options['multiple']
        r = filedialog.asksaveasfilename(**options)
    return r



def info(title, message):
    """Display info dialog box to user"""
    messagebox.showinfo(title, message)

def warning(title, message):
    """Display warning dialog box to user"""
    messagebox.showwarning(title, message)

def error(title, message):
    """Display error dialog box to user"""
    messagebox.showerror(title, message)

def lastException(title=None):
    """Report last exception in a dialog box."""
    msg = __lastError()
    messagebox.showerror(title= title or 'Python Exception', message=msg)

def __lastError():
    """
    Collect type and line of last exception.
    
    @return: '<ExceptionType> raised in line <lineNumber>. Reason: <Exception arguments>'
    @rtype: String
    """
    error, value, trace = sys.exc_info()
    if not error:
        return ''

    file = inspect.getframeinfo( trace.tb_frame )[0]
    try:
        error = error.__name__
        file = os.path.basename(file)
    except:
        pass

    r = "%s\nraised in %s line %i.\n\nReason: %s." % ( str(error),
                                          file, trace.tb_lineno, str(value) )

    return r
