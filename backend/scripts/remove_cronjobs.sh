#!/bin/bash

crontab -l | sed '/^.* # LIFEHUB/d' | crontab -
