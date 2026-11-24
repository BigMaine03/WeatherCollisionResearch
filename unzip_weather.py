import zipfile
import glob

for path in sorted(glob.glob("/Users/Manas/Desktop/ITC510/weathercdc/*.nc")):
    if zipfile.is_zipfile(path):
        folder = path.replace(".nc", "")
        with zipfile.ZipFile(path) as z:
            z.extractall(folder)
        print("unzipped:", path)
    else:
        print("NOT A ZIP:", path)

