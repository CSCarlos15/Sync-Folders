In order to run the program from console you must go to directory (cd {Path}) where main.py file is and use the follow command
  python main.py --log_file {log file name} --interval {optional, default=10 seconds} {source path} {replica path}
Example  python main.py --log_file logs.txt --interval 5 C:\User\Source C:\User\Replica

If you have an already existing log file created inside the same directory as main.py, it will write logs in it.
If there isn't any txt file there, it will create one with the name you gave to it.
