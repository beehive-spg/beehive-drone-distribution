#!/usr/bin/env python3
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(path)
sys.path.append(os.path.dirname(path))
import drone_distribution.distributor as distributor
import drone_distribution.training as training

def main():
	test_operator()

def test_operator():
	distributor.start_distribution_to(22)

if __name__ == '__main__':
	main()