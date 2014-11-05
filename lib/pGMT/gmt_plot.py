import subprocess
import warnings
import os
import shutil

from .gmt import GMT
from .gmt_plot_command_names import GMT_COMMANDS
from .gmt import _form_gmt_escape_shell_command

__all__ = ['GMTPlot']

def _check_command_name(command):
    assert command in GMT_COMMANDS, \
           'Command name %s is not a valid GMT command.'%command

def _check_command_finalized(command):
    if 'K' in command[2]:
        warnings.warn(
            'There is -K option in the command %s. Plot is not finilized.'%\
            command[0])

def _check_command_has_overlay(command):
    if 'O' not in command[2]:
        warnings.warn(
            "Command %s don't have overlay option (-O)."%\
            command[0])

def _check_command_history_finalized(command_history):
    _check_command_finalized(command_history[-1])

def _check_command_history_K_option(command_history):
    for cmd in command_history[:-1]:
        if 'K' not in cmd[2]:
            warnings.warn(
                "Command %s don't have continue option (-K)."%\
            cmd[0])
            
def _check_command_history_overlay(command_history):
    for cmd in command_history[1:]:
            _check_command_has_overlay(cmd)

def _assert_file_name_extension(fn, ext):
    fn, ext_ = os.path.splitext(fn)
    assert ext_ == ext, '%s == %'%(ext_, ext)
    
class GMTPlot(GMT):
    ''' Wrapper of GMT.
'''
    def __init__(self, config=None):
        super().__init__()
        self._command_history = []

    def __getattr__(self, command):
        def f(*args, **kwargs):
            return self._gmtcommand(command, *args, **kwargs)
        return f

    def _gmtcommand(self, command, 
                          *args,
                          **kwargs):
        _check_command_name(command)
        super()._gmtcommand(command, *args, **kwargs)
        self._command_history.append((command, args, kwargs))

    def _check_commands_validity(self):
        _check_command_history_K_option(self._command_history)
        _check_command_history_finalized(self._command_history)
        _check_command_history_overlay(self._command_history)

    def save(self, filename):
        fn, ext = os.path.splitext(filename)
        if ext == '.ps':
            self.save_ps(filename)
        elif ext == '.pdf':
            self.save_pdf(filename)
        else:
            raise NotImplementedError()

    def save_ps(self, filename):
        self._check_commands_validity()
        _assert_file_name_extension(filename, '.ps')
        self.save_stdout(filename)

    def save_pdf(self, filename, **kwargs):
        _assert_file_name_extension(filename, '.pdf')
        self.save_ps(filename[:-3]+'ps')
        gmt = GMT()
        gmt.ps2raster(filename[:-3]+'ps', T='f', **kwargs)

    def save_shell_script(self, filename, output_file=None):
        if output_file is None:
            output_file = ''
        self._check_commands_validity()
        with open(filename,'wt') as fid:
            fid.write('#!/bin/bash\n')
            for cmd in self._command_history:
                args = _form_gmt_escape_shell_command(cmd[0], cmd[1], cmd[2])
                print(' '.join(args) + output_file, file=fid)
                
            
            
    
