import subprocess
import typer
from pytube import YouTube
import os


def low_quality_inize(url: str):
    file = download_mp3(url)
    if file:
        input_file = file + ".mp3"
        output_file = file + "_low_quality.mp3"
        print(input_file)
        print(output_file)
        subprocess.run(
            [f"ffmpeg -i \"{input_file}\" -b:a 8k \"{output_file}\""],
            shell=True
        )
        print("Done")


def download_mp3(url: str):

    video = YouTube(str(url), use_oauth=True, allow_oauth_cache=True)
    audio = video.streams.filter(only_audio=True).first()

    out_file = audio.download(output_path=os.getcwd())
    base, ext = os.path.splitext(out_file)
    base = base[:len(os.getcwd())] + base[len(os.getcwd()):].lower().replace(" ", "-")
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    return base[len(os.getcwd())+1:]
    # except Exception:
    #     print("Couldn't download the supplied YouTube video")
    #     return False


if __name__ == '__main__':
    typer.run(low_quality_inize)
