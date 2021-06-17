# -*- encoding: utf-8 -*-
"""
KERI
keri.app.cli module

command line utility support
"""

import multicommand
from hio import help
from hio.base import doing
from hio.core.serial import serialing

from . import commands
from .. import habbing, keeping
from ...db import basing

logger = help.ogler.getLogger()


class Consoling(doing.DoDoer):
    """
    Manages command console
    """

    def __init__(self, name: str, doers=None, console=None, **kwa):
        """

        """
        self.always = True
        self.console = console if console is not None else serialing.Console()
        self.console.reopen()
        self.parser = multicommand.create_parser(commands)
        self.name = name

        db = basing.Baser(name=name, temp=False)
        ks = keeping.Keeper(name=name, temp=False)
        self.hab = habbing.Habitat(name=name, temp=False)

        self.doers = doers if doers is not None else [self.parserDo]
        self.doers.extend([basing.BaserDoer(baser=db),
                           keeping.KeeperDoer(keeper=ks),
                           self.parserDo])

        super(Consoling, self).__init__(doers=self.doers, **kwa)
        self.displayPrompt()

    @doing.doize()
    def parserDo(self, tymth=None, tock=0.0, **opts):
        """
         Returns Doist compatible generator method (doer dog) to process
            command input

        Doist Injected Attributes:
            g.tock = tock  # default tock attributes
            g.done = None  # default done state
            g.opts

        Parameters:
            tymth is injected function wrapper closure returned by .tymen() of
                Tymist instance. Calling tymth() returns associated Tymist .tyme.
            tock is injected initial tock value
            opts is dict of injected optional additional parameters

        Usage:
            add to doers list
        """
        while True:
            line = self.console.get().decode('utf-8')  # process one line of input
            if not line:
                continue

            chunks = line.lower().split()
            self.displayPrompt()

            if not chunks:  # empty list
                continue

            args = self.parser.parse_args(chunks)

            if hasattr(args, "handler"):
                setattr(args, "hab", self.hab)
                print(args)
                self.extend(doers=[args.handler(args)])
                continue

            self.displayPrompt()
            yield

    def displayPrompt(self):
        self.console.put(f'{self.name}: '.encode('utf-8'))

    def send(self, s):
        self.console.put(s.encode('-utf-8'))
        # self.displayPrompt()
