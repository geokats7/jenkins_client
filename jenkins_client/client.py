import time
import sys
import os
import datetime

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build
from jenkinsapi.queue import QueueItem
from jenkinsapi.custom_exceptions import NotBuiltYet
from requests import HTTPError
import fire
import logging

logging.basicConfig(format='%(levelname)s| %(message)s', level=os.getenv('LOG_LEVEL', 'INFO'))


class JenkinsClient:

    def __init__(self,
                 jenkins_base_url=os.getenv("JENKINS_BASE_URL"),
                 jenkins_user=os.getenv("JENKINS_USER"),
                 jenkins_password=os.getenv("JENKINS_PASSWORD"),
                 queue_poll_interval=2,
                 queue_max_timeout=500,
                 job_poll_interval=20,
                 overall_max_timeout=1800):
        if jenkins_base_url is None:
            raise AttributeError("JENKINS_BASE_URL is not set. Please provide Jenkins base URL.")
        self.jenkins_base_url = jenkins_base_url
        self._jenkins = Jenkins(jenkins_base_url, username=jenkins_user, password=jenkins_password)
        self.queue_poll_interval = queue_poll_interval
        self.queue_max_timeout = queue_max_timeout
        self.job_poll_interval = job_poll_interval
        self.overall_max_timeout = overall_max_timeout

    def list_jobs(self) -> list:
        """List all the available jobs of the Jenkins instance"""
        job_names_list = [item[0] for item in self._jenkins.items()]
        return job_names_list

    def start_job(self, job_name: str, params: dict = None, wait_for_result: bool = True):
        """Start a job and poll it until it's over or timed out."""
        if params is not None and type(params) is not dict:
            print(type(params))
            raise TypeError(f"The parameters should be entered as a dictionary.\nParameters given: {params}.\nHint: Check for missing quotation.")
        job = self._jenkins[job_name]
        queue_item = job.invoke(build_params=params)
        logging.info("Job entered queue")
        build = self._poll_job_queue(queue_item)
        logging.info(f"Job started building [Build no. {queue_item.get_build_number()}]")
        logging.info(f"Estimated duration -> {str(datetime.timedelta(seconds=build.get_estimated_duration())).split('.')[0]}")
        if wait_for_result:
            self._poll_build_for_status(build)

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
                logging.info(f"{time.ctime()}: Job {queue_item.get_job_name()} has not started yet.")
            if elapsed_time > self.queue_max_timeout:
                raise Exception("Max time out for queue reached!")

    def _poll_build_for_status(self, build: Build):
        start_epoch = int(time.time())

        while True:
            build.poll()
            result = build.get_status()
            if result == 'SUCCESS':
                # Do success steps
                logging.info(f"{time.ctime()} | Job: {build.job.name} | Status: {result}")
                break
            elif result == 'FAILURE':
                # Do failure steps
                logging.info(f"{time.ctime()} | Job: {build.job.name} | Status: {result}")
                logging.info(f"View more details here: {build.get_build_url()}")
                sys.exit(1)
            elif result == 'ABORTED':
                # Do aborted steps
                logging.info(f"{time.ctime()} | Job: {build.job.name} | Status: {result}")
                logging.info(f"View more details here: {build.get_build_url()}")
                sys.exit(1)
            else:
                logging.info(f"{time.ctime()} | Job: {build.job.name} | Status: The job is still running. Polling again in {self.job_poll_interval} secs")

            cur_epoch = int(time.time())
            if (cur_epoch - start_epoch) > self.overall_max_timeout:
                logging.info(f"Overall timeout: No status before timeout of {self.overall_max_timeout} secs")
                sys.exit(1)

            time.sleep(self.job_poll_interval)


if __name__ == '__main__':
    fire.Fire(JenkinsClient)

