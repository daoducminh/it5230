#!/usr/bin/env bash
for x in u u1 c r rv
do
  python manage.py loaddata "$x.json"
done
