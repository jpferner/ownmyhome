[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/t1dqGhBU)

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
[Tests](Tests)
<h2> How to build/run this project </h2>
<h3>This web application runs in python with Flask.</h3> 
<h4>The version we recommend using is 3.10.10</h4>
<h4>To build and run this project:</h4>
<ol>
<li> Download the release repo</li>
<li> Set up a virtual environment with this link [[https://docs.python.org/3/library/venv.html]]</li>
<li>Use the requirements file to install required packages/libraries with pip</li>
<li>Run app.py to start the application.</li>
</ol>

<h2> Running user tests </h2>
<h3> Calendar page </h3>
<ol>
<li> User must have firefox binary installed </li>
<li> Run `python Tests/calendar.py <url for testing>`</li>
<li> Enter email and password of existing OwnMyHome account with no calendar events added</li>
<li> Test program will run with no errors for a successful test </li>
</ol>
</ol><br>

<h2> How to run white box testing for Mark Karels' and Andrew Court's tests </h2>
<ol>
<li>Open terminal in IDE or ensure proper path in Command Prompt/Windows Powershell window</li>
<li>Run the following command: pytest --cov --cov-branch --cov-report html</li>
<li>View the pytest html report to ensure each route being covered has 100% coverage</li>
<li>Those routs should include home(), checklist(), add_checklist_items(), login(), sign_up(), logout(), send_password_reset_email(), reset_password_request(), reset_token(), services(), search(), get_page_token(), get_lat_lng_from_zip()</li>
</ol>
