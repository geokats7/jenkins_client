## Jenkins utility
This is a package able to perform various jenkins actions such as:  
trigger jobs remotely, poll the jenkins server for the result of a specific build,  
get status of last builds and many more.


#### Required to use the client

- Jenkins server url
- Username and password (or API key) for the Jenkins server

#### Example of usage
~~~
from qa_tools.jenkins.jenkins_server import JenkinsServer

js = JenkinsServer(jenkins_base_url="https://ci.orfium.com/jenkins",
                   username="auto",
                   password=*****)

js.start_job(job_name, params) # params must be a python dictionary
~~~

---
###### Contact QA team in order to add more actions to the package.
