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

The database can then be built with

    (env)$ cd database
    (env)$ ./init_db
    (env)$ cd ..

As much of this as was working from the 2012 web development
class I've copied here, namely the splash page and the data model.

The SQLAlchemy model in src/model.py has doctests which can be seen 
to run with

    (env)$ python src/model.py -v

Any of these tests or other interactive data munging can
also be done from the console.

    (env)$ ./console
    Welcome to planet_express.
    >>> 
    >>> fry = Employee.find_by('name', 'Phillip J. Fry')
    >>> fry
    <Employee name='Phillip J. Fry' id=4343294736>
    >>> fry.shipments
    [<Shipment id=4343295824>, <Shipment id=4343374096>]
    >>> fry.clearances[0].planet.name
    <Planet name='Omicron Persei 8' id=4343375760>

Finally, to see it run, start the server and point a browser
at the right URL. The flask server has a nice debugger - 
try putting an error in one of the templates to see it 
do its thing.

    (env)$ python planet_express.py
    * Running on http://0.0.0.:8090/
    * Restarting with reloader

[github repo]: https://github.com/MarlboroCollegeComputerScience/flask_sql_planet_express


