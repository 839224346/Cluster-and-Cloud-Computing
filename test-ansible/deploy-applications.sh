#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False
. ./unimelb-comp90024-2021-grp-34-openrc.sh; ansible-playbook --ask-become-pass deploy_app.yaml -i inventory/hosts.ini
