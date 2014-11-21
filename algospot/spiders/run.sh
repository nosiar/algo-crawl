#! /bin/bash

if [ $# -eq 0 ] ; then
	scrapy crawl -o problem.json problem
else
	scrapy crawl -o user$1.json -a uid=$1 user
fi
