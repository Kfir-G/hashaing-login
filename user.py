import argparse, csv, hashlib, uuid

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

login = subparser.add_parser('login')
register = subparser.add_parser('register')

login.add_argument('--username', type=str, required=True)
login.add_argument('--password', type=str, required=True)
register.add_argument('--username', type=str, required=True)
register.add_argument('--password', type=str, required=True)
args = parser.parse_args()

flag = False
salt = uuid.uuid4().hex #Random salt

#----Login----
if args.command == 'login':
  print('Logging in with username:', args.username, 'and password:', args.password)

  #searching user info:
  with open('shadow.csv', newline='') as myFile:
    reader = csv.reader(myFile)
    for row in reader:
      #Checking input password to password in file per row
      if str(row[0])==args.username and hashlib.sha256(args.password.encode('utf-8')+row[2].encode('utf-8')).hexdigest() == row[1]: 
        print('Login success! Hello', args.username)
        flag = True
        break

    #Cheking if we have found the user
    if(flag == False):
      print('user authentication FALSE')

#----Register----
elif args.command == 'register':
  print('Creating username', args.username, 'and password:', args.password)

  #searching user exists
  with open('shadow.csv', newline='') as myFile:
    reader = csv.reader(myFile)
    for row in reader:
      #Checking input password to password in file per row
      if str(row[0])==args.username: 
        print('User already exists!')
        flag = True
        break
  
  if flag == False :
    #Write to file
    myData = [[args.username, hashlib.sha256(args.password.encode('utf-8')+salt.encode('utf-8')).hexdigest(),salt]]
    myFile = open('shadow.csv', 'a', newline='')
    with myFile:
      writer = csv.writer(myFile)
      writer.writerows(myData)