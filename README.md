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
 | `polling_interval` | No | Set the time interval to poll Jenkins for job result (seconds)               |

**Notes**  
`jenkins_job_parameters` and `wait_for_result` should be quoted as in the example below.

#### Example of usage:
~~~yaml
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
          polling_interval: 20
~~~
---
