#!/usr/bin/env bash
for x in u c r rv m mv
do
  python manage.py loaddata "$x.json"
done
