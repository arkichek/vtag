#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# 2012 (c) Arkady Fraerman <arkady.fr@gmail.com>


import argparse


class VersionTag:
	def __init__(self, projPath):
		self.projPath = projPath
		pass



def parseArgs():
	parser = argparse.ArgumentParser(description='Tool for managing version labels in iOS projects')
	parser.add_argument('-t', '--tag', dest='tag', help='Human version label')
	parser.add_argument('-b', '--build', dest='build', help='New build number')
	parser.add_argument('-ib', '--incrementBuild', dest='incrementBuild', action='store_true', default=False, help='Increase by one step build number')
	parser.add_argument('projPath', help='Path to .xcodeproj file')
	return parser.parse_args()


if __name__ == '__main__':
	args = parseArgs()
