import brain
import sys

b = brain.Brain("logfile")
tests = ['.s/test/XX/']

for test in tests:
    b.contemplate("uberj","channel",test)
