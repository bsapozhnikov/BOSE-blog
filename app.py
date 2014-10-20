from flask import Flask,render_template,request,redirect
import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()

app = Flask(__name__)

##attr should be a dictionary with attributes as the keys and types as the values
##create_table('people',{'name':'text','id':'integer'})
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

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('blog.html')
    else:
        #validate and add post to blog
        title = request.form['title']
        post = request.form['post']
        

@app.route('/<title>', methods=['GET','POST'])
def show_post(title):
    if request.method=='GET':
        pass
        #show post
    else:
        #add comment to post
        #show post
        comment = request.form['comment']

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
    #drop_table('posts')
    #drop_table('comments')
    
