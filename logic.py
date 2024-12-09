# Zachary Morin 
# SNUMS LOGIC BOARD
# Simple Network User Management System

import ldap
import ldap.modlist as modlist
import hashlib


"""
# Queries the SLAPd server
searchScope = ldap.SCOPE_SUBTREE
result = connect.search_s(binddn,
                          ldap.SCOPE_SUBTREE,
                          binddn,
                          ['memberOf'])
print(result)
"""

def connectToSLAPd(ip, binddn, passwd):
    uri = 'ldap://' + ip
    connection = ldap.initialize(uri)
    connection.set_option(ldap.OPT_REFERRALS, 0)
    connection.simple_bind_s(binddn, passwd)
    return connection

# Creating a new OU
def CreateOU(connection, name, base_location):
    connect = connection
    #ou_name = b"NewOU"
    OU_name = name.encode('utf-8')
    attributes = {
        "objectClass" : [b"organizationalUnit"],
        "ou" : OU_name
    }
    # base_location = "DC=snums,DC=local"
    dn_ou = b"ou=" + OU_name + b"," + str.encode(base_location)
    print(dn_ou)
    ldif = modlist.addModlist(attributes)
    print(ldif)
    try:
        connect.add_s(dn_ou.decode(), ldif)
        print(OU_name.decode() + " OU has been created.")
    except ldap.ALREADY_EXISTS:
        print(OU_name.decode() + " OU already exists.")

#CreateOU("NewOU2",basedn)

#testCase = input("Name of new OU: ")
#CreateOU(testCase, basedn)

# Create Group
def CreateGroup(name, OU_DN):
    pass

# Create User
def CreateUser(connection, name, password, OU_DN):
    connect = connection
    hashedPassword = hashlib.md5(password.encode('utf-8'))
    digest = hashedPassword.digest()
    shadowEntry = b"{CRYPT}" + name.encode('utf-8') + b":" + b"$1$" + digest + b"::" + b"::" + b":99999:" + b"::" + b"::" + b"::"
    user_dn = b"cn=" + name.encode('utf-8') + b"," + OU_DN.encode('utf-8')
    user_attributes = {
        "objectClass" : [b"inetOrgPerson", b"person", b"top", b"posixAccount", b"shadowAccount"],
        "uid": name.encode('utf-8'),
        "cn" : name.encode('utf-8'),
        "sn" : b"none",
        "givenName": name.encode('utf-8'),
        "userPassword" : shadowEntry,
        "mail": b"none@none.com",
        "uidNumber" : b"891",
        "gidNumber" : b"49",
        "homeDirectory" : b"/home/test",
        "loginShell" : b"/bin/bash",
    }

    print(user_attributes)
    
    ldif = modlist.addModlist(user_attributes)
    try:
        connect.add_s(user_dn.decode(), ldif)
        print("User "+name+ " has been created.")
    except ldap.ALREADY_EXISTS:
        print("User "+name+" already exists.")


# List all top-level Organizational Units
def GetOUs(connection, base_location):
    connect = connection
    result = connect.search_s(base_location,
                          ldap.SCOPE_SUBTREE,
                          'objectClass=organizationalUnit', # Put ldapsearch filter here.
                          ['memberOf']) 
    return result

def GetUsers(connection, base_location):
    connect = connection
    result = connect.search_s(base_location,
                          ldap.SCOPE_SUBTREE,
                          'objectClass=inetOrgPerson', # Put ldapsearch filter here.
                          ['memberOf']) 
    return result


#CreateUser("morin","testGroup","OU=NewOU2,DC=snums,DC=local")

# FUNCTION TESTS HERE
if __name__ == "__main__":

    # Sets the SLAPd hostname and user information
    ldap_uri = 'ldap://10.0.0.27'
    binddn = "cn=admin,dc=snums,dc=local"
    pw = 'admin'
    basedn = "dc=snums,dc=local"

    # Connects to the SLAPd server
    connect = ldap.initialize(ldap_uri)
    connect.set_option(ldap.OPT_REFERRALS, 0)
    connect.simple_bind_s(binddn, pw)   

    CreateOU(connect, "test",basedn) # DONE SUCCESSFULLY
    CreateOU(connect, "test2",basedn)
    print(GetOUs(connect, basedn))
    CreateUser(connect,"zachary","password","ou=test,dc=snums,dc=local") # Done successfully.
    print(GetUsers(connect,basedn)) # Done successfully.
