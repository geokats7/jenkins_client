import time
import sys

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build
from jenkinsapi.queue import QueueItem
from jenkinsapi.custom_exceptions import NotBuiltYet
from requests import HTTPError
import fire


class JenkinsClient:

    def __init__(self, jenkins_base_url, username, password,
                 queue_poll_interval=2, queue_max_timeout=500,
                 job_poll_interval=20, overall_max_timeout=1800):
        self.jenkins_base_url = jenkins_base_url
        self._jenkins = Jenkins(jenkins_base_url, username=username, password=password)
        self.queue_poll_interval = queue_poll_interval
        self.queue_max_timeout = queue_max_timeout
        self.job_poll_interval = job_poll_interval
        self.overall_max_timeout = overall_max_timeout

    def list_jobs(self):
        job_names_list = [item[0] for item in self._jenkins.items()]
        return job_names_list

    def start_job(self, job_name, params: dict = None):
        if params is not None:
            if type(params) is not dict:
                print(type(params))
                raise AttributeError("The parameters should be entered in a dictionary")
        job = self._jenkins[job_name]
        queue_item = job.invoke(build_params=params)
        print("Job entered queue")
        # build = queue_item.block_until_building()
        build = self._poll_job_queue(queue_item)
        print("Job started building")
        # build_number = queue_item.get_build_number()
        self._poll_build_for_status(build)
        print(build.get_status())

    def _poll_job_queue(self, queue_item: QueueItem):
        elapsed_time = 0
        while True:
            time.sleep(self.queue_poll_interval)
            elapsed_time += self.queue_poll_interval
            try:
                queue_item.poll()
                return queue_item.get_build()
            except (NotBuiltYet, HTTPError):
                time.sleep(self.queue_poll_interval)
            if (elapsed_time % (self.queue_poll_interval * 10)) == 0:
                print(f"{time.ctime()}: Job {queue_item.get_job_name()} has not started yet.")
            if elapsed_time > self.queue_max_timeout:
                raise Exception("Max time out for queue reached!")

    def _poll_build_for_status(self, build: Build):
        print(f"{time.ctime()}: Job started URL: {build.get_build_url()}")
        start_epoch = int(time.time())

        while True:
            build.poll()
            result = build.get_status()
            if result == 'SUCCESS':
                # Do success steps
                print(f"{time.ctime()}: Job: {build.job.name} Status: {result}")
                break
            elif result == 'FAILURE':
                # Do failure steps
                print(f"{time.ctime()}: Job: {build.job.name} Status: {result}")
                sys.exit(1)
            elif result == 'ABORTED':
                # Do aborted steps
                print(f"{time.ctime()}: Job: {build.job.name} Status: {result}")
                sys.exit(1)
            else:
                print(f"{time.ctime()}: Job: {build.job.name} Status: {result}. Polling again in {self.job_poll_interval} secs")

            cur_epoch = int(time.time())
            if (cur_epoch - start_epoch) > self.overall_max_timeout:
                print(f"Overall timeout: No status before timeout of {self.overall_max_timeout} secs")
                sys.exit(1)

            time.sleep(self.job_poll_interval)


if __name__ == '__main__':
    fire.Fire(JenkinsClient)
