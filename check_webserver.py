#!/usr/bin/python -tt
import sys
import os
import commands
#code we are checking
## Given a dir path, run an external 'ls -l' on it --
## shows how to call an external program

def checknginx():
  
  cmd = 'ps -Al | grep nginx | grep -v grep'
  (status, output) = commands.getstatusoutput(cmd)
  if status: 
    print "Nginx Server NOT  running"
    print "do you want to start nginx? (y/n)"
    name=raw_input(">").lower()
    if name == "y":
      cmd3 = "sudo yum -y service nginx start"
      (status, output) = commands.getstatusoutput(cmd2)
      if status: 
        print "Nginx Server NOT  running"
      else:
        print "Nginx Server IS running"
        print output
    else:
      sys.exit(1)
    print "Running"
  else:
    print "Nginx Server IS running"
  print output  ## Otherwise do something with the command's output
#main

def main():
    checknginx()
    

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()
