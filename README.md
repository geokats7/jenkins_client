## Jenkins client
Use this package to perform various jenkins actions such as:
trigger jobs remotely, poll the jenkins server for the result of a specific build,
get status of last builds and more.


#### Required to use the client

- Jenkins server url
- Username and password (or API key) for the Jenkins server

#### Example of usage
```
from jenkins_client import JenkinsClient

jc = JenkinsClient(jenkins_base_url='https://my-jenkins-instance.com',
                   username='auto',
                   password='*****')

jc.start_job(job_name='job_name', params={'param_key':'param_value'}) # params must be a python dictionary
```

### GitHub Action usage
You can use this package as a GitHub Action to trigger a job remotely and optionally wait for the job's result.
The action parameters are the following:

| Parameter                          | Required  | Description                                                                  |
|------------------------------------|-----------|------------------------------------------------------------------------------|
| `jenkins_job_name`                 | Yes | The name of the job to trigger                                               |
| `jenkins_job_parameters`           | No | A dictionary of parameters to pass to the job                                |
| `jenkins_base_url`                 | Yes | The url of the jenkins server                                                |
| `jenkins_user`                     | Yes | The username for the jenkins server                                          |
| `jenkins_password`                 | Yes | The password/token for the jenkins server                                    |
| `wait_for_result` | No | If set to true, the action will wait for the job to finish _(default: True)_ |

**Note**
`jenkins_job_parameters` and `wait_for_result` should be quoted as in the example below.

#### Example of usage:
```yaml
jobs:
  start-jenkins-job:
    runs-on: ubuntu-latest
    steps:
      - name: Start Jenkins job
        uses: geokats7/jenkins_client@main
        with:
          jenkins_job_name: 'Job_folder/my_job'
          jenkins_job_parameters: '{"APP_ENV_NAME": "staging"}'
          jenkins_base_url: 'https://my-jenkins-instance.com/'
          jenkins_user: ${{ secrets.JENKINS_USER }}
          jenkins_password: ${{ secrets.JENKINS_PASSWORD }}
          wait_for_result: 'False'
```

###### Contact QA team in order to add more actions to the package.
