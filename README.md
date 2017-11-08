# CA674-Cloud-Architecture

<p> The aim of this project was to take a previously hosted application (http://hnkatwe.com/) and migrate it to a new platform.</p>

<p> This application was built using the Flask web framework and Docker. The application has gone from a static website to one where:
  <ul>
    <li>Users can register an account with the site</li>
    <li>Users can edit their profiles</li>
    <li>Confirmation Emails are sent to confirm User accounts</li>
    <li>Admins can add new books</li>
    <li>Books can be reviewed by Users</li>
    <li>Books now have a rating based on their reviews</li>
    <li>Users can submit Enquiries to Admins</li>
   </ul>
</p>

You can run this application using Docker or by itself standalone.

<h2>Without Docker</h2>
<ol>
  <li> Install PostgreSQL (https://www.postgresql.org/download/) and create database table users-dev</li>
  <li> Clone repo and cd new directory</li>
  <li> Create .env file and set <code>DEV_DATABASE_URL='postgresql://localhost/devdb'</code></li>
  <li> Run <code> python manage.py runserver</code></li>
  <li> Navigate to http://127.0.0.1:5000/</li>
 </ol>
 
 <h2>With Docker</h2>
 <ol>
  <li> Install Virtualbox (https://www.virtualbox.org/wiki/Downloads)</li>
  <li> Create new Docker machine using <code>docker-machine create -d virtualbox dev</code></li>
  <li> Run <code> eval "$(docker-machine env dev)"</code></li>
  <li> Run <code> docker-compose up -d --build </code></li>
  <li> Navigate to ip received from <code>docker-machine ip dev</code></li>
</ol>
