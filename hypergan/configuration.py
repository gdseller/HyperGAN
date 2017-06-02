import hyperchamber as hc
import os

class Configuration:
    def find(configuration):
        dirname = os.path.dirname(os.path.realpath(configuration))
        return dirname + "/hypergan/configurations/"+configuration
    def load(configuration):
        return hc.Selector().load(Configuration.find(configuration))
    def default():
        return Configuration.load('default.json')