from configparser import ConfigParser

def load_config(filename='/Users/bekzatamantay/PP2/Lab 10/Tutor/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return config