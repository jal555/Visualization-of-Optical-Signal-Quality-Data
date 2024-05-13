# Analysis and Visualization of Optical Signal Quality Data

This project, titled “Analysis and Visualization of Optical Signal Quality Data,” is a significant attempt aimed at enhancing our understanding and interpretation of optical signal quality data. Since April of 2023, large JSON files have been meticulously compiled, with each file representing just a day’s worth of optical signal quality data from labs across New York state. The sheer volume of these files currently makes it challenging to comprehend the data in its raw form. Here is where the importance of this project lies: by parsing all of the data and developing a dashboard to visualize it, each JSON file is transformed from its raw form into visual representations that can easily be understood and analyzed. Not only will this aid in the identification of patterns and trends among the data, but it will also visualize dips in signal quality. The analysis of the data using a dashboard is pivotal to the enhancement of the overall performance and reliability of each optical signal. Therefore, this project aims to transform massive amounts of data into meaningful and accessible insights.

## Architecture and Dependencies

The entire project was executed using Python 3.12.3, which was utilized for parsing the data, generating graphs, building the dashboard, and creating a linear regression model. A virtual environment was set up in Conda to manage all the dependencies required for the project. The details of these dependencies can be found in the environment.yml file.

## Setup
As the dashboard is deployed locally and not hosted publicly, the following steps must be followed to install and set up the project:

1.) Clone the Repository: Clone the GitHub repository to your local machine using the command: 
```bash
git clone https://github.com/jal555/Visualization-of-Optical-Signal-Quality-Data.git
```
2.) Navigate to the Repository Folder: Change your directory to the cloned repository folder.

3.) Create and Activate the Virtual Environment: Use Conda to create and activate a virtual environment with the commands:
```bash
conda env create -f environment.yml
conda activate vis-opt-sig-data
```
4.) Install Python: Ensure that Python 3.12.3 is installed as it is necessary to run the script.

5.) Run the Script: Execute the script using the command:
```bash
python visualize_data.py <USER> <PASSWORD>
```
Please note that you must provide your username and password to access the lambda1.cs.cornell.edu server where the data is stored. You must also be connected to the Cornell University campus WiFi or using the Cornell University VPN, as well as have access to the server. The script should take around 15-20 minutes to finish running completely.

6.) View the Dashboard: Navigate to http://127.0.0.1:8050/ on your machine to view the dashboard. Please allow a minute or two for the dashboard to load completely.
