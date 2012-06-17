#!/usr/bin/env python
#coding: utf-8

from ConfigParser import ConfigParser

class Main(object):

    config = ConfigParser()
    host_name = None

    def __init__(self, config_file, host_name):
        self.config.read(config_file)
        self.host_name=host_name

    def run(self):
        results = []

        # execute
        import re
        import time
        from subprocess import Popen, PIPE, STDOUT
        command_pattern = re.compile(r'^command_.*')
        execute_at = int(time.time())
        for k,v in self.config.items('agent'):
            if command_pattern.match(k):
                command = {'command_name':k, 'command_line':v}
                try:
                    process = Popen(v, shell = True, 
                        stdin = PIPE, stdout = PIPE, stderr = STDOUT,
                        close_fds = True)
                    (stdouterr, stdin) = (process.stdout, process.stdin)
                    output=''
                    while True:
                        line = stdouterr.readline()
                        if not line:
                            break
                        output = output + line
                    process.communicate()
                    command['output'] = output
                    command['return_code'] = process.returncode
                except:
                    # TODO: logging and error handling
                    pass
                results.append(command)

        # send result
        import urllib
        import urllib2
        project_name = self.config.get('agent','group_name')
        server_url = self.config.get('server','server_url')
        host_name = self.host_name
        for result in results:
            result['group_name'] = project_name
            result['visible'] = 'True'
            result['execute_at'] = execute_at
            result['host_name'] = host_name
            try:
                query = urllib.urlencode(result)
                response = urllib2.urlopen(server_url,query)
                # TODO: logging and output handling
            except:
                # TODO: logging and error handling
                pass

