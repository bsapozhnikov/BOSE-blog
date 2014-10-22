from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()

app = Flask(__name__)


def create_table(name, attr):
    """Creates a table in the database \'blog.db\'

    1st parameter - name of table (string)
    2nd parameter - Dictionary with keys and types as values'
    """
    print name
    L = [k+' '+attr[k] for k in attr.keys()]
    s = ','.join(L)
    c.execute("CREATE TABLE %s(%s)" % (name, s))
    conn.commit()
    print ("CREATE TABLE %s(%s)") % (name, s)


def drop_table(name):
    c.execute("DROP TABLE %s" % (name))
    conn.commit()
    print ("DROP TABLE %s" % (name))


def add_post(title, cont):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts VALUES ('%s','%s')" % (title, cont))
    conn.commit()
    print "added %s to posts" % (title)


def add_comment(post, cont):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("INSERT INTO comments VALUES ('%s','%s')" % (post, cont))
    conn.commit()
    print "added comment to %s" % (post)


def get_posts():
    """returns a dictionary of posts

    the key of the dictionary is the title of the post
    the value of the dictionary is content
    """
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    posts = {}
    for row in c.execute("SELECT * FROM posts"):
        posts[row[0]] = row[1]
    return posts


def get_comments(post):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    """returns comments from given post"""
    command = "SELECT comment FROM comments WHERE post=?"
    return [row[0] for row in c.execute("%s" % command, (post, ))]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = get_posts()
        print posts
        return render_template('blog.html', posts = posts)
    else:
        # validate and add post to blog
        title = request.form['title']
        post = request.form['post']
        # Currently, there is no validation of the title/post
        add_post(title, post)
        return render_template('blog.html',posts=get_posts())


@app.route('/<title>', methods=['GET', 'POST'])
def show_post(title):
    posts = get_posts()
    comments = get_comments(title)
    if request.method == 'GET':
        return render_template('title.html',title=title,content=posts[title],comments=comments)
        # show post
    else:
        # add comment to post
        # show post
        comment = request.form['comment']
        add_comment(title, comment)
        comments = get_comments(title)
        return render_template('title.html',title=title,content=posts[title],comments=comments)

@app.route("/resetdb")
def create_tables():
    drop_table('posts')
    drop_table('comments')
    create_table('posts', {'title': 'text', 'post': 'text'})
    create_table('comments', {'post': 'text', 'comment': 'text'})
    return redirect("/")

if __name__ == '__main__':
    app.debug = True
    app.run()

