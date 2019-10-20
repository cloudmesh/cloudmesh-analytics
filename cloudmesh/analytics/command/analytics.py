from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.analytics.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE

class AnalyticsCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_analytics(self, args, arguments):
        """
        ::

          Usage:
                analytics server start [--cloud=CLOUD]
                analytics server stop [--cloud=CLOUD]

          This command manages the cloudmesh analytics server on the given cloud.
          If the cloud is not spified it is run on localhost

          Options:
              --clout=CLOUD  The name of the cloud as specified in the
                             cloudmesh.yaml file

        """

        VERBOSE(arguments)

        Console.error("This is just a sample")

        if arguments.server and arguments.start:
            print("start the server")

        if arguments.server and arguments.stop:
            print("stop the server")

        return ""
