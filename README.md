# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Type `python server.py` to run the app

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

    We also like to show how well we're testing, so there's a module called 
    [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.
   
   All tests scripts are stored in `tests` directory. Most of the tests are unit tests (in `tests/unit_tests` directory).
   
   An integration test can be found in `tests/integration_tests`.

   There are also some functionnal tests in the `tests/functionnal_tests` directory. Those functionnal tests require you to install `selenium`.
   Installing this framework needs to follow different steps depending on both your Operating System and the Internet Browser you use.
   That's why we recommend you to follow instructions here : https://selenium-python.readthedocs.io/installation.html

   To launch all tests, use the following command : `pytest`. More information is available using the `-v` option : `pytest -v`.

   To perform a specific test, use the following command :`pytest  tests/<test subdirectory>/<test filename>`

   To control the scripts coverage by tests, use  the following command : `pytest --cov`. If you want a detailed report, use the command `pytest --cov --cov-report html` which will genrate a `index.html` file in the `htmlcov` directory. Opening this file in a browser enables you to have more acurate information on coverage testing of this Flask app.



