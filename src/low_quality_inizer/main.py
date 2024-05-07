import subprocess
import typer
from pytube import YouTube
import os
from enum import Enum


class Quality(Enum):
    EXTRA_LOW = 8
    LOW = 16
    MEDIUM = 24


def low_quality_inize(url: str, image: str = None, quality: str = "LOW"):
    quality = get_quality(quality)

    file = download_mp3(url)
    if file:
        input_file = file + ".mp3"
        output_file = file + "_low_quality.mp4"
        print(input_file)
        print(output_file)

        output_dir = r"~/Desktop/low\ quality\ songs/videos/" + file + "_low_quality"

        if image:
            subprocess.run(
                [
                    f"mkdir {output_dir}",
                ],
                shell=True
            )
            subprocess.run(
                [
                    f"ffmpeg -loop 1 -i {image} -i {input_file} -c:v libx264 -vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" -c:a aac -strict experimental -b:a  {quality.value}k -shortest {output_dir}/{output_file}"
                ],
                shell=True
            )
        else:
            subprocess.run(
                [
                    f"ffmpeg -i \"{input_file}\" -b:a 8k -vn \"{output_file}\""],
                shell=True
            )

        subprocess.run(
            [
                f"rm {input_file}"
            ],
            shell=True
        )
        print("Done")


def get_quality(quality):
    match(quality.upper()):
        case "XLOW":
            return Quality.EXTRA_LOW
        case "LOW":
            return Quality.LOW
        case "MEDIUM":
            return Quality.MEDIUM
        case _:
            return Quality.LOW


def download_mp3(url: str):
    try:
        video = YouTube(str(url), use_oauth=True, allow_oauth_cache=True)
        audio = video.streams.filter(only_audio=True).first()

        out_file = audio.download(output_path=os.getcwd())
        base, ext = os.path.splitext(out_file)
        base = base[:len(os.getcwd())] + base[len(os.getcwd()):].lower().replace(" ", "-")
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        return base[len(os.getcwd())+1:]
    except Exception:
        print("Couldn't download the supplied YouTube video")
        return False


if __name__ == '__main__':
    typer.run(low_quality_inize)
