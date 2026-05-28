import mysql.connector
db=mysql.connector.connect(host="localhost",user="root",password="",database="bank_management_system")
cursor=db.cursor()
def save_transaction(acc_no,name,action,amount,balance):
    query="INSERT INTO transactions(acc_no,name,action,amount,balance) VALUES(%s,%s,%s,%s,%s)"
    values=(acc_no,name,action,amount,balance)
    cursor.execute(query,values)
    db.commit()
cursor.execute("SELECT COUNT(*) FROM accounts")
count=cursor.fetchone()[0]
if count==0:
    default_accounts=[
        (1001,"ravi",1111,5000,False),
        (1002,"arun",2222,7000,False),
        (1003,"kumar",3333,3000,False),
        (1004,"vijay",4444,9000,False),
        (1005,"ajith",5555,6000,False)
    ]
    query="INSERT INTO accounts(acc_no,name,pin,balance,locked) VALUES(%s,%s,%s,%s,%s)"
    cursor.executemany(query,default_accounts)
    db.commit()
manager={"name":"suriya","password":12,"pin":34}
print("WELCOME TO OUR BANK")
while True:
    print("1.Create Account")
    print("2.Login")
    print("3.Admin Login")
    print("4.Exit")
    a=int(input("Enter choice : "))
    if a==1:
        name=input("Enter name : ")
        pin=int(input("Enter pin : "))
        balance=int(input("Enter amount more than 1000 : "))
        if balance>=1000:
            cursor.execute("SELECT MAX(acc_no) FROM accounts")
            last_acc=cursor.fetchone()[0]
            if last_acc:
                acc=last_acc+1
            else:
                acc=1001
            query="INSERT INTO accounts(acc_no,name,pin,balance,locked) VALUES(%s,%s,%s,%s,%s)"
            values=(acc,name,pin,balance,False)
            cursor.execute(query,values)
            db.commit()
            print("Account created successfully")
            print("Account Number :",acc)
        else:
            print("Invalid amount")
    elif a==2:
        account_no=int(input("Enter account number : "))
        pin=int(input("Enter pin : "))
        query="SELECT * FROM accounts WHERE acc_no=%s AND pin=%s"
        cursor.execute(query,(account_no,pin))
        user=cursor.fetchone()
        if user:
            locked=user[4]
            if locked:
                print("Account is locked")
                continue
            while True:
                print("1.Balance")
                print("2.Deposit")
                print("3.Withdraw")
                print("4.Transfer")
                print("5.Change Pin")
                print("6.Delete Account")
                print("7.Transaction History")
                print("8.Logout")
                option=int(input("Choose option : "))
                if option==1:
                    cursor.execute("SELECT balance FROM accounts WHERE acc_no=%s",(account_no,))
                    balance=cursor.fetchone()[0]
                    print("Balance :",balance)
                elif option==2:
                    deposit=int(input("Enter deposit amount : "))
                    if deposit>0:
                        query="UPDATE accounts SET balance=balance+%s WHERE acc_no=%s"
                        cursor.execute(query,(deposit,account_no))
                        db.commit()
                        cursor.execute("SELECT balance,name FROM accounts WHERE acc_no=%s",(account_no,))
                        data=cursor.fetchone()
                        balance=data[0]
                        name=data[1]
                        save_transaction(account_no,name,"Deposit",deposit,balance)
                        print("New balance :",balance)
                elif option==3:
                    withdraw=int(input("Enter withdraw amount : "))
                    cursor.execute("SELECT balance,name FROM accounts WHERE acc_no=%s",(account_no,))
                    data=cursor.fetchone()
                    balance=data[0]
                    name=data[1]
                    if 0<withdraw<=balance:
                        query="UPDATE accounts SET balance=balance-%s WHERE acc_no=%s"
                        cursor.execute(query,(withdraw,account_no))
                        db.commit()
                        new_balance=balance-withdraw
                        save_transaction(account_no,name,"Withdraw",withdraw,new_balance)
                        print("New balance :",new_balance)
                    else:
                        print("Invalid amount")
                elif option==4:
                    transfer=int(input("Enter transfer amount : "))
                    transfer_account=int(input("Enter receiver account : "))
                    cursor.execute("SELECT balance,name FROM accounts WHERE acc_no=%s",(account_no,))
                    sender=cursor.fetchone()
                    sender_balance=sender[0]
                    sender_name=sender[1]
                    if 0<transfer<=sender_balance:
                        cursor.execute("SELECT name,balance FROM accounts WHERE acc_no=%s",(transfer_account,))
                        receiver=cursor.fetchone()
                        if receiver:
                            receiver_name=receiver[0]
                            cursor.execute("UPDATE accounts SET balance=balance-%s WHERE acc_no=%s",(transfer,account_no))
                            cursor.execute("UPDATE accounts SET balance=balance+%s WHERE acc_no=%s",(transfer,transfer_account))
                            db.commit()
                            print("Transfer successful")
                            save_transaction(account_no,sender_name,"Transfer Sent",transfer,sender_balance-transfer)
                            save_transaction(transfer_account,receiver_name,"Transfer Received",transfer,receiver[1]+transfer)
                        else:
                            print("Invalid account")
                    else:
                        print("Insufficient balance")
                elif option==5:
                    new_pin=int(input("Enter new pin : "))
                    cursor.execute("UPDATE accounts SET pin=%s WHERE acc_no=%s",(new_pin,account_no))
                    db.commit()
                    print("Pin changed successfully")
                elif option==6:
                    confirm=input("Delete account yes/no : ")
                    if confirm=="yes":
                        cursor.execute("DELETE FROM accounts WHERE acc_no=%s",(account_no,))
                        db.commit()
                        print("Account deleted")
                        break
                elif option==7:
                    cursor.execute("SELECT action,amount,balance FROM transactions WHERE acc_no=%s",(account_no,))
                    data=cursor.fetchall()
                    for i in data:
                        print(i)
                elif option==8:
                    print("Logout successful")
                    break
                else:
                    print("Invalid option")
        else:
            print("Invalid account or pin")
    elif a==3:
        password=int(input("Enter password : "))
        pin=int(input("Enter pin : "))
        if password==manager["password"] and pin==manager["pin"]:
            while True:
                print("1.Show Accounts")
                print("2.Delete Account")
                print("3.Lock Account")
                print("4.Unlock Account")
                print("5.Total Balance")
                print("6.Logout")
                option=int(input("Enter option : "))
                if option==1:
                    cursor.execute("SELECT * FROM accounts")
                    data=cursor.fetchall()
                    for i in data:
                        print(i)
                elif option==2:
                    acc=int(input("Enter account : "))
                    cursor.execute("DELETE FROM accounts WHERE acc_no=%s",(acc,))
                    db.commit()
                    print("Account deleted")
                elif option==3:
                    acc=int(input("Enter account : "))
                    cursor.execute("UPDATE accounts SET locked=True WHERE acc_no=%s",(acc,))
                    db.commit()
                    print("Account locked")
                elif option==4:
                    acc=int(input("Enter account : "))
                    cursor.execute("UPDATE accounts SET locked=False WHERE acc_no=%s",(acc,))
                    db.commit()
                    print("Account unlocked")
                elif option==5:
                    cursor.execute("SELECT SUM(balance) FROM accounts")
                    total=cursor.fetchone()[0]
                    print("Total Balance :",total)
                elif option==6:
                    break
        else:
            print("Wrong password or pin")
    else:
        print("Exit successful")
        break
