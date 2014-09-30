# history.txt

See ../README.md for an overview, 
and the [GitHub repository][github repo] for the version history.

## Sep 30 2014

I'm building on the Fall 2012 Planet Express Flask SQL thingy
I did, starting with a fresh GitHub repo and copying files
from the 2012 effort here.

### installing the software

First I created a bare GitHub template on their site in the 
MarlboroCollegeComputerScience, MIT License & python gitignore.

Then I setup working folder on my mac laptop

  $ git clone git@github.com:MarlboroCollegeComputerScience/flask_sql_planet_express.git

With that in place, my regular work flow is

    # edit laptop files
    $ git add <files>
    $ git commit <files> -m "..."
    $ git push

Setting up the python virutal environment

    $ python --version
    Python 2.7.8
    $ virtualenv --version
    1.9.1
    $ virtualenv -p python2.7 env

Put an alias in a shell startup file (i.e. ~/.profile or ~/.bashrc)
that lets you type "activate" in a project folder to activate virtualenv.

    # ~/.profile ---
    alias activate=". env/bin/activate"

Then once that alias is on (new shell or ". ~/.profile")

    $ activate
    (env)$               # virtualenv prompt
    (env)$ which python  # Now using local python?
    ./env/bin/python     # Yup.

The ./requirements.txt file lists the other software needed.
The ones that need to be installed manually (i.e. apt-get 
or whatever) are python, virtualenv, git, and sqlite3. 
The rest are python packages that the virtualenv version
of pip will can install within the local ./env from
the requirements.txt file.

    (env)$ pip install -r requirements.txt




[github repo]: https://github.com/MarlboroCollegeComputerScience/flask_sql_planet_express


