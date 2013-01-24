# vtag

## Description

Command line tool for managing Info.plist iOS/Mac projects.

Receives arguments for:

- updating version string number (tag)
- setting new build number or incrementing it
- reading current version
- adding release notes to changelog via vi editor, that is stored in root of the project


## Install

Project contains bash script install.sh that copies tool to /usr/local/bin/vtag and runs chmod 755 for it.


## Usage

This example will increment build number and show vi editor for typing release notes:

	vtag -ib -ul .
	
Run
 
	vtag -h  
	
for full arguments list.