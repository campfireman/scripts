#!/bin/bash

# Copyright by Leon Stoldt: https://github.com/LeonStoldt

# custom functions
time_calc() {
        START_TIME=$1
        SHORT_BREAK=$(date -d "$START_TIME today + 3 hour" +'%H:%M')
        FULL_BREAK=$(date -d "$START_TIME today + 6 hour" +'%H:%M')
        NORMAL_DAY=$(date -d "$START_TIME today + 500 minute" +'%H:%M')
        MAX_TIME=$(date -d "$START_TIME today + 650 minute" +'%H:%M')
        echo "You started at: $START_TIME o'clock.
Automatically booked 20 minute break since: $SHORT_BREAK o'clock.
Automatically booked 30 minute break since: $FULL_BREAK o'clock.
Full day incl. full break ends at: $NORMAL_DAY o'clock.
Do not work longer than $MAX_TIME o'clock!"
}

time_calc ${1}
