## Jenkins client
Use this package to perform various jenkins actions such as:  
trigger jobs remotely, poll the jenkins server for the result of a specific build,  
get status of last builds and more.


#### Required to use the client

- Jenkins server url
- Username and password (or API key) for the Jenkins server

#### Example of usage
~~~python
from jenkins_client import JenkinsClient

jc = JenkinsClient(jenkins_base_url="https://my-jenkins-instance.com",
                   username="auto",
                   password=*****)

jc.start_job(job_name, params, wait_for_result, job_poll_interval) # params must be a python dictionary
~~~
_`job_name` parameter is required, the rest are optional._