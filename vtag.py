#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# 2012 (c) Arkady Fraerman <arkady.fr@gmail.com>


import argparse
import os
import codecs
import re
import sys
import plistlib
from datetime import *


class VersionTag:
	def __init__(self, projPath):
		self.projPath = projPath
		if not self.isValidProjPath():
			print('Path in not valid or doesn\'n contain xcode project')
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
		raise Exception('Please cpecify corrent path to xcodeproj folder')

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
		now = datetime.now()
		plistObj['AFBuildDate'] = now.strftime("%Y-%m-%d %H:%M:%S")
		plistlib.writePlist(plistObj, self.infoPlistPath())

	def setTag(self, tag):
		pl = self.plist()
		pl['CFBundleShortVersionString'] = tag
		self.savePlist(pl)

	def setBuild(self, build):
		pl = self.plist()
		pl['CFBundleVersion'] = build
		self.savePlist(pl)

	def incrementBuild(self):
		pl = self.plist()
		nbn = eval('%s + 1' % (pl['CFBundleVersion']))
		pl['CFBundleVersion'] = str(nbn)
		print('New build number is %s' % (pl['CFBundleVersion']))
		self.savePlist(pl)

	def readCurrentVersion(self):
		print('Current build version: %s (%s)' % (self.lastTag(), self.lastBuild()))
		buildDate = self.lastBuildDate()
		if buildDate:
			print('Build date: %s' % (buildDate))

	def lastTag(self):
		pl = self.plist()
		return pl['CFBundleShortVersionString']

	def lastBuild(self):
		pl = self.plist()
		return pl['CFBundleVersion']

	def lastBuildDate(self):
		result = None
		pl = self.plist()
		if 'AFBuildDate' in pl.keys():
			result = pl['AFBuildDate']
		return result


class Changelog:
	def __init__(self, vtag):
		self.vtag = vtag

	def updateLog(self):
		pass



def parseArgs():
	parser = argparse.ArgumentParser(description='Tool for managing version labels in iOS projects')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s Version: 0.1')
	parser.add_argument('-r', '--read', dest='read', action='store_true', default=False, help='Read current version tag')
	parser.add_argument('-t', '--tag', dest='tag', help='New human version label')
	parser.add_argument('-b', '--build', dest='build', help='New build number')
	parser.add_argument('-ib', '--incrementBuild', dest='incrementBuild', action='store_true', default=False, help='Increase by one step build number')
	parser.add_argument('projPath', help='Path to folder where .xcodeproj file is located')
	return parser.parse_args()

def changeVersion(args):
	vtag = VersionTag(args.projPath)
	changelog = Changelog(vtag)
	# print current version
	if args.read:
		vtag.readCurrentVersion()
	# new tag
	if args.tag:
		vtag.setTag(args.tag)
		changelog.updateLog()
	# new build number
	if args.build:
		vtag.setBuild(args.build)
		changelog.updateLog()
	# increment build number
	if args.incrementBuild:
		vtag.incrementBuild()
		changelog.updateLog()

if __name__ == '__main__':
	args = parseArgs()
	changeVersion(args)
