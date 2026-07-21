#!/bin/bash
mongoimport --db crawler --collection posting --file /data/results.json --upsert --upsertFields url
