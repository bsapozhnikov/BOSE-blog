from flask import Flask,render_template,request,redirect
import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()

app = Flask(__name__)

##attr should be a dictionary with attributes as the keys and types as the values
def create_table(name, attr):
    print name
    L = [k+' '+attr[k] for k in attr.keys()]
    s = ','.join(L)
    c.execute("CREATE TABLE %s(%s)"%(name,s))
    conn.commit()
    print ("CREATE TABLE %s(%s)")%(name,s)

def drop_table(name):
    c.execute("DROP TABLE %s"%(name))
    conn.commit()
    print ("DROP TABLE %s"%(name))

def add_post(title,cont):
    c.execute("INSERT INTO posts VALUES (%s,%s)"%(title,cont))
    conn.commit()
    print "added %s to posts"%(title)

def add_comment(post,cont):
    c.execute("INSERT INTO comments VALUES (%s,%s)"%(post,cont))
    conn.commit()
    print "added comment to %s"%(post)

##returns a dictionary of posts in the form 'title':'post'
def get_posts():
    posts={}
    for row in c.execute("SELECT title FROM posts"):
        posts[row[0]]=row[1]
    return posts

##return a list of comments for the given posts
def get_comments(post):
    return [row[0] for row in c.execute("SELECT comment FROM comments WHERE post=?",(post,))]
    
@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('blog.html')
    else:
        #validate and add post to blog
        title = request.form['title']
        post = request.form['post']
        #Currently, there is no validation of the title/post
        add_post(title,post)
        
        

@app.route('/<title>', methods=['GET','POST'])
def show_post(title):
    if request.method=='GET':
        pass
        #show post
    else:
        #add comment to post
        #show post
        comment = request.form['comment']
        add_comment(title,comment)
        
@app.route("/resetdb")
def create_tables():
    drop_table('posts')
    drop_table('comments')        
    create_table('posts',{'title':'text','post':'text'})
    create_table('comments',{'post':'text','comment':'text'})    
    return redirect("/")

if __name__=='__main__':
    app.debug=True
    app.run()
  
    
