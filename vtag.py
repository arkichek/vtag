#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# 2012 (c) Arkady Fraerman <arkady.fr@gmail.com>


import argparse
import os
import codecs
import re
import sys
import plistlib
import tempfile
import subprocess
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
		b = float(self.lastBuild())
		b = b + 1
		bstr = '%.0f' % (b)
		pl['CFBundleVersion'] = bstr
		self.savePlist(pl)
		print('New build number is %s' % (bstr))
		

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
		textToAdd = self.finalizedBlock(self.textFromDialog())
		if textToAdd:
			logLines = self.logFileLines()
			logLines.insert(self.insertIndex(logLines), textToAdd)
			if self.writeLogLinesToFile(logLines):
				print('Changelog has been updated')
			else:
				print('Failed to update chagelog file')

	def insertIndex(self, logLines):
		result = 0
		if logLines:
			for i in range(len(logLines)):
				aLine = logLines[i]
				match = re.search('### Version', aLine)
				if match:
					result = i
					break
		return result

	def logFileLines(self):
		with codecs.open(self.logFilePath(), 'r') as logFile:
			return logFile.readlines()
		return None			

	def writeLogLinesToFile(self, lines):
		with codecs.open(self.logFilePath(), 'w', 'utf-8') as logFile:
			logFile.writelines(lines)
			return True
		return False

	def finalizedBlock(self, content):
		sub = (
			self.vtag.lastTag(), 
			self.vtag.lastBuild(), 
			self.vtag.lastBuildDate(), 
			content)
		return ('### Version %s (%s)\n*%s*  \n%s\n\n' % sub)

	def logFilePath(self):
		return os.path.join(self.vtag.projPath, 'CHANGELOG.md')

	def textFromDialog(self):
		# create temp file
		(fd, path) = tempfile.mkstemp()
		# open temp file with vi	
		editor = os.getenv('EDITOR', 'vi')
		commandLine = '%s %s' % (editor, path)
		subprocess.call(commandLine, shell=True)
		# open edited tempfile
		with codecs.open(path, 'r') as logFile:
			return logFile.read()
		return None



def parseArgs():
	parser = argparse.ArgumentParser(description='Tool for managing version labels in iOS projects')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s Version: 0.2')
	parser.add_argument('-r', '--read', dest='read', action='store_true', default=False, help='Read current version tag')
	parser.add_argument('-t', '--tag', dest='tag', help='New human version label')
	parser.add_argument('-b', '--build', dest='build', help='New build number')
	parser.add_argument('-ib', '--incrementBuild', dest='incrementBuild', action='store_true', default=False, help='Increase by one step build number')
	parser.add_argument('-ul', '--updateChangelog', dest='updateChangelog', action='store_true', default=False, help='Show vi editor to add new release notes')
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
		if args.updateChangelog:
			changelog.updateLog()
	# new build number
	if args.build:
		vtag.setBuild(args.build)
		if args.updateChangelog:
			changelog.updateLog()
	# increment build number
	if args.incrementBuild:
		vtag.incrementBuild()
		if args.updateChangelog:
			changelog.updateLog()

if __name__ == '__main__':
	args = parseArgs()
	changeVersion(args)
