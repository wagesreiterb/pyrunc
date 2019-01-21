#!/bin/bash

MY_PID=`ps aux | grep sleeper | grep -v grep | grep -v python| awk '{ print $2 }'`
MY_PPID=`ps aux | grep sleeper | grep -v grep | grep python| awk '{ print $2 }'`

ps aux | grep sleeper | grep -v grep | grep -v python| awk '{ print $2 }'
echo PID $MY_PID

echo
ps aux | grep sleeper | grep -v grep | grep python| awk '{ print $2 }'
echo PPID $MY_PPID

ls -l /proc/$MY_PID/ns
ls -l /proc/$MY_PPID/ns