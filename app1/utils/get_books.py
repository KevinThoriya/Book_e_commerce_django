import requests
from bs4 import BeautifulSoup
import random

def get_python_book_from_url(url):
    req = requests.get(url) 
    soup = BeautifulSoup(req.text, "lxml")
    books = soup.find_all(class_="section3")
    Books_data = []
    for book in books:
        book_data = {}
        book_data['book_name'] = book.find('h3').text[:-1]
        book_details = book.find_all('p')
        book_data['book_author'] = book_details[0].text
        book_data['book_img'] = book_details[1].find('img').get('src')
        book_data['book_desc'] = book_details[2].text + book_details[3].text
        book_data['book_price'] = '$' + str(random.randint(15,99)) + '.' + str(random.randint(15,99))  
        Books_data.append(book_data)
    return Books_data



def get_java_book_from_url(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    books_div = soup.find(class_='blog-content')
    books_name = []
    book_author = [] 
    book_disc = []
    book_img = []
    for book in books_div.find_all('ol')[2:]:
        books_name.append(book.find('h2').text) 
    
    for author in books_div.select('p > strong, p > b'):
        if (author.text[:6] == 'Author'):
            book_author.append(author.text)

    parent_p_list = []
    for log_disc in books_div.select('p > span'):
        if log_disc.parent in parent_p_list:
            book_disc[-1] += '\n' + log_disc.text
        else :
            book_disc.append(log_disc.text)
            parent_p_list.append(log_disc.parent)
    book_disc = book_disc[:-2]

    for img in books_div.select('img'):
        if(img.get('data-src')):
            book_img.append(img.get('data-src'))
        else:
            book_img.append('https://www.edureka.co' + img.get('src'))

    returnto = []
    for i in range(10):
        book_price = '$' + str(random.randint(15,99))+ '.' +str(random.randint(15,99))  
        returnto.append({'book_price':book_price, 'book_name': books_name[i],'book_author': book_author[i],'book_img': book_img[i],'book_desc': book_disc[i]})

    return returnto

def get_book_from_amazon(url,book_for):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    books_div = []
    for i in soup.select('.zg-item'):
        if i.select('.a-size-small.a-color-secondary')[0].text == 'Paperback':
            books_div.append(i)

    books_detail = []
    for book_div in books_div:
        book_detail = {}
        book_detail['book_img'] = book_div.find('img').get('src')
        book_detail['book_name'] = book_div.select('a.a-link-normal > div')[0].text #if book_div.select('.p13n-sc-truncated') else 'My New Book'
        book_detail['book_author'] = book_div.find('a',class_ = 'a-size-small').text.strip() if book_div.find('a',class_ = 'a-size-small') else 'kevin' 
        book_detail['book_price'] = book_div.select('span.p13n-sc-price')[0].text
        if book_for == 'js':
            book_detail['book_desc'] = """
                The use of JavaScript has expanded beyond its web browser roots. JavaScript engines are now embedded in a variety of other software systems, both for server-side website deployments and non-browser applications.
                Initial attempts at promoting server-side JavaScript usage were Netscape Enterprise Server and Microsoft's Internet Information Services, but they were small niches.[32] Server-side usage eventually started to grow in the late-2000s, with the creation of Node.js and other approaches.
                Electron, Cordova, and other software frameworks have been used to create many applications with behavior implemented in JavaScript. Other non-browser applications include Adobe Acrobat support for scripting PDF documents[33] and GNOME Shell extensions written in JavaScript.
                JavaScript has recently begun to appear in some embedded systems, usually by leveraging Node.js."""
        elif book_for == 'php':
            book_detail['book_desc'] = """
                PHP is an acronym for "PHP: Hypertext Preprocessor"
                PHP is a widely-used, open source scripting language
                PHP scripts are executed on the server
                PHP is free to download and use
                PHP can generate dynamic page content
                PHP can create, open, read, write, delete, and close files on the server
                PHP can collect form data
                PHP can send and receive cookies
                PHP can add, delete, modify data in your database
                PHP can be used to control user-access
                PHP can encrypt data
            """
        elif book_for == 'asp.net':
            book_detail['book_desc'] = """
                .NET is a developer platform made up of tools, programming languages, and libraries for building many different types of applications.
                The base platform provides components that apply to all different types of apps. Additional frameworks, such as ASP.NET, extend .NET with components for building specific types of apps.
            """
        elif book_for == 'css':
            book_detail['book_desc'] = """
                CSS stands for Cascading Style Sheets
                CSS describes how HTML elements are to be displayed on screen, paper, or in other media
                CSS saves a lot of work. It can control the layout of multiple web pages all at once
                External stylesheets are stored in CSS files
            """
        elif book_for == 'rubi':
            book_detail['book_desc'] = """
            Rubi is a real gem. She has a free spirit that cannot be bound. She is kind, loving and caring. Rubi is a person that any man would be lucky to have by his side. She is direct, honest, sticks up for her values and she can achieve anything she sets her mind to. If you know a Rubi, don't let her out of your sight. Be it as a friend or a lover, she will only add to the richness of your life.
            """
        elif book_for == 'complier':
            book_detail['book_desc'] = """
            In computing, a compiler is a computer program that translates computer code written in one programming language (the source language) into another language (the target language). The name "compiler" is primarily used for programs that translate source code from a high-level programming language to a lower level language (e.g., assembly language, object code, or machine code) to create an executable program
            """
        books_detail.append(book_detail)

    return books_detail





def getAllBook():
    returnto = {}
    print("Going to get all Book")
    returnto['JavaScript'] = get_book_from_amazon('https://www.amazon.com/Best-Sellers-Books-JavaScript-Programming/zgbs/books/3617','js');
    returnto['PHP'] = get_book_from_amazon('https://www.amazon.com/Best-Sellers-Books-PHP-Programming/zgbs/books/295223','php');
    returnto['ASP_NET'] = get_book_from_amazon('https://www.amazon.com/Best-Sellers-Books-ASP-NET-Programming/zgbs/books/379360011','asp.net');
    returnto['CSS'] = get_book_from_amazon('https://www.amazon.com/Best-Sellers-Books-CSS-Programming/zgbs/books/379357011','css');
    returnto['Rubi'] = get_book_from_amazon('https://www.amazon.com/Best-Sellers-Books-Ruby-Programming/zgbs/books/6134006011','rubi');
    returnto['Compiler'] = get_book_from_amazon('https://www.amazon.com/Best-Sellers-Books-Software-Programming-Compilers/zgbs/books/3971','complier');
    returnto['Python'] = get_python_book_from_url("https://realpython.com/best-python-books/")
    returnto['Java'] = get_java_book_from_url('https://www.edureka.co/blog/top-10-books-to-learn-java/')
    print("Done geting all Book")

    return returnto