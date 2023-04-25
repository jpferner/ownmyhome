<h1> Own My Home </h1>
<p> Created by...</p>
<ul>
  <li>David Hollock</li>
  <li>Mark Karels</li>
  <li>Connor McNabb</li>
  <li>Andrew Court</li>
  <li>Jake Ferner</li>
</ul>

<h2> Component Responsibilities </h2>
<ul>
    <li>David Hollock</li>
       <ul>
          <li>Property Search</li>
       </ul>
    <li>Mark Karels</li>
       <ul>
          <li>Checklist</li>
       </ul>
    <li>Connor McNabb </li>
       <ul>
          <li>Calculators</li>
       </ul>
    <li>Andrew Court </li>
       <ul>
          <li>UserManagement</li>
       </ul>
    <li>Jake Ferner </li>
       <ul>
          <li>Calendar</li>
       </ul>
</ul>
<br>

<h2> How to build/run this project </h2>
<h3>This web application runs in python with Flask.</h3> 
<h4>The version we recommend using is 3.10.10</h4>
<h4>To build and run this project:</h4>
<ol>
<li> Download the release repo</li>
<li> Set up a virtual environment with this link [[https://docs.python.org/3/library/venv.html]]</li>
<li> Use the requirements file to install required packages/libraries with pip</li>
<li> Open a command prompt with venv activated in the root directory of this project</li>
<li> To build the database run the next 2 commands</li>
<li> Run the command flask db upgrade</li>
<li> Run the command flask db migrate</li>
<li> Run the command flask run  to start the application</li>
<li> Create an account on the website and you will have access to all features</li>
</ol>


<h1>Testing</h1>

<h2>How to run black box tests for David Hollock</h2>
<ol>
<li> Files needed for these tests are in Tests/Dhollock </li>
<li> They require this version of Chrome browser </li>
<li> The chromedriver must be added to your windows path</li>
<li> Install required packages using the pip requirements file</li>
<li> Activate your virtual environment in command prompt</li>
<li> Run the project using flask run </li>
<li> Create user with email test@gmail.com and password Test123! It is necessary for this user to be in the database</li>
<li> From another command prompt with venv activated from Tests/Dhollock run python test_website.py</li>
<li> Test should open a web browser and run automatically displaying ok in command prompt</li>
</ol>

<h2> How to run black box testing for Jake Ferner's test </h2>
<ol>
<li> User must have firefox binary installed </li>
<li> Run `python Tests/calendar.py (url for testing)`</li>
<li> Enter email and password of existing OwnMyHome account with no calendar events added</li>
<li> Test program will run with no errors for a successful test </li>
</ol><br>

<h2> How to run white box testing for Mark Karels' and Andrew Court's tests </h2>
<ol>
<li>Open terminal in IDE or ensure proper path in Command Prompt/Windows Powershell window</li>
<li>Run the following command: pytest --cov --cov-branch --cov-report html</li>
<li>View the pytest html report to ensure each route being covered has 100% coverage</li>
<li>Those routs should include home(), checklist(), add_checklist_items(), login(), sign_up(), logout(), send_password_reset_email(), reset_password_request(), reset_token(), services(), search(), get_page_token(), get_lat_lng_from_zip()</li>
</ol>
