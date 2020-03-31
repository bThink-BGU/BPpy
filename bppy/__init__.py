from os import listdir
from os.path import dirname, basename, isfile, join, isdir

# TODO: find a smarter way to import al submodules
from bppy.execution.listeners.b_program_runner_listener import *
from bppy.execution.listeners.print_b_program_runner_listener import *
from bppy.model.event_selection.event_selection_strategy import *
from bppy.model.event_selection.experimental_smt_event_selection_strategy import *
from bppy.model.event_selection.simple_event_selection_strategy import *
from bppy.model.event_selection.smt_event_selection_strategy import *
from bppy.model.b_event import *
from bppy.model.bprogram import *
from bppy.model.event_set import *
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
from bppy.utils.z3helper import *

# def getListOfFiles(dirName):
#     # create a list of file and sub directories
#     # names in the given directory
#     listOfFile = listdir(dirName)
#     allFiles = list()
#     # Iterate over all the entries
#     for entry in listOfFile:
#         # Create full path
#         fullPath = join(dirName, entry)
#         # If entry is a directory then get the list of files in this directory
#         if isdir(fullPath):
#             allFiles = allFiles + getListOfFiles(fullPath)
#         else:
#             print(fullPath)
#             allFiles.append(fullPath)
#     return allFiles
#
# print([ basename(f)[:-3] for f in getListOfFiles(dirname(__file__)) if f[-3:] == ".py" and not f.endswith('__init__.py')])
# __all__ = [ basename(f)[:-3] for f in getListOfFiles(dirname(__file__)) if f[-3:] == ".py" and not f.endswith('__init__.py')]
#__all__ = ["examples", "execution", "model", "utils"]