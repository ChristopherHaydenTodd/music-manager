#!/usr/bin/env bash
#
# Test Python
#
# Example Call:
#    ./test.sh
#

echo "$(date +%c): Running Unit Tests"
pytest music_manager

TEST_STATUS=$?
echo "$(date +%c): Test Exit Status - ${TEST_STATUS}"
