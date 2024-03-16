import configparser

config = configparser.ConfigParser()
config.read('./AS5-Lacrosse.ini')
idx = 0
mapping = dict()
for section in config.sections():
    name = config[section]["NAME"]
    length = config[section]["LENGTH"]
    mapping[name] = (idx, idx + int(length))
    idx += int(length)

print(mapping)