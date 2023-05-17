from flask import Flask, render_template, redirect, url_for, request, flash,session
from implement import Library, User, DEFAULT_PASSWORD

from flask_login import LoginManager
import mysql.connector
import schedule
import time
import threading



app = Flask(__name__)
library = Library('localhost', 'root', 'syl21b', 'proj1')
app.secret_key = '123456798'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



# Define a route to display the list of books
@app.route('/list')
def list():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='syl21b',
        database='proj1'
    )
    # Create a cursor
    cur = conn.cursor()

    # Execute a query to get all books from the database
    cur.execute('SELECT * FROM Book')
    books = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Render the list of books in HTML table format using the template 'list.html'
    return render_template('list.html', books=books)




# Home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_type = request.form.get('user-type')
        if user_type:
            if user_type == "librarian":
                #with library as lib:
                    #lib.schedule_overdue_reminders()
                return redirect(url_for('librarian'))
            elif user_type == "member":
                return redirect(url_for('member'))
        flash('Invalid user type')
    return render_template('index.html')


# Options page
@app.route('/options', methods=['POST'])
def options():
    user_type = request.form['user_type']
    if user_type == 'librarian':
        return render_template('librarian.html')
    elif user_type == 'member':
        return render_template('member.html')
    else:
        flash('Invalid user type')
        return redirect(url_for('options'))

'''
# Librarian page
@app.route('/librarian')
def librarian():
    # code to render the librarian page
    return render_template('librarian.html')


# Member page
@app.route('/member')
def member():
    # code to render the member page
    return render_template('member.html')
'''

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from form data
        username = request.form['username']
        password = request.form['password']
        
        with library as lib:
            #if lib.log_in(username, password):
                # Check if the user is a librarian or a member
                #user_type = lib.get_user_type(username)
                user_type =lib.log_in(username, password)
                if user_type == 'librarian':
                    # User is a librarian, redirect to the librarian page
                    return render_template('base_librarian.html', librarian_id=username)
                elif user_type == 'member':
                        # User is a member, redirect to the member page
                        return render_template('base_member.html', member_id=username)
                else:
                    # User is neither a librarian nor a member, show an error message
                    message = "Invalid user ID or password."
                    return render_template('login.html', message=message)
            #else:
                # Invalid credentials, show an error message
                #flash('Invalid username or password')
                #message = "Invalid user ID or password."
                #return render_template('login.html', message=message)
    
    return render_template('login.html')
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        phone_number = request.form['phonenumber']
        email = request.form['email']
        user_id = request.form['userid']
        password = request.form['password']
        
            
        with library as lib:
            if not lib.create_new_member(first_name, last_name, phone_number, email, user_id, password):
                message = 'New member record created successfully.'
                return render_template('login.html', message= message)
            else:
                message = 'The User ID already exists in the system. Please enter a new ID.'
                return render_template(message= message)
    else:
        return render_template('create_member.html')

    
# Logout the current user
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return render_template('index.html')







###################################################
@app.route('/update-member', methods=['GET', 'POST'])
def update_member():
    if request.method == 'POST':
        member_id = request.form['member_id']
        change_phone = request.form['change_phone']
        change_email = request.form['change_email']
       # borrow_book = request.form['borrow_book']
        new_phone_number = request.form['phone_number']
        new_email_address = request.form['email']
        #book_id = request.form['book_id']
        #issue_date = request.form['issue_date']
        #return_status = request.form['return_status']
        change_password = request.form['change_password']
        new_password = request.form['password']

        with library as lib:
            message1=''
            if change_phone == 'yes':
                memberexist = lib.update_member_phone(member_id, new_phone_number)
                message1 += 'phone number, '  
                if  memberexist == 'Member ID not found':
                    return render_template('update-member.html', message=memberexist)
            
            
            if change_email == 'yes':
                memberexist =lib.update_member_email(member_id, new_email_address)
                message1 += 'email, '
                if  memberexist == 'Member ID not found':
                    return render_template('update-member.html', message=memberexist)
           
           # if borrow_book == 'yes':
            #    lib.borrow_book(member_id, book_id, issue_date, return_status)
            if change_password == 'yes':
                memberexist =lib.update_member_password(member_id, new_password)
                message1 += 'password'
                if  memberexist == 'Member ID not found':
                    return render_template('update-member.html', message=memberexist)
            
            result = lib.display_member_info(member_id)
            message = 'You have updated successfully: ' + message1
            return render_template('display_member_info.html', message=message, member_id=member_id, result=result)
    else:
        #librarian_id = request.args.get('librarian_id')
        #return render_template('update-member.html', librarian_id=librarian_id)
        return render_template('update-member.html')

@app.route('/delete-member', methods=['GET', 'POST'])
def delete_member():
    if request.method == 'POST':
        member_id = request.form['member_id']
        delete_account = request.form['delete_account']
        if delete_account == 'yes':
            with library as lib:
                result = lib.delete_member(member_id)
                if result == 'Membership deleted successfully!':
                    return render_template('delete-member.html',message=result)
                if  result =='Member ID not found':
                    return render_template('delete-member.html', message=result)
                if result == 'Cannot delete member with borrow records':
                    return render_template('delete-member.html',  message=result+'. The member must return the book before deleting the account.')
        else:
            message ='Your account still exists.'
            return render_template('base_member.html', message=message, member_id = member_id )   
    else:
        member_id = request.args.get('member_id')
        return render_template('delete-member.html', member_id=member_id)
    
    
@app.route('/display_member_info', methods=['GET', 'POST'])    
def display_member_info():
    if request.method == 'POST':
        member_id = request.form['member_id']
    else: 
        member_id = request.args.get('member_id')
    with library as lib:
        result = lib.display_member_info(member_id)
    return render_template('display_member_info.html', member_id=member_id, result=result)


####################LIBRARIAN###################################   
@app.route('/create-librarian', methods=['GET', 'POST'])
def create_librarian():
    if request.method == 'POST':
        
        main_librarian_id = request.args.get('librarian_id')
        
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        phone_number = request.form['phonenumber']
        user_id = request.form['userid']
        #password = request.form['password']
        password= DEFAULT_PASSWORD
        with library as lib:
            if not lib.create_librarian(first_name, last_name, phone_number, user_id):
                message ='A new librarian account has been created successfully!' +' The default password is: ' +password
                return render_template('base_librarian.html', message= message,librarian_id=main_librarian_id)
            else:
                message = 'The User ID already exists in the system. Please enter a new ID.'
                return render_template('create_librarian.html',message= message,librarian_id=main_librarian_id)
    else:
        librarian_id = request.args.get('librarian_id')
        return render_template('create_librarian.html', librarian_id=librarian_id)
 
@app.route('/update_librarian', methods=['GET', 'POST'])
def update_librarian():
    librarian_id = None  # define a default value for librarian_id
    if request.method == 'POST':
        librarian_id = request.form['librarian_id']
        change_phone = request.form['change_phone']
        new_phone_number = request.form['phone_number']
        change_password = request.form['change_password']
        new_password = request.form['password']

        with library as lib:
            if change_phone == 'yes':
                lib.update_librarian_phone(librarian_id, new_phone_number)
            if change_password == 'yes':
                lib.update_librarian_password(librarian_id, new_password)
            message='Librarian information updated successfully'
            return render_template('update_librarian.html', librarian_id=librarian_id,message=message)
           
    else:
        librarian_id = request.args.get('librarian_id')
        return render_template('update_librarian.html', librarian_id=librarian_id)

@app.route('/delete_librarian', methods=['GET', 'POST'])
def delete_librarian():
    if request.method == 'POST':
        main_librarian_id = request.args.get('librarian_id')
        
        librarian_id = request.form['librarian_id1']
        choice = request.form['choice']
        if choice == 'yes':
            with library as lib:
                result =lib.delete_librarian(librarian_id)
                if result == 'Librarian record deleted successfully!':
                    message = "You have just deleted the ID: " + librarian_id
                    return render_template('base_librarian.html', message= message, librarian_id=main_librarian_id)
                else:
                    return render_template('delete_librarian.html', message = result,librarian_id=main_librarian_id)
        else:
            message = "You do not delete the account: " + librarian_id
            return render_template('base_librarian.html', message= message, librarian_id=main_librarian_id)
    else:
        librarian_id = request.args.get('librarian_id')
        return render_template('delete_librarian.html',librarian_id=librarian_id)

########################BOOK######################
@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        member_id = request.form['member_id']
        book_id = request.form['book_id']
        issue_date = request.form['issue_date']
        with library as lib:
            result = lib.borrow_book(member_id, book_id, issue_date)
            if result == "success":
                message= 'Book borrowed successfully.'
                result = lib.display_member_info(member_id)
                return render_template('display_member_info.html',message=message, member_id = member_id, result = result)
            if result == 'Book ID not found':
                message= 'Book ID not found'
                return render_template('borrow.html',message=message,member_id = member_id)
            if result == 'Book not available':
                message= 'Book not available'
                return render_template('borrow.html',message=message,member_id = member_id)
            if result =='Currently borrow a book':
                message= 'You are borrowing a book. Please return it to be able to borrow a new one!'
                return render_template('borrow.html',message=message,member_id = member_id)
    else:
        member_id = request.args.get('member_id')
        return render_template('borrow.html',member_id = member_id)
    
@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        member_id = request.form['member_id']
        book_id = request.form['book_id']
        returnstatus = request.form['returnstatus']
        if returnstatus =='No':
            return render_template('return.html')
        with library as lib:
            result = lib.return_book(member_id, book_id, returnstatus)
            if result == 'Book returned successfully':
                #message= 'Book returned successfully'
                result = lib.display_member_info(member_id)
                return render_template('display_member_info.html',message=result,member_id = member_id, result =result )
            elif result == 'Book ID not found':
                #message= 'Book ID not found'
                return render_template('return.html',message=result,member_id = member_id)
            elif result == 'Book not borrowed':
                #message= 'Book not borrowed'
                return render_template('return.html',message=result,member_id = member_id)
            else:
                #message= 'The book is not borrowed by the member'
                return render_template('return.html',message=result,member_id = member_id)
    else:
        member_id = request.args.get('member_id')
        return render_template('return.html', member_id=member_id)



@app.route('/update-book', methods=['GET', 'POST'])
def update_book():
    if request.method == 'POST':
        librarian_id = request.args.get('librarian_id')
        
        book_id = request.form['book_id']
        isbn = request.form['isbn']
        title = request.form['title']
        genre = request.form['genre']
        author = request.form['author']
        year = request.form['year']
        publisher = request.form['publisher']
        URL = request.form['URL']
        
        isbn_choice = request.form.get('isbn_choice')
        title_choice = request.form.get('title_choice')
        genre_choice = request.form.get('genre_choice')
        author_choice = request.form.get('author_choice')
        year_choice = request.form.get('year_choice')
        publisher_choice = request.form.get('publisher_choice')
        url_choice = request.form.get('url_choice')
        
        with library as lib:
            result = lib.check_book_id(book_id)
            if result == 'Book ID not found':
                return render_template('update-book.html')
            else:
                message = 'Book information updated successfully!'
                if isbn_choice=="yes":
                    lib.update_isbn(isbn, book_id)
                    message += ' ISBN updated'
                if title_choice=="yes":
                    lib.update_title(title, book_id)
                    message += ' Title updated'
                if genre_choice=="yes":
                    lib.update_genre(genre, book_id)
                    message += ' Genre updated'
                if author_choice=="yes":
                    lib.update_author(author, book_id)
                    message += ' Author updated'
                if year_choice=="yes":
                    lib.update_year(year, book_id)
                    message += ' Year updated'
                if publisher_choice=="yes":
                    lib.update_publisher(publisher, book_id)
                    message += ' Publisher updated'
                if url_choice=="yes":
                    lib.update_url(URL, book_id)
                    message += ' URL updated'
                
                return render_template('base_librarian.html',message =message, librarian_id= librarian_id)
    else:
        librarian_id = request.args.get('librarian_id')
        return render_template('update-book.html',librarian_id= librarian_id)

    
@app.route('/create_book', methods=['GET','POST'])
def create_book():
    
    if request.method == 'POST':
        librarian_id = request.args.get('librarian_id')
        
        isbn = request.form['isbn']
        title = request.form['title']
        genre = request.form['genre']
        author = request.form['author']
        year = request.form['year']
        publisher = request.form['publisher']
        url1 = request.form['url1']
        with library as lib:
            message, book_id = lib.create_new_book(isbn, title, genre, author, year, publisher, url1)
            messge= message+ 'with Book ID: ' +str(book_id)
            
        return render_template('base_librarian.html',message =messge, librarian_id= librarian_id)
    else:
        librarian_id = request.args.get('librarian_id')
        return render_template('create_book.html',librarian_id= librarian_id) 
    
@app.route('/delete-book', methods=['GET', 'POST'])
def delete_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        
        with library as lib:
            message =lib.delete_book(book_id)
            # Delete the book record
            if message=='Book record deleted successfully':
                return message
            if message=='Book ID not found':
                return 'Book ID does not exist'
            if message=='The book is currently being borrowed':
                return message
    else:
        return render_template('delete-book.html') 



#______QUERIES______________________________________________________________________________________________________  
# Member page
@app.route('/features')
def features():
    librarian_id = request.args.get('librarian_id')

    # code to render the member page
    return render_template('features.html',librarian_id=librarian_id)


@app.route('/available_books_count')
def get_available_books_count():
        with library as lib:
            result, books = lib.get_available_books_count()
            message ='There are ' + str(result) +" available."
        return render_template('available_books_count.html', message= message, books=books)

@app.route('/overdue-members', methods=['GET'])
def overdue_members():
    with library as lib:
        result = lib.get_overdue_members()
        if result:
            message ='overdue-members'
            return render_template('overdue-members.html',message = message, result=result)
        else:
            return  'No overdue members found'
        
@app.route('/get_books_by_member', methods=['GET'])
def get_books_by_member():
    member_id = request.args.get('member_id')
    with library as lib:
        book, message = lib.get_books_by_member(member_id)
        return render_template('get_books_by_member.html',message = message, book=book, member_id=member_id)
     

#____________________________________________________________________________________________________________  
@app.route('/search')
def search():
    member_id = request.args.get('member_id')

    # code to render the member page
    return render_template('search.html',member_id = member_id)

@app.route('/available_books_by_genre', methods=['GET'])
def available_books_by_genre():
    genre = request.args.get('genre')
    with library as lib:
        book, message = lib.get_available_books_by_genre(genre)
        return render_template('available_books_by_genre.html',message = message, book=book, genre=genre)
    
# Define a route that groups books by their genre and returns the count of books in each group
@app.route('/books_by_genre', methods=['GET'])
def books_by_genre():
    with library as lib:
        list1 = lib.count_books_by_genre()
        return render_template('count_books_by_genre.html',list1 = list1)     

@app.route('/get_book_by_isbn', methods=['GET'])
def get_book_by_isbn():
        # Get the book with the given ISBN number
        isbn = request.args.get('isbn')
        with library as lib:
            book, message = lib.get_book_by_isbn( isbn)
            return render_template('get_book_by_isbn.html',message = message, book=book, isbn=isbn)
     
@app.route('/get_book_by_author', methods=['GET'])
def get_book_by_author():
        # Get the book with the given author
        author = request.args.get('author')
        with library as lib:
            book, message = lib.get_book_by_author( author)
            return render_template('get_book_by_author.html',message = message, book=book, author=author)
     
@app.route('/get_book_by_year', methods=['GET'])
def get_book_by_year():
        # Get the book with the given year
        year = request.args.get('year')
        with library as lib:
            book, message = lib.get_book_by_year( year)
            return render_template('get_book_by_year.html',message = message, book=book, year=year)
    
@app.route('/get_book_by_publisher', methods=['GET'])
def get_book_by_publisher():
        # Get the book with the given publisher
        publisher = request.args.get('publisher')
        with library as lib:
            book, message = lib.get_book_by_publisher( publisher)
            return render_template('get_book_by_publisher.html',message = message, book=book, publisher=publisher)


@app.route('/get_book_by_keyword', methods=['GET'])
def get_book_by_keyword():
        # Get the book with the given publisher
        keyword = request.args.get('keyword')
        with library as lib:
            book, message = lib.get_book_by_keyword( keyword)
            return render_template('get_book_by_title.html',message = message, book=book, keyword=keyword)



#____________________________________________________________________________________________________________  


@app.route('/show_record_by_memberid', methods=['GET'])
def show_record_by_memberid():
    member_id = request.args.get('member_id')
    with library as lib:
        book, message = lib.show_record_by_memberid( member_id)
        return render_template('show_record_by_memberid.html', message = message, book=book, member_id=member_id)
        
@app.route('/last_borrow_book_by_memberid', methods=['GET'])
def last_borrow_book_by_memberid():
    member_id = request.args.get('member_id')
    with library as lib:
        book, message = lib.last_borrow_book_by_memberid( member_id)
        return render_template('last_borrow_book_by_memberid.html', message = message, book=book, member_id=member_id)
   
@app.route('/get_member_info_borrowing_book', methods=['GET'])
def get_member_info_borrowing_book():
    book_id = request.args.get('book_id')
    with library as lib:
        result, message = lib.get_member_info_borrowing_book(book_id)
        if result is None:
            result = []  # set result to an empty list if it is None
        return render_template('get_member_info_borrowing_book.html', message=message, book_id=book_id, result=result)


#______ADVANCED FUNCTION___OVERDUE AND REMINDER__________________________________________________________________________
# Define the route for sending overdue reminders via email or SMS
@app.route('/send_overdue_reminders')
def send_overdue_reminders():
    #sending overdue reminders here
    with library as lib:
        list1=lib.send_overdue_reminders()
        message="Overdue reminders sent successfully!"
        return render_template('send_overdue_reminders.html', message=message,list1=list1)

# Define the function to schedule overdue reminders to be sent daily
def schedule_overdue_reminders():
    # Schedule the overdue reminders to be sent daily at a specific time (e.g., 9:00 AM)
    schedule.every().day.at("15:13").do(send_overdue_reminders)

    while True:
        # Run the scheduled tasks
        schedule.run_pending()

        # Wait for 60 second before checking the schedule again
        time.sleep(60)

# Start the scheduler in a separate thread
def start_scheduler():
    with app.app_context():
        schedule_overdue_reminders()

if __name__ == '__main__':
    # Start the scheduler thread
    scheduler_thread = threading.Thread(target=start_scheduler)   #This allows the Flask application to continue handling other requests while the scheduler is running.
    scheduler_thread.start()

    # Run the Flask application
    app.run(debug=True)