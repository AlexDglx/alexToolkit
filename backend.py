###This backgend converts images to a user selected format

import os
import cv2
import subprocess
from bcolors import bcolors
import numpy as np
from pathlib import Path

class Image:

    def __init__(self, filepath:str):
        self.filepath = filepath
        self.base, self.fullname = os.path.split(filepath)
        self.name, self.extension = self.fullname.split('.')
        self.directory= Path(filepath).parent.absolute()
        
    def filemetadata(self):
        
        name, extension =os.path.split(self.filepath)
        img = cv2.imread(self.filepath)
        width , height = img.shape[0],img.shape[1] 
        
        metadata = {
            "name":name,
            "extension":extension,
            "dimensions":{
                "height":height,
                "width":width,
            }
        }

        return metadata
    
    def convertBW(self, outputName:str,ext:str):
        
        outputpath = os.path.join(self.directory,f'{outputName}{ext}')
        
        try:
            
            script=f"""
            #!/bin/bash
            ffmpeg -i {self.filepath} -vf format=gray {outputpath}
            """
            subprocess.run(script, shell=True, check=True,capture_output=True)
            print(f"File {bcolors.OKCYAN}{bcolors.BOLD}{os.path.basename(outputpath)}{bcolors.ENDC} converted")
            
        except Exception as err:
            print(err)
    
    def convert(self, outputdir:str,outputname:str,outputExt:str):
        outputpath = os.path.join(outputdir,f'{outputname}.{outputExt}')
        try:
            script = f"""
            #!/bin/bash
            ffmpeg -y -i {self.filepath} {outputpath}
            """
            subprocess.run(script, shell=True, check=True,capture_output=True)
            print(f"File {bcolors.OKCYAN}{bcolors.BOLD}{os.path.basename(outputpath)}{bcolors.ENDC} converted")
        except Exception as err:
            print(err)
    
    #ffmpeg -i input.jpg -vf scale=320:240 output_320x240.png
    def scale(self, outputdir:str, outputname:str,outputExt:str, dimension:tuple):

            outputpath = os.path.join(outputdir,f'{outputname}{outputExt}')
            script = f"""
            #!/bin/bash
            ffmpeg -y -i {self.filepath} -vf scale={dimension[0]}:{dimension[1]}:flags=lanczos {outputpath}
            """
            subprocess.run(script, shell=True, check=True,capture_output=True)
        
class YTDownloader:
    def __init__(self, directory:str, url:str, frmt:str, output_name:str):
        self.url = url
        self.frmt = frmt
        self.output_name = output_name
        self.directory = directory
        
    def audio_download(self):
        try:
            script = f"""
            #!/bin/bash
            cd
            cd "{self.directory}"
            yt-dlp --post-overwrites --force-overwrites -o "{self.output_name}" -x --audio-format "{self.frmt}" --audio-quality 0 "{self.url}"
            echo Song downloaded
            """
            subprocess.run(script,  shell=True, check=True,capture_output=True)
            print(f"Audio {bcolors.OKCYAN}{bcolors.BOLD}downloaded{bcolors.ENDC}")
        except Exception as err:
            print(err) 
    
    def video_download(self):
        
        script = f"""
        #!/bin/bash
        cd
        cd "{self.directory}"
        yt-dlp --post-overwrites --embed-metadata --embed-thumbnail --force-overwrites -o "{self.output_name}" -f "bv*[height<=720][ext=mp4][vcodec^=avc1]+ba[ext=mp4]" -N 4 "{self.url}" 
        ffmpeg -i "{self.output_name}.mp4" "{self.output_name}.{self.frmt}"
        """
        subprocess.run(script, shell=True, check=True,capture_output=True)
        print(f"Video {bcolors.OKCYAN}{bcolors.BOLD}downloaded{bcolors.ENDC}")
        
if __name__ == "__main__":
    #img1 = Image("/Users/adegallaix/Downloads/bears.png")
    #print(img1.convertBW())
    #audio_file = YTDownloader('/Users/adegallaix/Downloads',
    #                          'https://www.youtube.com/watch?v=9uYF95jR_ME', 'wav','moonlight shadow audio')
    #audio_file.audio_download()
    
    video_file = YTDownloader('/Users/adegallaix/Downloads',
                              'https://youtu.be/xD11FpDa3NY',
                              'mov','moonlight shadow video')
    video_file.video_download()
    
# --post-overwrites --embed-metadata --embed-thumbnail --force-overwrites 
#"