#!/bin/bash
. utils/package_manager.sh

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing postgresql            |"
echo "|                                          |"
echo "+------------------------------------------+"



$pkg_mng --yes install postgresql python3-psycopg2

echo "adding user and database"

sudo -u postgres psql <<EOF
\x
create database openrlabs;
create user openrlabs with encrypted password 'openrlabs';
grant all privileges on database openrlabs to openrlabs;
EOF

echo "restore schema"

sudo -u postgres psql openrlabs < packages/openrlabs.dump
