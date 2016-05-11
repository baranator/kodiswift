'''
    kodiswift
    ----------

    A micro framework to enable rapid development of Kodi plugins.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
'''
from types import ModuleType


class module(ModuleType):
    '''A wrapper class for a module used to override __getattr__. This class
    will behave normally for any existing module attributes. For any attributes
    which do not existi in in the wrapped module, a mock function will be
    returned. This function will also return itself enabling multiple mock
    function calls.
    '''

    def __init__(self, wrapped=None):
        self.wrapped = wrapped
        if wrapped:
            self.__dict__.update(wrapped.__dict__)

    def __getattr__(self, name):
        '''Returns any existing attr for the wrapped module or returns a mock
        function for anything else. Never raises an AttributeError.
        '''
        try:
            return getattr(self.wrapped, name)
        except AttributeError:
            def func(*args, **kwargs):
                '''A mock function which returns itself, enabling chainable
                function calls.
                '''
                log.warning('The %s method has not been implented on the CLI. '
                            'Your code might not work properly when calling '
                            'it.', name)
                return self
            return func


try:
    import xbmc
    import xbmcgui
    import xbmcplugin
    import xbmcaddon
    CLI_MODE = False
except ImportError:
    CLI_MODE = True

    import sys
    from logger import log

    # Mock the Kodi modules
    from mockxbmc import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
    xbmc = module(xbmc)
    xbmcgui = module(xbmcgui)
    xbmcplugin = module(xbmcplugin)
    xbmcaddon = module(xbmcaddon)
    xbmcvfs = module(xbmcvfs)


from kodiswift.storage import TimedStorage
from kodiswift.request import Request
from kodiswift.common import (xbmc_url, enum, clean_dict, pickle_dict,
    unpickle_args, unpickle_dict, download_page, unhex)
from kodiswift.constants import SortMethod, VIEW_MODES
from kodiswift.listitem import ListItem
from kodiswift.logger import setup_log
from kodiswift.module import Module
from kodiswift.urls import AmbiguousUrlException, NotFoundException, UrlRule
from kodiswift.xbmcmixin import XBMCMixin
from kodiswift.plugin import Plugin