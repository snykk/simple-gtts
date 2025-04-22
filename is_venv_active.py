import sys

if sys.prefix != sys.base_prefix:
    print("Virtual environment is active.")
else:
    print("Virtual environment is not active.")