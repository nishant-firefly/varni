# Add the parent directory to the Python path
import os 
import sys
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)