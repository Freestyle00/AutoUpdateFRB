from subprocess import Popen, run
import requests
from bs4 import BeautifulSoup
import re as regex
import datetime
import os
import zipfile

class FRB_Getter:
    def __init__(this):
        this.DATE_URL        = "https://files.flatredball.com/content/FrbXnaTemplates/DailyBuild/"
        this.FILE_URL        = "https://files.flatredball.com/content/FrbXnaTemplates/DailyBuild/FRBDK.zip" 
        this.DATETIMEREGEX   = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})"
        this.FRB_PATH        = os.path.join("c:", os.sep,"Users", "Nick_", "Desktop", "FRB")  #r"C:/Users/Nick_/Desktop/FRB" 
        this.FRBDK_PATH      = os.path.join(this.FRB_PATH, "FRBDK")
        this.O_TXT_FILE_PATH = os.path.join(this.FRB_PATH, "date.txt")
        this.ZIP_PATH        = os.path.join(this.FRB_PATH, "FRBDK.zip")
        newdate, oldate = this.get_dates()
        this.compare_dates(newdate, oldate)
        this.OpenFRB()
    def get_old_date_time(this) -> datetime.datetime:
        with open(this.O_TXT_FILE_PATH, "r") as f:
            datetimes = f.read()
        datetimes = datetime.datetime.strptime(datetimes, "%Y-%m-%d %H:%M")
        return datetimes
    def write_new_date(this, newdate):
        with open(this.O_TXT_FILE_PATH, "w") as f:
            f.flush()
            f.write(newdate.strftime("%Y-%m-%d %H:%M"))
    def get_dates(this):
        ndatetimes = datetime.datetime.strptime(regex.search(this.DATETIMEREGEX, BeautifulSoup(requests.get(this.DATE_URL).text, "html.parser").text).group(1), "%Y-%m-%d %H:%M")
        olddatetimes = this.get_old_date_time()
        return ndatetimes, olddatetimes
    def compare_dates(this, ndatetimes=None, olddatetimes=None):
        if ndatetimes > olddatetimes:
            dele   = Popen(["del", "/s", "/q", this.FRBDK_PATH], shell=True)
            stdout, stderr = dele.communicate()
            rmdir  = Popen(["rmdir", "/s", "/q", this.FRBDK_PATH], shell=True)
            stdout, stderr = rmdir.communicate()
            try:
                os.remove(this.ZIP_PATH)
            except:
                pass
            wgett  = run(["powershell", "wget", this.FILE_URL, "-O", this.ZIP_PATH], shell=True)
            os.mkdir(this.FRBDK_PATH)
            with zipfile.ZipFile(this.ZIP_PATH) as zf:
                zf.extractall(this.FRBDK_PATH)
            this.write_new_date(ndatetimes)
    def OpenFRB(this):
        p = Popen("OpenFlatRedBall.bat", cwd=this.FRB_PATH)
        stdout, stderr = p.communicate()

if __name__ == "__main__":
    FRB_Getter()