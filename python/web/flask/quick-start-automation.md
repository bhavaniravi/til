---
added: Aug 04 2022
draft: false
image: null
layout: ../layouts/BlogPost.astro
slug: quick-start-automation
sub_title: Start here for your 1st flask script
tags:
- flask
title: Quick Start Automation
---

# Quick Start Automation

Every time I want to start a flask project I will create a directory strucutre and create files. Copy the quick start tempalate from Flask docs and then run the app. Too much work, right?

So I've automated it by adding a small script to my `~/.zshrc` file. If you are using bash this will be `~/.bashrc` for you

Add the following to your rc file

{% code title="~/.bashrc or ~/.zshrc" %}
```
flaskapp() {
    mkdir $1
    cd $1  
    python3 -m venv venv
    source venv/bin/activate
    pip install flask
    touch hello.py
    
    // echo command starts here
    echo "
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return '<p>Hello, World!</p>'
    
    
    @app.route('/user/<username>')
    def show_user_profile(username):
        # show the user profile for that user
        return f'User {escape(username)}'
    
    @app.route('/post/<int:post_id>')
    def show_post(post_id):
        # show the post with the given id, the id is an integer
        return f'Post {post_id}'
    
    if __name__ == '__main__':
    	app.run(port=8000, debug=True)
    " > hello.py
    
    // echo command ends here
}
```
{% endcode %}

Run `source ~/.zshrc` or restart your terminal

### Setup The App

Now everytime you need a new app all you have to do is go to your terminal and write

```
flaskpp
```

* It will create a new directory
* Create a virtualenv
* Create a sample hello world file

### Run the App

`python hello.py`

### Test the API

1. Open the browser
2. Hit the following URLs

```
https://loaclhost:8000/
https://loaclhost:8000/post/10
https://loaclhost:8000/user/Tom
```