# Tournament
This was a database project to orchestrate certain documented actions on a swiss ranking system based tournament.

# Prereqs

## Local Machine
A standalone instance of this will require PostgreSQL and the pyscopg library for Python 2.7.

## Pre-configure VM
A fully configured VM is available as part of the project. For this you will require Vagrant and VirtualBox.

Vagrant: https://www.vagrantup.com/

VirtualBox: https://www.virtualbox.org/wiki/Downloads

Configured VM: https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58488015_fsnd-virtual-machine/fsnd-virtual-machine.zip

### Installation and Usage of VM

Unzip and cd into the downloaded VM dir, then cd into the vagrant subdir. 

```bash
unzip FSND-Virtual-Machine.zip ; cd FSND-Virtual-Machine/vagrant
```

Here you will be able to run the following:

```bash
vagrant up
```

This will download the VM operating system and prepare everything for you. Next clone this repo and overwrite the tournament dir.

```bash
git clone repo
```

Time to ssh in:

```bash
vagrant ssh
```

Then navigate to the tournament directory and init the database:

```bash
cd /vagrant/tournament ; psql -c '\i tournament.sql'
```

# Testing the database

```bash
python tournment_test.py
```
