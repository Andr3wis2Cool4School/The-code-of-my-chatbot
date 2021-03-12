import os 

data_types = ('.csv')

def list_data(basePath, contains=None):
    return list_files(basePath, validExts=data_types, contains=contains)


def list_files(basePath, validExts=None, contains=None):
    for (rootDir, dirNames, filenames) in os.walk(basePath):
        for filename in filenames:
            if contains is not None and filename.find(contains) == -1:
                continue

            ext = filename[filename.rfind("."):].lower()

            if validExts is None or ext.endswith(validExts):
                dataPath = os.path.join(rootDir, filename)
                yield dataPath
