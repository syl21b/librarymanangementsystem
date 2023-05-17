#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 17:20:30 2023

@author: shinle
"""


'''
Created on Sat Feb 25 20:43:15 2023
Idea:
https://www.matellio.com/blog/how-to-develop-library-management-system/

Implement:
https://data-flair.training/blogs/library-management-system-python-project/
https://pythongeeks.org/python-library-management-system-project/

@author: Shin Le

email:
https://www.codespeedy.com/sending-emails-using-smtp-and-mime-in-python/
https://pybit.es/articles/python-MIME/
https://python.readthedocs.io/fr/hack-in-language/library/email-examples.html
https://docs.python.org/3/library/email.mime.html
'''


import pandas as pd
import mysql.connector
from datetime import datetime, timedelta, date

'''USING FOR ADVANCED FUNCTION'''
import smtplib
from email.mime.text import MIMEText
import schedule
import time



DEFAULT_PASSWORD='123456789LIB'

# Read Excel file into a Pandas DataFrame
dfBook = pd.read_excel('Books.xlsx')
dfLibrarian = pd.read_excel('Librarians.xlsx')
dfMember = pd.read_excel('Member.xlsx')
dfSystem = pd.read_excel('System.xlsx')

# replace any NaN values in the DataFrame with None values
#dfMember = dfMember.where(pd.notnull(dfMember), None)

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='syl21b',
    database='proj1'
)

# Create a cursor
cur = conn.cursor()

def close(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

'''
#___CREATE TABLES___________________________________________________________________________________________
# Create and insert into the System table 
cur.execute('CREATE TABLE System_Table (User_ID VARCHAR(50), Password VARCHAR(50), PRIMARY KEY (User_ID))')
for row in dfSystem.itertuples():
    cur.execute('INSERT INTO  System_Table (User_ID, Password) VALUES (%s, %s)', (row[1], row[2]))
 
# Create and insert into the Book table 
cur.execute('CREATE TABLE IF NOT EXISTS Book ('
                     'Book_ID INT, ISBN VARCHAR(255),'
                    'Title VARCHAR(255),'
                    'Genre VARCHAR(50), ' 
                    'Author VARCHAR(255),'
                   'Year INT, Publisher VARCHAR(255), Availability VARCHAR(255), URL VARCHAR(255), PRIMARY KEY(Book_ID)'
                   ')')
for row in dfBook.itertuples():
    cur.execute('INSERT INTO Book (book_id, isbn, title, genre, author, year, publisher,Availability, URL) VALUES (%s,%s, %s, %s,%s, %s, %s, %s, %s)', (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],row[9]))

# Create and insert into the Librabrian table 
cur.execute('CREATE TABLE IF NOT EXISTS Librarian (Librarian_ID VARCHAR(50),  Name VARCHAR(50), Phone_Number VARCHAR(20),PRIMARY KEY (Librarian_ID), FOREIGN KEY (Librarian_ID) REFERENCES System_Table(User_ID))')

for row in dfLibrarian.itertuples():
    cur.execute('INSERT INTO Librarian (Name, Librarian_ID,Phone_Number ) VALUES (%s, %s,%s)', (row[1], row[2], row[3]))

# Create and insert into the Member table 
cur.execute('CREATE TABLE IF NOT EXISTS Member ('
            'Member_ID VARCHAR(50) ,  First_Name VARCHAR(50), Last_Name VARCHAR(50),Phone_Number VARCHAR(20),'
            'Email VARCHAR(50),Issue_Date DATE, Due_Date DATE, Return_Status VARCHAR(10),  '
            'Book_ID INT NULL,Record VARCHAR(8096) NULL, PRIMARY KEY (Member_ID),'
            'FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID), FOREIGN KEY (Member_ID) REFERENCES System_Table(User_ID)'
            ')')

for row in dfMember.itertuples():
   
    # Insert row into Member table
    cur.execute('INSERT INTO Member (Member_ID, First_Name, Last_Name, Phone_Number, Email, Issue_Date, Due_Date, Return_Status, Book_ID, Record) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
            (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9] if str(row[9]) != 'nan' else None, None if str(row[10]) == 'nan'  else row[10]))

   
# Execute a SELECT statement to retrieve data from the table
#cur.execute('SELECT * FROM System_Table')
#cur.execute('SELECT * FROM Book')
#cur.execute('SELECT * FROM Member')
#cur.execute('SELECT * FROM Librarian')

# Fetch all the rows and print them
rows = cur.fetchall()
for row in rows:
    print(row)

# Commit the changes and close the connection
conn.commit()
conn.close()
#________________________________________________________________________________________

'''
class User:
    def __init__(self, id, hashed_password):
        self.id = id
        self.hashed_password = hashed_password

        
class Library:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
   
    def get_user(self, user_id):
        self.cur.execute("SELECT User_ID, Password FROM System_Table WHERE User_ID=%s", (user_id,))
        row = cur.fetchone()
        cur.close()
        if row:
            user = User(row[0], row[1])
            return user
        return None
#____________________________________________________________________________________________________________  

#UPDATE/DELETE BOOK INFORMATION
    #UPDATE BOOK FUNCTIONS:
    def check_book_id(self, book_id):
        
        # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()
        if result:
            return 'Book ID is valid'
             
        else:
            return 'Book ID not found'
        
    def update_isbn(self, isbn, book_id):
        '''Updates the ISBN field for a book based on the given book_id.'''
        # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()
        if result:
             # Update the phone number of the member
            self.cur.execute("UPDATE Book SET ISBN = %s WHERE Book_ID = %s", (isbn, book_id))
             
        else:
            return 'Book ID not found'
    
    def update_title(self, title, book_id):
        '''Updates the Title field for a book based on the given book_id.'''
        # Check if book ID exists in Book table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()
        if result:
            # Update the title of the book
            self.cur.execute("UPDATE Book SET Title = %s WHERE Book_ID = %s", (title, book_id))
             
        else:
            return 'Book ID not found'
        
    def update_genre(self, genre, book_id):
        '''Updates the Genre field for a book based on the given book_id.'''
        # Check if book ID exists in Book table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()
        if result:
            # Update the genre of the book
            self.cur.execute("UPDATE Book SET Genre = %s WHERE Book_ID = %s", (genre, book_id))
             
        else:
            return 'Book ID not found'
        
    def update_author(self, author, book_id):
        '''Updates the Author field for a book based on the given book_id.'''
        # Check if book ID exists in Book table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()
        if result:
            # Update the author of the book
            self.cur.execute("UPDATE Book SET Author = %s WHERE Book_ID = %s", (author, book_id))
             
        else:
            return 'Book ID not found'
    
    def update_year(self, year, book_id):
        '''Updates the Year field for a book based on the given book_id.'''
        # Check if book ID exists in Book table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()
        if result:
            # Update the year of the book
            self.cur.execute("UPDATE Book SET Year = %s WHERE Book_ID = %s", (year, book_id))
             
        else:
            return 'Book ID not found'

    def update_publisher(self, publisher, book_id):
        '''Updates the Publisher field for a book based on the given book_id.'''
        # Check if book ID exists in Book table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()
        if result:
            # Update the publisher of the book
            self.cur.execute("UPDATE Book SET Publisher = %s WHERE Book_ID = %s", (publisher, book_id))
             
        else:
            return 'Book ID not found'

    def update_url(self, url, book_id):
        '''Updates the URL field for a book based on the given book_id.'''
        # Check if book ID exists in Book table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()
        if result:
            # Update the URL of the book
            self.cur.execute("UPDATE Book SET URL = %s WHERE Book_ID = %s", (url, book_id))
             
        else:
            return 'Book ID not'

    #CREATE BOOK FUNCTIONS:
    def create_new_book(self, isbn, title, genre, author, year, publisher, URL):
        self.cur.execute("SELECT MAX(Book_ID) FROM Book")
        result = self.cur.fetchone()[0]
        next_book_id = result + 1 if result else 1
        book_id = next_book_id;
                
        availability="Yes"
        
        # Execute the insert statement
        sql = "INSERT INTO Book (Book_ID, ISBN, Title, Genre, Author, Year, Publisher, Availability, URL) VALUES ( %s,%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (book_id, isbn, title, genre, author, year, publisher, availability, URL)
        self.cur.execute(sql, values)
        
        # Commit the changes and close the connection
         
        
        return 'New book record created successfully', book_id
        

#______DELETE BOOK______________________________________________________________________________________________________  
   
    def delete_book(self, book_id):
        # Check if book ID exists in Book table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()
    
        if not result:
            #"Book ID not found."
            return 'Book ID not found'
        else:
            # Check if book ID exists in Book table
            self.cur.execute('SELECT * FROM Member WHERE Book_ID = %s AND Return_Status =%s', (book_id,'No',))
            checkReturn = self.cur.fetchone()
            
            if checkReturn:
                return 'The book is currently being borrowed'
            else:
                # Execute the delete statement
                sql = "DELETE FROM Book WHERE Book_ID = %s"
                value = (book_id,)
                self.cur.execute(sql, value)
                #"Book record deleted successfully."
                return 'Book record deleted successfully'
#____________________________________________________________________________________________________________  
 
#CREATE NEW MEMBER
    def create_new_member(self,first_name, last_name, phone_number, email,user_id, password):
        
        # Check if user ID and password match in system table
        self.cur.execute('SELECT * FROM System_Table WHERE User_ID = %s', (user_id, ))
        system_result = self.cur.fetchone()

        if system_result:
            return True
            
        else:
            # Set default values for new member record
            issue_date = '2000-01-01'
            due_date = '2000-01-01'
            return_status = 'Yes'
            book_id = None
            record = None
            
            # Insert new user and password into System_Table
            sql1 = "INSERT INTO System_Table (User_ID, Password) VALUES (%s, %s)"
            value1 = (user_id, password)
            self.cur.execute(sql1, value1)
            
            # Insert new record into Member table
            sql_member = "INSERT INTO Member (Member_ID, First_Name, Last_Name, Phone_Number, Email, Issue_Date, Due_Date, Return_Status, Book_ID, Record) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values_member = (user_id, first_name, last_name, phone_number, email, issue_date, due_date, return_status, book_id, record)
            self.cur.execute(sql_member, values_member)
            return False
            
      
#______UPDATE/DELETE MEMBERSHIP INFORMATION______________________________________________________________________________________________________  
        

    
    def update_member_phone(self,member_id, new_phone_number):
        # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s', (member_id,))
        result = self.cur.fetchone()
        if result:
             # Update the phone number of the member
            self.cur.execute('UPDATE Member SET Phone_Number = %s WHERE Member_ID = %s', (new_phone_number, member_id))
             
        else:
            return 'Member ID not found'
        
    def update_member_password(self,member_id, new_password):
        # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Member JOIN System_Table ON Member.Member_ID = System_Table.User_ID WHERE Member.Member_ID = %s', (member_id,))
        result = self.cur.fetchone()
        if result:
            # Update the password of the member
            self.cur.execute('UPDATE System_Table SET Password = %s WHERE User_ID = %s', (new_password, member_id))
             
        else:
            return 'Member ID not found'        
     
    
    def update_member_email(self,member_id, new_email_address):
        # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s', (member_id,))
        result = self.cur.fetchone()
        if result:
            # Update the email address of the member
            self.cur.execute('UPDATE Member SET Email = %s WHERE Member_ID = %s', (new_email_address, member_id))
             
        else:
           return 'Member ID not found'

    def delete_member(self, member_id):
        # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s', (member_id,))
        result = self.cur.fetchone()
    
        if not result:
            #print("Member ID not found.")
            return 'Member ID not found'
        else:
            if result[7] == 'No':
                # The member has borrow records, cannot delete
                #print("Cannot delete member with borrow records.")
                return 'Cannot delete member with borrow records'
            else:
                # Execute the delete statement
                sql = "DELETE FROM Member WHERE Member_ID = %s"
                value = (member_id,)
                self.cur.execute(sql, value)
                
                sql1 = "DELETE FROM System_Table WHERE User_ID = %s"
                value1 = (member_id,)
                self.cur.execute(sql1, value1)
                
                #print("Member record deleted successfully.")
                return 'Membership deleted successfully!'

#____BORROW / RETURN BOOK________________________________________________________________________________________________________  

    def borrow_book(self,member_id, book_id, issue_date):
        # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s', (member_id,))
        result = self.cur.fetchone()
        if result:
            #self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s AND Return_Status =%s', (member_id,'No',))
            #result1 = self.cur.fetchone()
            #if result1:
            #    return 'You are borrowing a book. Please return it to be able to borrow a new one!'

            # Check if the member has any overdue books
            self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s AND Return_Status = %s', (member_id, 'No'))
            result1 = self.cur.fetchall()
            if result1:
                return 'Currently borrow a book'
            

            # Update the book information of the member
            due_date = datetime.strptime(issue_date, '%Y-%m-%d') + timedelta(days=7)

            # Check if the book exists in the Book table
            self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
            book = self.cur.fetchone()

            if not book:
                return 'Book ID not found'
            else:
                # Check if the book is available
                self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s AND Availability = %s', (book_id,'No',))
                record_result = self.cur.fetchone()

                if record_result:
                    return 'Book not available'

            self.cur.execute('UPDATE Book SET Availability = %s WHERE Book_ID = %s',('No',book_id,))

            return_status ='No'

            record = str(book_id)
            # Check if Record is empty
            self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s ', (member_id,))
            record_result = self.cur.fetchone()
            if record_result[9] == None:
                # If empty, set Record to new value
                self.cur.execute('UPDATE Member SET Book_ID = %s, Issue_Date = %s, Due_Date = %s,Return_Status=%s, Record = %s WHERE Member_ID = %s', (book_id, issue_date, due_date,return_status, record, member_id))
            else:
                # If not empty, concatenate new value to Record
                self.cur.execute('UPDATE Member SET Book_ID = %s, Issue_Date = %s, Due_Date = %s,Return_Status=%s, Record = CONCAT(Record, "; ", %s) WHERE Member_ID = %s', (book_id, issue_date, due_date, return_status, record, member_id))


            return 'success'

        else:
            #print("Member ID not found.")
            return 'Member ID not found.'


    
    def return_book(self, member_id, book_id, returnstatus):
        # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s', (member_id,))
        result = self.cur.fetchone()

        if not result:
            return 'Member ID not found'

        # Check if book ID exists in Book table
        self.cur.execute('SELECT * FROM Book WHERE Book_ID = %s', (book_id,))
        book = self.cur.fetchone()

        if not book:
            return 'Book ID not found'

        # Check if member has borrowed the book
        self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s AND Book_ID = %s', (member_id, book_id))
        borrow_result = self.cur.fetchone()

        if not borrow_result:
            return 'The book is not borrowed by the member'
        
        # Update the member's record
        self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s', (member_id,))
        record_result = self.cur.fetchone()
        #if record_result[0] == str(book_id):
            # If the member has only borrowed this book, set the record to empty
        self.cur.execute('UPDATE Member SET Book_ID = NULL, Issue_Date = "2000-01-01", Due_Date = "2000-01-01", Return_Status = %s WHERE Member_ID = %s', (returnstatus, member_id))
        '''else:
            # If the member has borrowed multiple books, remove the returned book from the record
            book_ids = record_result[0].split(', ')
            book_ids.remove(str(book_id))
            record = ', '.join(book_ids)
            self.cur.execute('UPDATE Member SET Book_ID = NULL, Issue_Date = "2000-01-01", Due_Date = "2000-01-01", Return_Status= %s WHERE Member_ID = %s', (returnstatus, member_id))
        '''
        # Update the book's availability
        self.cur.execute('UPDATE Book SET Availability = "Yes" WHERE Book_ID = %s', (book_id,))
        #self.cur.execute('UPDATE Member SET Return = %s WHERE Member_ID = %s', (returnstatus,member_id,))
         

        return 'Book returned successfully'


#______UPDATE/DELETE LIBRARIAN INFORMATION______________________________________________________________________________________________________  
            
    def update_librarian_password(self,Librarian_id, new_password):
        # Check if Librarian ID exists in Librarian table
        self.cur.execute('SELECT * FROM Librarian JOIN System_Table ON Librarian.Librarian_ID = System_Table.User_ID WHERE Librarian.Librarian_ID = %s', (Librarian_id,))
        result = self.cur.fetchone()
        if result:
            # Update the password of the Librarian
            self.cur.execute('UPDATE System_Table SET Password = %s WHERE User_ID = %s', (new_password, Librarian_id))
             
        else:
            print("Librarian ID not found.")
    
    def update_librarian_phone(self,Librarian_id, new_phone_number):
        # Check if Librarian ID exists in Librarian table
        self.cur.execute('SELECT * FROM Librarian WHERE Librarian_ID = %s', (Librarian_id,))
        result = self.cur.fetchone()
        if result:
             # Update the phone number of the Librarian
            self.cur.execute('UPDATE Librarian SET Phone_Number = %s WHERE Librarian_ID = %s', (new_phone_number, Librarian_id))
             
        else:
            return 'Librarian ID not found'
        #____________________________________________________________________________________________________________  
             

    def update_librarian(self, librarian_id, change_phone, password):
          # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Librarian WHERE Librarian_ID = %s', (librarian_id,))
        result = self.cur.fetchone()
        if result:
             # Update the phone number of the member
            self.cur.execute('UPDATE Librarian SET Phone_Number = %s, Password =%s WHERE Librarian_ID = %s', (change_phone, password, librarian_id))
            self.cur.execute('UPDATE System_Table SET  Password =%s WHERE User_ID = %s', ( password, librarian_id))
             
            return 'Librarian information updated successfully'
        else:
            return 'Librarian ID not found'
       
    
    def create_librarian(self, first_name, last_name, phone_number,Librarian_id):
        
        
        # Check if member ID exists in Member table
        self.cur.execute('SELECT * FROM Librarian WHERE Librarian_ID = %s', (Librarian_id,))
        result = self.cur.fetchone()
        
        if result:
            return True
        else:
            
            name = first_name + "," +last_name
            password = DEFAULT_PASSWORD #THIS IS THE DEFAULT PASSWORD
            
            #INSERT NEW USER AND PASSWORD into System_Table
            sql1 = "INSERT INTO System_Table (User_ID, Password) VALUES (%s, %s)"
            value1 = (Librarian_id, password)
            self.cur.execute(sql1, value1)
            
            # Execute the insert statement
            sql = "INSERT INTO Librarian (Librarian_ID, Name, Phone_Number) VALUES ( %s, %s, %s)"
            values = (Librarian_id, name, phone_number)
            self.cur.execute(sql, values)
                
            
                
            print("New librarian record created successfully.")
            return False
            
    def delete_librarian(self, librarian_id):
        # Check if Librarian ID exists in Librarian table
        self.cur.execute('SELECT * FROM Librarian WHERE librarian_id = %s', (librarian_id,))
        result = self.cur.fetchone()

        if not result:
            return 'Librarian ID not found'
        else:
            # Execute the delete statement
            sql = "DELETE Librarian, System_Table FROM Librarian INNER JOIN System_Table ON Librarian.librarian_id = System_Table.User_ID WHERE Librarian.librarian_id = %s"
            value = (librarian_id,)
            self.cur.execute(sql, value)
            '''
            # Execute the delete statement
            sql = "DELETE FROM Librarian WHERE Librarian_ID = %s"
            value = (Librarian_id,)
            self.cur.execute(sql, value)
                
            sql1 = "DELETE FROM System_Table WHERE User_ID = %s"
            value1 = (Librarian_id,)
            self.cur.execute(sql1, value1)
             '''   
            #print("Librarian record deleted successfully.")
            return 'Librarian record deleted successfully!'
            
        
#____________________________________________________________________________________________________________  

#LOG IN
    def log_in(self, user_id, password):
        # Check if user ID and password match in system table
        self.cur.execute('SELECT * FROM System_Table WHERE User_ID = %s AND Password = %s', (user_id, password,))
        system_result = self.cur.fetchone()

        if system_result:
            # Check if the user is a librarian
            self.cur.execute('SELECT * FROM Librarian WHERE Librarian_ID = %s', (user_id,))
            librarian_result = self.cur.fetchone()

            if librarian_result:
                return "librarian"
            
            # Check if the user is a member
            self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s', (user_id,))
            member_result = self.cur.fetchone()

            if member_result:
                return "member"

        # Return None if user ID and password don't match or if the user is not found in either table
        return None
#____________________________________________________________________________________________________________  

  
    '''
•	Basic Functions:
    o	Insert records to the database.
    o	Search the database and list or print returned results: searching the information about book and membership.
    o	Show a few different interesting queries over your database. 
        •	How many books are currently available in the library?
        •	***What is the name of the book that was checked out the greatest number of times in the last year?
        •	Which books have been checked out by a member with the ID 123456?
        •	Which books are currently available and belong to the “sports” genre? 
        •	Who is the author of the book with the ISBN number 123456?
        •	What is the name of the member who checked out the book with the title " Contact"?
    o	One of the queries must involve join of multiple tables, and one must be an aggregate query: 
        •	Join query: Find the names and email addresses of all members who have checked out books currently, along with the titles of the books they have checked out.
        •	Aggregate query: Find the total number of books checked out each month, grouped by month.
    o	Show how to update records: update information for new books, new member, and new librarian, book return, etc. Also, members can update their password, and librarians can update the return status, due date, and issue date for borrowers.
    o	Show how to delete records: delete the book or membership if it does not exist anymore or is expired.

•	Advanced Functions:
    To enhance the user experience and increase the functionality of the Library Management System, I may add at least one of these unique features:
    o	Book recommendation: Provide a feature for library members to receive book recommendations based on their reading history and preferences.
    o	Overdue reminders: Send automated reminders to members when their checked-out items are approaching their due date. 
    o	Late Fees Calculator: This function will calculate the late fees for member who have returned books past the due date. To implement this, you can use a simple formula based on the number of days late and the late fee rate, which can be stored in the database.
    o	Event calendar: Add a calendar feature to display information about upcoming library events and programs.
    o	Email Notifications for Book Availability: This function will send email notifications to members who have placed a hold on a book that has become available. To implement this, you can use an email service, such as Gmail, to send the emails and a task scheduling tool to schedule the notifications.

'''

#____________________________________________________________________________________________________________  

    def get_available_books_count(self):
        self.cur.execute("SELECT COUNT(*) FROM Book WHERE Availability = 'Yes'")
        result = self.cur.fetchone()[0]
        self.cur.execute("SELECT * FROM Book WHERE Availability = 'Yes'")
        books = self.cur.fetchall()
        return result, books
    



#____________________________________________________________________________________________________________  
  
    def get_books_by_member(self, member_id):
        # Execute the select statement to get book that is being borrowed by the member
        sql = "SELECT * FROM Book JOIN Member ON Member.Book_ID = Book.Book_ID WHERE Member.Member_ID = %s"
        values = (member_id,)
        self.cur.execute(sql, values)  
        results = self.cur.fetchall()
        
        # Return the results
        if results:
            message = 'This Member ID  ' + member_id.upper() + ' is borrowing a book' 
            return results, message
        else:
            message = 'This Member ID ' + member_id.upper() + ' does not borrow any book'
            
        return results, message


#____________________________________________________________________________________________________________  
   
    
    def get_available_books_by_genre(self, genre):
        # Execute the select statement
        self.cur.execute("SELECT * FROM Book WHERE Genre = %s AND Availability = 'Yes'", (genre,))
        result = self.cur.fetchall()

        # Print the results
        if result:
            message = f"Available {genre} books:"
        else:
            message = f"No available {genre} books found."
            
        return result, message

    def count_books_by_genre(self):
        # Execute a SELECT statement to retrieve data from the table
        self.cur.execute("SELECT genre, COUNT(*) FROM Book GROUP BY genre, Availability HAVING Book.Availability = 'Yes'")

        # Fetch all the rows and store them in a list of dictionaries
        rows = self.cur.fetchall()
        books_by_genre = [{'genre': row[0], 'count': row[1]} for row in rows]

        return books_by_genre

    def get_book_by_isbn(self, isbn):
        # Get the author of the book with the given ISBN number
        self.cur.execute('SELECT * FROM Book WHERE ISBN = %s', (isbn,))
        result = self.cur.fetchall()
        if result:
            message = f"The book with ISBN {isbn} is:"
        else:
            message= f"No book found with ISBN {isbn}"
        
        return result, message   
    
    def get_book_by_author(self, author):
        # Get the author of the book with the given ISBN number
        self.cur.execute('SELECT * FROM Book WHERE Author = %s', (author,))
        result = self.cur.fetchall()
        if result:
            message = f"The book by author {author} is:"
        else:
            message= f"No book found with author {author}"
        
        return result, message   
    
    def get_book_by_year(self, year):
        # Get the book with the given year
        self.cur.execute('SELECT * FROM Book WHERE Year = %s', (year,))
        result = self.cur.fetchall()
        if result:
            message = f"The book with year {year} is:"
        else:
            message= f"No book found with year {year}"
        
        return result, message  
    
    def get_book_by_publisher(self, publisher):
        # Get the book with the given publisher
        self.cur.execute('SELECT * FROM Book WHERE Publisher = %s', (publisher,))
        result = self.cur.fetchall()
        if result:
            message = f"The book by publisher {publisher} is:"
        else:
            message= f"No book found with publisher {publisher}"
        
        return result, message  
    
    def get_book_by_keyword(self, keyword):
         # Search for books with titles containing the input string
         self.cur.execute("SELECT * FROM Book WHERE Title LIKE %s", ('%' + keyword + '%',))
         result = self.cur.fetchall()
         
         # Print the results
         if result:
             message = f"Books with titles containing '{keyword}':"
         else:
             message = f"No books found with titles containing '{keyword}'."
             
         return result, message


#____________________________________________________________________________________________________________  
    def show_record_by_memberid(self, member_id):
        # Check if the member ID exists in the Member table
        #self.cur.execute("SELECT COUNT(*) FROM Member WHERE Member_ID = %s", (member_id,))
        self.cur.execute("SELECT * FROM Member WHERE Member_ID = %s", (member_id,))
        member_exist = self.cur.fetchone()
        if not member_exist:
            message = f"No member found with ID {member_id}"
            book_info = []
            return book_info, message
        else:
            
            # Retrieve the Borrowed Record string from the Member table
            self.cur.execute( "SELECT Record FROM Member WHERE Member_ID = %s", (member_id,))
            record = self.cur.fetchone()[0]

            if not record or record == None:
                message = f"No Borrowed Record found for member ID {member_id}"
                book_info = []
                return book_info, message
            else:
                # Split the Borrowed Record string into a list of individual book IDs
                book_ids = record.split(';')

                # Retrieve the book information for each book ID from the Book table
                book_info = []
                for book_id in book_ids:
                    self.cur.execute("SELECT * FROM Book WHERE Book_ID = %s", (book_id,))
                    book_data = self.cur.fetchone()
                    if book_data:
                        book_info.append(book_data)
                    
                message =f"The Book Record found for member ID: {member_id}:"
                # Return the list of book information
                return book_info,message
    
    def last_borrow_book_by_memberid(self, member_id):
        # Check if the member ID exists in the Member table
        self.cur.execute("SELECT * FROM Member WHERE Member_ID = %s", (member_id,))
        member_exist = self.cur.fetchone()
        if not member_exist:
            message = f"No member found with ID {member_id}"
            book_info = []
            return book_info, message
        else:
            # Retrieve the Borrowed Record string from the Member table
            self.cur.execute("SELECT Record FROM Member WHERE Member_ID = %s", (member_id,))
            record = self.cur.fetchone()[0]
    
            if not record:
                message = f"No Borrowed Record found for member ID {member_id}"
                book_info = []
                return book_info, message
            else:
                # Split the Borrowed Record string into individual book IDs
                book_ids = [id for id in record.split(';') if id]
                last_book_id = book_ids[-1]
    
                # Retrieve the book information for the last book ID from the Book table
                book_info = []
                self.cur.execute("SELECT * FROM Book WHERE Book_ID = %s", (last_book_id,))
                book_data = self.cur.fetchone()
                if book_data:
                    book_info.append(book_data)
    
                message = f"The last borrowed book found for member ID: {member_id}:"
                return book_info, message

 #____________________________________________________________________________________________________________  
           
#____________________________________________________________________________________________________________  
   
    def get_member_info_borrowing_book(self, book_id):
        # Get the Member_ID of the member who borrowed the book with the given title
        self.cur.execute('SELECT Member_ID FROM Member WHERE Book_ID = %s', (book_id,))
        result = self.cur.fetchone()

        if not result:
            message = f"No member is currently borrowing the book {book_id}"
            return result, message

        member_id = result[0]

        # Get all information about the member
        self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s', (member_id,))
        result1 = self.cur.fetchall()

        if not result1:
            message = f"No information found for member {member_id}"
        else:
            message = f"Information for member who is currently borrowing the book {book_id}:"

        return result1, message

#____________________________________________________________________________________________________________  
    
    def get_overdue_members(self):
        self.cur.execute("SELECT * FROM Member WHERE Due_Date < CURDATE() AND Return_Status = 'No'")
        result = self.cur.fetchall()
        return result if result else None
#____________________________________________________________________________________________________________  

    def display_member_info (self, member_id):
        self.cur.execute('SELECT * FROM Member WHERE Member_ID = %s', (member_id,))
        result = self.cur.fetchone()
        if not result[8]:
            return result
        else:
            self.cur.execute('SELECT * FROM Member, Book WHERE Member.Book_ID = Book.Book_ID AND Member_ID = %s', (member_id,))
            result1 = self.cur.fetchone()
            return result1

       
        
#______ADVANCED FUNCTION______________________________________________________________________________________________________  

    '''

    •	Advanced Function: To implement Overdue reminders, I will follow these general steps:
        o	Set up a background task or scheduler that runs periodically (e.g., daily) to check for overdue checkout records.
        o	Retrieve all checkout records that are overdue (i.e., their due date is less than the current date).
        o	For each overdue checkout record, retrieve the member's contact information (e.g., email or phone number).
        o	Send an automated reminder to the member via email or SMS, providing details about the overdue items and the associated late fees (if applicable).

    '''
    def overdue_reminder(self):
            # Get the current date
            self.cur.execute("SELECT CURDATE()")
            current_date = self.cur.fetchone()[0]
            
            # Get the list of members who have overdue their due dates
            self.cur.execute("SELECT * FROM Member WHERE Due_Date < %s AND Return_Status ='No'", (current_date,))
            result = self.cur.fetchall()
            
            # Check if any members have overdue due dates
            if result:
                return result 
            else:
                return None

    def send_email(self, recipient_email, subject, message):
            # Replace the placeholders with actual values
            sender_email = "les098196@gmail.com"
            sender_password = "mlyliijgvlkesndb"
            smtp_server = "smtp.gmail.com"

            # Create a MIME message object
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email

            # Send the message via SMTP
            with smtplib.SMTP(smtp_server, 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)

    def send_overdue_reminders(self):
        # Get the current date
        today = date.today()

        # Get the list of checkout records that are overdue
        self.cur.execute("SELECT * FROM Member WHERE Due_Date < %s AND Return_Status ='No'", (today,))
        overdue_checkouts = self.cur.fetchall()
        
        list1 = []
        for checkout in overdue_checkouts:
            # Retrieve the member's contact information
            member_id = checkout[0]
            
            first_name = checkout[1]
            last_name = checkout[2]
            phone = checkout[3]
            email = checkout[4]
            due_date = checkout[6]
            late_fee_per_day = 0.25 # Replace with actual late fee amount
            late_days = (today - due_date).days
            late_fee = late_fee_per_day * late_days

                # Create the message for the reminder
            subject = "Library Book Overdue Reminder"
            message = f"Dear {first_name} {last_name},\n\nThis is a reminder that you have an overdue library book."+\
                    f"The book was due on {due_date.strftime('%m/%d/%Y')}, and it is now {late_days} days late. "\
                    f"The late fee is {late_fee:.2f} dollars.\n\nPlease return the book as soon as possible "\
                    f"to avoid further fees.\n\nThank you for using our library!\n"\
                    f"\nLibrary Management System"

            
            # Send the reminder via email or SMS
            if email:
                self.send_email(email, subject, message)
                message1 = f"Dear {first_name} {last_name}"
                list1.append([ email, subject, message1])
            #elif phone:
                # Send the reminder via SMS (assuming the SMS gateway for the carrier...
                
        return list1
    '''
    def send_overdue_reminders1(self):
        # Get the current date
        today = date.today()

        # Get the list of checkout records that are overdue
        self.cur.execute("SELECT * FROM Member WHERE Due_Date < %s AND Return_Status ='No'", (today,))
        overdue_checkouts = self.cur.fetchall()
        
        list1 = []
        for checkout in overdue_checkouts:
            # Retrieve the member's contact information
            member_id = checkout[0]
            
            first_name = checkout[1]
            last_name = checkout[2]
            phone = checkout[3]
            email = checkout[4]
            due_date = checkout[6]
            late_fee_per_day = 0.25 # Replace with actual late fee amount
            late_days = (today - due_date).days
            late_fee = late_fee_per_day * late_days

                # Create the message for the reminder
            subject = "Library Book Overdue Reminder"
            message = f"Dear {first_name} {last_name},\n\nThis is a reminder that you have an overdue library book."+\
                    f"The book was due on {due_date.strftime('%m/%d/%Y')}, and it is now {late_days} days late. "\
                    f"The late fee is {late_fee:.2f} dollars.\n\nPlease return the book as soon as possible "\
                    f"to avoid further fees.\n\nThank you for using our library!\n"

            
            # Send the reminder via email or SMS
            if email:
                self.send_email(email, subject, message)
                message1 = f"Dear {first_name}"
                list1.append([ email, subject, message1])
            #elif phone:
                # Send the reminder via SMS (assuming the SMS gateway for the carrier...
            

    def schedule_overdue_reminders(self):
            # Schedule the overdue reminders to be sent daily at a specific time (e.g., 9:00 AM)
            schedule.every().day.at("17:21").do(self.send_overdue_reminders1)

            while True:
                # Run the scheduled tasks
                schedule.run_pending()

                 # Wait for 1 second/(minute) before checking the schedule again
                time.sleep(1)
'''


 # Close the connection
#conn.close()