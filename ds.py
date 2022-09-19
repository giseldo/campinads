import pysd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

model = pysd.read_vensim('teacup.mdl')

model.doc