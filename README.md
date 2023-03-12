# [Docker image: githubtraffic](https://hub.docker.com/r/drpsychick/githubtraffic/)

[![Docker image](https://img.shields.io/docker/image-size/drpsychick/githubtraffic?sort=date)](https://hub.docker.com/r/drpsychick/githubtraffic/tags)
[![Workflow Status](https://img.shields.io/github/actions/workflow/status/drpsychick/docker-githubtraffic/release.yaml)](https://github.com/DrPsychick/docker-githubtraffic/actions)
[![license](https://img.shields.io/github/license/drpsychick/docker-githubtraffic.svg)](https://github.com/drpsychick/docker-githubtraffic/blob/master/LICENSE) 
[![DockerHub pulls](https://img.shields.io/docker/pulls/drpsychick/githubtraffic.svg)](https://hub.docker.com/r/drpsychick/githubtraffic/) 
[![DockerHub stars](https://img.shields.io/docker/stars/drpsychick/githubtraffic.svg)](https://hub.docker.com/r/drpsychick/githubtraffic/) 
[![GitHub stars](https://img.shields.io/github/stars/drpsychick/docker-githubtraffic.svg)](https://github.com/drpsychick/docker-githubtraffic) 
[![Contributors](https://img.shields.io/github/contributors/drpsychick/docker-githubtraffic.svg)](https://github.com/drpsychick/docker-githubtraffic/graphs/contributors)

[![GitHub issues](https://img.shields.io/github/issues/drpsychick/docker-githubtraffic.svg)](https://github.com/drpsychick/docker-githubtraffic/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/drpsychick/docker-githubtraffic.svg)](https://github.com/drpsychick/docker-githubtraffic/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/drpsychick/docker-githubtraffic.svg)](https://github.com/drpsychick/docker-githubtraffic/pulls)
[![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/drpsychick/docker-githubtraffic.svg)](https://github.com/drpsychick/docker-githubtraffic/pulls?q=is%3Apr+is%3Aclosed)
[![Paypal](https://img.shields.io/badge/donate-paypal-00457c.svg?logo=paypal)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=FTXDN7LCDWUEA&source=url)
[![GitHub Sponsor](https://img.shields.io/badge/github-sponsor-blue?logo=github)](https://github.com/sponsors/DrPsychick)


A very simple python script that just fetches view and clone traffic 
to print it to standard out and optionally push it to influxdb

```shell
docker run --rm --env-file .env -t drpsychick/githubtraffic
```