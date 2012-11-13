#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# 2012 (c) Arkady Fraerman <arkady.fr@gmail.com>


import argparse
import os
import codecs
import re
import sys
import plistlib


class VersionTag:
	def __init__(self, projPath):
		self.projPath = projPath
		if not self.isValidProjPath():
			print('Path in not valid')
			sys.exit(0)

	def isValidProjPath(self):
		# TODO: check if proj file exists and it is correct extension
		return True

	def xcodeprojPath(self):
		lst = os.listdir(self.projPath)
		for aName in lst:
			match = re.search('(.+\.xcodeproj)', aName)
			if match:
				return os.path.join(self.projPath, match.group(1)) 
		return None

	def pbxprojPath(self):
		return os.path.join(self.xcodeprojPath(), 'project.pbxproj')	

	def infoPlistPath(self):
		with codecs.open(self.pbxprojPath(), 'r') as pbxprojFile:
			pbx = pbxprojFile.read()
			match = re.search('INFOPLIST_FILE = "(.+)";', pbx)
			if match:
				return os.path.join(self.projPath, match.group(1))
		return None

	def plist(self):
		return plistlib.readPlist(self.infoPlistPath())

	def savePlist(self, plistObj):
		# TODO: change date
		plistlib.writePlist(plistObj, self.infoPlistPath())

	def setTag(self, tag):
		pass

	def setBuild(self, build):
		pass

	def incrementBuild(self):
		pl = self.plist()
		nbn = eval('%s + 1' % (pl['CFBundleVersion']))
		pl['CFBundleVersion'] = str(nbn)
		print('New build number is %s' % (pl['CFBundleVersion']))
		self.savePlist(pl)

	def readCurrentVersion(self):
		pl = self.plist()
		print('Current build version: %s (%s)' % (pl['CFBundleShortVersionString'], pl['CFBundleVersion']))



def parseArgs():
	parser = argparse.ArgumentParser(description='Tool for managing version labels in iOS projects')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s Version: 0.1')
	parser.add_argument('-r', '--read', dest='read', action='store_true', default=False, help='Read current version tag')
	parser.add_argument('-t', '--tag', dest='tag', help='New human version label')
	parser.add_argument('-b', '--build', dest='build', help='New build number')
	parser.add_argument('-ib', '--incrementBuild', dest='incrementBuild', action='store_true', default=False, help='Increase by one step build number')
	parser.add_argument('projPath', help='Path to .xcodeproj file')
	return parser.parse_args()

def changeVersion(args):
	vtag = VersionTag(args.projPath)
	# print current version
	if args.read:
		vtag.readCurrentVersion()
	# new tag
	if args.tag:
		vtag.setTag(args.tag)
	# new build number
	if args.build:
		vtag.setBuild(args.build)
	# increment build number
	if args.incrementBuild:
		vtag.incrementBuild()

if __name__ == '__main__':
	args = parseArgs()
	changeVersion(args)
