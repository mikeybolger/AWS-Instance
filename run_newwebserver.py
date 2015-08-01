#!/usr/bin/python -tt

import commands
import boto.ec2
import time
import sys
import logging

#Create a log file that stores instance debug information
logging.basicConfig(filename="ec2.log", level=logging.DEBUG)

#User keys
#my_key chosen during aws signup
#my_tag Tag name to identify owners instance on aws
#my_instance an array to store instance information
my_key = 'StudentA1'
my_tag = 'TX_MIKEBOLGER'
my_instance = []

def main():
  menu()

def menu():
  print
  print"+++++++++++++++++++++++++++++++++++++++++++++"
  print"+---------------- Main Menu ----------------+"
  print"+++++++++++++++++++++++++++++++++++++++++++++"
  print
  print "1.) Launch new AWS Instance"
  print
  print"---------------------------------------------"
  print"---------When instance is running------------"
  print"---------------------------------------------"
  print
  print "2.) Install and Run nginx"
  print
  print "3.) SCP program to nginx"
  print
  print "4.) Make copied program executable"
  print
  print "5.) Set iptable rules"
  print
  print "6.) Terminate instance"
  print
  print"---------------------------------------------"
  print"---------Check Instance and nginx------------"
  print"---------------------------------------------"
  print
  print "7.) Check Connection "
  print
  print "8.) check copied program is executable"
  print
  print "9.) View iptables"
  print 
  print "--------------------------------------------"
  print "10.) Exit"
  print

  choice = raw_input('Enter your choice [1-10] : ')

  choice = int(choice)

  if choice == 1:
        print ("Creating Instance...")
	create_instance()
  elif choice == 2:
        print ("Installing nginx...")
        install_nginx()
  elif choice == 3:
        print ("Checking nginx...")
        scp_nginx()
  elif choice == 4:
        print ("Checking nginx...")
        ex_nginx()
  elif choice == 5:
        print ("Setting iptable rules...")
        set_iptables()
  elif choice == 6:
        print ("Delete instance...")
        del_instance()
  elif choice == 7:
        print ("Checking Connection to Webserver Through ssh...")
	check_connection()
  elif choice == 8:
        print ("Checking if program is executable...")
        check_prog()  
  elif choice == 9:
        print ("Checking iptable rules...")
        view_iptables()   
  elif choice == 10:
        print ("Exiting...")
        sys.exit(0)
  else:    ## default ##
        print ("Invalid number. Try again...")
  return menu()

#Create an amazon ec2 instance designate region to connect to
def create_instance(): 
  conn = boto.ec2.connect_to_region("eu-west-1")
  print 'Opening connection... '

#Specify instance type, keys and user group.
  reservation = conn.run_instances    ('ami-6e7bd919',key_name=my_key,instance_type='t2.micro',security_groups=  ['witsshrdp'])

  instance = reservation.instances[0]

#Place created instance into my_instance array
  my_instance.insert(0, instance)
  instance.add_tag('Name', my_tag)


#When instance state does not = running sleep for 5 seconds and the retry, loops until instance is running
  print 'Trying to create instance... '
  while instance.state != 'running':
    time.sleep(5)
    instance.update()
    print 'Creating instance please wait... '
  
  print 'Instance ' + instance.id + ' now running...'
  print 'The public DNS name is ' + instance.public_dns_name
  time.sleep(5)

  menu()

#Use secure shell (SSH) to remotely install and start nginx on the server, print output success, failure status
def install_nginx():
  cmd1 = "ssh -t -o StrictHostKeyChecking=no -i " + my_key + ".pem ec2-user@" + my_instance[0].public_dns_name + " 'sudo yum -y install nginx'"

  print cmd1  # displaying command for debug purposes
  (status, output) = commands.getstatusoutput(cmd1)
  while (status):
    print "Attempting to install nginx please wait....."
    time.sleep(30)
    (status, output) = commands.getstatusoutput(cmd1)
  if status:    ## Error case, print the command's output to stderr and exit
    sys.stderr.write(output)
    print "cmd2 Failed to install nginx...."
    time.sleep(5)
    sys.exit(1)
  if status:
    print "Trying to start webserver"
    (status2, output2) =commands.getoutput(cmd1)
    print "Status: ", status2
    print "Output: ", output2
  else:
    print output  ## Otherwise print the command's output
    print "nginx has been sucessfully installed"
    time.sleep(5)

#Use secure shell (SSH) to start nginx service on the amazon AMI print output success, failure status
  cmd2 = "ssh -t -o StrictHostKeyChecking=no -i " + my_key + ".pem ec2-user@" + my_instance[0].public_dns_name + " 'sudo service nginx start'"

  print cmd2  # displaying command for debug purposes
  (status, output) = commands.getstatusoutput(cmd2)
  while (status):
    print "cmd2 Attempting to start nginx please wait....."
    time.sleep(30)
    (status, output) = commands.getstatusoutput(cmd2)
  if status:    ## Error case, print the command's output to stderr
    sys.stderr.write(output)
    print "cmd2 Failed to start nginx...."
    time.sleep(5)
    sys.exit(1)
  else:
    print output  ## Otherwise print the command's output
    print "nginx has been sucessfully started or is already running"
    time.sleep(5)
  menu()

#Secure copy (SCP) local file onto the server using the scp command, print output success, failure
def scp_nginx():
  cmd3 = "scp -i " + my_key + ".pem check_webserver.py ec2-user@" + my_instance[0].public_dns_name + ":."

  print cmd3
  (status, output) = commands.getstatusoutput(cmd3)
  if status:    ## Error case, print the command's output to stderr and exit
    sys.stderr.write(output)
    print "SCP failed"
  else:
    print output  ## Otherwise print the command's output
    print "SCP success file has been copied"
    time.sleep(5)
  menu()

#Make the copied file executable on the webserver with the chmod 700 command followed by the name of the file to be made executable
def ex_nginx():
  cmd4 = "ssh -i " + my_key + ".pem ec2-user@" + my_instance[0].public_dns_name + " 'chmod 700 check_webserver.py'"

  print cmd4
  (status, output) = commands.getstatusoutput(cmd4)
  if status:    ## Error case, print the command's output to stderr and exit
    sys.stderr.write(output)
    print "SSH failed"
  else:
    print output  ## Otherwise print the command's output
    print "SSH success file is now executable"
    time.sleep(5)
  menu()

#Remotely set iptable rules for instance through secure shell (SSH)
def set_iptables():
  
#Set iptable rules for instance
#Accept incomming and outgoing (ICMP) ping messages
  cmd5 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A INPUT -p icmp -j ACCEPT"
  cmd6 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A OUTPUT -p icmp -j ACCEPT"
#Accept incomming port 22 ssh traffic
  cmd7 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT"
#Enable Incomming and outgoing port 53 for DNS
  cmd8 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A OUTPUT -p udp --dport 53 -j ACCEPT"
  cmd9 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A INPUT -p udp --sport 53 -j ACCEPT"
#Enable Incomming and outgoing port 53 HTTP protocol
  cmd10 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT"
  cmd11 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A INPUT -p tcp --sport 80 -j ACCEPT"
#Enable Incomming and outgoing port 443 Hypertext Transfer Protocol over TLS/SSL (HTTPS)
  cmd12 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT"
  cmd13 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A INPUT -p tcp --sport 443 -j ACCEPT"
#Enable local host
  cmd14 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A INPUT -s 127.0.0.1 -j ACCEPT"
  cmd15 = "ssh -t -i " + "'" + my_key + ".pem'" +" ec2-user@" + my_instance[0].public_dns_name + " sudo iptables -A OUTPUT -d 127.0.0.1 -j ACCEPT"
  time.sleep(5)
  
  print cmd5
  (status, output) = commands.getstatusoutput(cmd5)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd6
  (status, output) = commands.getstatusoutput(cmd6)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd7
  (status, output) = commands.getstatusoutput(cmd7)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd8
  (status, output) = commands.getstatusoutput(cmd8)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd9
  (status, output) = commands.getstatusoutput(cmd9)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd10
  (status, output) = commands.getstatusoutput(cmd10)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd11
  (status, output) = commands.getstatusoutput(cmd11)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd12
  (status, output) = commands.getstatusoutput(cmd12)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd13
  (status, output) = commands.getstatusoutput(cmd13)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd14
  (status, output) = commands.getstatusoutput(cmd14)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."

  print cmd15
  (status, output) = commands.getstatusoutput(cmd15)
  if status:    ## Error case, print the command's output to stderr 
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."
  menu()

#Prompt the user to delete the instance yes or no
def del_instance():
  ans = raw_input("\nWould you like to terminate the instance? (Y/N)")
  if ans == "y" or ans == "Y" or ans == "Yes" or ans == "YES" or ans == "yes":
    my_instance[0].terminate()
    del my_instance[:]
    print 'Instance terminated'
  else:
    print 'Instance not terminated returnin to main menu'

#Check that the program has become executable following command 5
def check_prog():
  cmd16 = "ssh -t -i " + my_key + ".pem ec2-user@" + my_instance[0].public_dns_name + " 'sudo python check_webserver.py'"

  print cmd16
  (status, output) = commands.getstatusoutput(cmd16)
  if status:    ## Error case, print the command's output to stderr and exit
    sys.stderr.write(output)
    print "Failure...Unable to execute file"
  else:
    print output  ## Otherwise print the command's output
    print "Success...File is now executable"
    time.sleep(5)
  menu()

#Check the connection to AWS instance and print output status
def check_connection(): 
  cmd17 = "ssh -o StrictHostKeyChecking=no -i " + my_key + ".pem ec2-user@" + my_instance[0].public_dns_name + " 'pwd'"

  print cmd17  # displaying command for debug purposes
  (status, output) = commands.getstatusoutput(cmd17)
  while (status):
    print "Attempting to SSH please wait....."
    time.sleep(30)
    (status, output) = commands.getstatusoutput(cmd17)
  if status:    ## Error case, print the command's output to stderr and exit
    sys.stderr.write(output)
    print "SSH failed exiting...."
    time.sleep(5)
    sys.exit(1)
  else:
    print output  ## Otherwise print the command's output
    print "SSH success"
    time.sleep(5)

#View current iptable rules
def view_iptables():

  cmd18 = "ssh -t -i " + my_key + ".pem ec2-user@" + my_instance[0].public_dns_name + " 'sudo iptables --list'"
  
  (status, output) = commands.getstatusoutput(cmd18)
  if status:    ## Error case, print the command's output to stderr and exit
    sys.stderr.write(output)
    print "Failure...Unable to view iptables"
  else:
    print output  ## Otherwise print the command's output
    print "Success..."
    time.sleep(5)
  menu()

main()

