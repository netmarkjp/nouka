========================
NOUKA data collector
========================

Overview
========================
NOUKA is client tool of inventory management system.

NOUKA enable ...

- AUTOMATIC update
- PERIODIC update

and NOUKA focus to Linux machines.

http://www.slideshare.net/toshiak_netmark/nouka-inventry-manager

Requirement
========================

client
-------
- python 2.4+

server
-------
- fluentd or td-agent
  http://fluentd.org/
- fluent-plugin-mongo
- fluent-plugin-http-enhanced
  https://github.com/parolkar/fluent-plugin-http-enhanced


shell::

 gem install fluent-plugin-http-enhanced


Install
========================

shell::

 hg clone ...(writing)


Server Configuration
========================

fleutd.conf::

 <source>
   type httpenhanced
   port 1981
   full_query_string_record true
   respond_with_empty_img false
   default_tag nouka
 </source>
 
 <match nouka.**>
     type mongo
     database nouka
     collection naya
     host localhost
     port 27017
     ignore_invalid_record true
     buffer_chunk_limit 128k
     flush_interval 1s
 </match>

Execution
========================
only execute `<NOUKA_HOME>/bin/nouka`

if you need help, 
execute `<NOUKA_HOME>/bin/nouka --help`

Data Format
========================

json::

 {
     'group_name'   : '<group_name's value in config file>',
     'host_name'    : '<env HOSTNAME>',
     'command_name' : '<command name in config file. named command_*>',
     'command_line' : '<command line(value) in config file>',
     'output'       : '<output of command line>',
     'return_code'  : '<return code of command line>',
     'visible'      : 'True',
     'execute_at'   : '<execute date as unixtime>',
 }

- unique key of the host is `group_name` and `host_name`.
- unique key of the command execution is `group_name` and `host_name` and `command_name` and `execute_at`.


Examples
========================
To get latest results of group_name=system_A

mongo::

 # step1. find latest result date
 > db.nengu.distinct('execute_at',{'group_name':'system_A'})
 [ "1339597836", "1339597926", "1339597944", "1339597953" ]

 # step2. get results
 > db.nengu.find({'group_name':'system_A','execute_at':'1339597953'})

Development
========================

shell::

 virtualenv --no-site-packages --python=python2.4 venv
 # or 
 /usr/local/Cellar/python24/2.4.*/bin/virtualenv --no-site-packages --python=python2.4 venv


See Also
========================
related project is yaoya data convertor https://bitbucket.org/netmarkjp/yaoya

Note
========================
If you use MacOSX, install python2.4 with homebrew.

shell::

 brew tap homebrew/versions
 brew install homebrew/versions/python24
 curl http://peak.telecommunity.com/dist/ez_setup.py|python2.4
 /usr/local/Cellar/python24/2.4.6/bin/easy_install pip
 /usr/local/Cellar/python24/2.4.6/bin/pip install virtualenv
 

