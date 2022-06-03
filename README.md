<h1>Solution Architect: Coding Challenge
<p>Tyler Berman </h1>


<h2>Phone Number Validation</h2>
<p><h3>Background:</h3>
There is a ton of friction when uploading phone numbers into Klaviyo for SMS consent. 
Often phone numbers are in an improper format, lack a country code or are phone numbers for countries that Klaviyo does not yet support for SMS messaging. 
This is one of our clients' first onboarding steps with SMS & the process can be extremely frustrating when phone #s aren’t successfully imported.

<p><h3>Solution:</h3>
<ol>
<li>Programmatically parse out US phone numbers from a csv file.</li>
<li>Reformat phone numbers into E.164.</li>
<li>Capture country & language as additional properties.</li>
<li>Upload SMS consent.</li>
</ol>
<p><h3>To get started:</h3>
<ol>
<li> Download or clone the repository from Github.</li>
<li> Create an .env file in the base directory of the project.</li> 
<li> Create a Klaviyo account.</li>
<li> Create a List in your Klaviyo account.</li>
<li> Replace the following variables in your script:</li>
    <ol>
        <li>"csv_file_name.csv" - this is the name of your csv file</li>
        <li>PRIVATE - this is the private API key, which you can grab/create from Klaviyo > Accounts > Settings > API keys</li>
        <li>LIST_ID - this is the 6 digit List ID, which you can grab from the Klaviyo List's URL</li>
</ol>
</ol>    
<p><h3>Things to note:</h3>
<ol>
    <li>Ensure your csv file is in the same folder as your script.</li>
    <li>Including sample CSV - smsvalidatetesting.csv - for testing/formatting visualization.</li>
    <li>This script was written, created & debugged using Python 3.9 in PyCharm.</li>
</ol>
<p><h4>Additional questions?</p></h5>
<p>tyler.berman@klaviyo.com</p>
