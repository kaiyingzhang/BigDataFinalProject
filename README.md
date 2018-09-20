# Music Recommendation Website

## To use Our project, you need to:
First, install Google SDK, and set up the Google cloud project.
Second, enable Google Cloud Vision API and YouTube Data API v3.
Third, install MogoDB and import the data to database
Last, import v.xiaocase project as a Mavn porject.

## To use the Google API, you need to:
1.Install the Google SDK, which connect your code to Google server.(https://cloud.google.com/sdk/)
2.Go to you Google cloud console, create a project and enable the Google vision API on that project.
3.Go to API manger-Credentials and create a services account key. You will get a Json file. Keep it somewhere, you will need it latter.
4.Open a Terminal, type: gcloud auth application-default login 
You will be asked to login your google account.
5.After login, you will see the default Credentials has been save in some folder. Find that folder and copy the previous Credentials into the folder replace the old one.

## To use MongoDB, you need to:
1.install mongoDB.
2.Import the data use this CMD(in you mongoDB bin folder):
mongoimport --db songs --collection song --type csv --headerline --ignoreBlanks --file /you-file-path/songs.csv

## Now you can run the project without UI.

To run the project on UI, you need to do more:
1.Import the HelloWorld maven project.
2.Place the v.xiaocase-0.0.1-SNAPSHOT.jar in your local computer
3.Change the path to your v.xiaocase-0.0.1-SNAPSHOT.jar location in HelloWorld.java:
