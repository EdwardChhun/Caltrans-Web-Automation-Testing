This program was created to post ~70 Pilot Projects onto Caltrans' Portal [https://caltrans.brightidea.com/InnovationExchange](https://caltrans.brightidea.com/TransformationalOperationsProcess) for all 12 District including HQ to share "bright ideas". This motive behind this portal is to share previous project efforts to eliminate redundancy, act as a space for innovation and further refinement, and to able all Districts within Caltrans to communicate within Traffic Operations. 

This script uses Python, Selenium, Pandas.

- Python - Programming language that is user friendly enough to enable me to spin up a web automation script on a dynamic website under an hour.
- Selenium - Library I used to open a Google window to act as my canvas to navigate through the [Bright Idea Website](https://caltrans.brightidea.com/TransformationalOperationsProcess). Enabled me to search for input fields, populate text, select and sort parameters that are needed to be posted on to the database portal.
- Pandas - A medium where I used to clean/parse the data from an Excel sheet and convert it into CSV. This enabled me to store all of ~70 pilot projects into a continuous array which I can loop through to popluate the website.

This is the best I am documenting this program. this code will be no longer be maintained as is, unless needed to...

--- 

This is the website that I eventually want to access to upload and populate the website with current pilot projects as of August 2024 (66)
[https://caltrans.brightidea.com/InnovationExchange](https://caltrans.brightidea.com/TransformationalOperationsProcess)

Further on the portal will be the source of populating the projects itself, will no longer be needing this code base to automate for us.

Solutions is to run locally, this was initially on a github codespace env, issues such as authentication arises.
No GUi due to running cloud-base, difficult to navigate complex dynamic site.

Solutions <br></br>
1. Run Locally
2. Access the website and run authentication
3. Move pilot projects file onto local computer
