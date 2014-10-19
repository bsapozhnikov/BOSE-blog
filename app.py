from flask import Flask,render_template,request,redirect
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('blog.db')
c = conn.cursor()

##attr should be a dictionary with attributes as the keys and types as the values
##creat_table('people',{'name':'text','id':'integer'})
def create_table(name, attr):
    L = [k+' '+attr[k] for k in attr.keys()]
    s = ','.join(L)
    c.execute("CREATE TABLE %s(%s)"%(name,s))
    conn.commit()
    #print ("CREATE TABLE %s(%s)")%(name,s)

create_table('posts',{'title':'text','post':'text'})
create_table('comments',{'post':'text','comment':'text'})    

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
        #show post
    else:
        #add comment to post
        #show post
        comment = request.form['comment']


if __name__=='__main__':
    #print create_table('people',{'name':'text','id':'integer'})
    app.debug=True
    app.run()
    
