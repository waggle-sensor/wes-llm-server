#!/usr/bin/env python3
#
# This tool downloads models to the /media/plugin-data/llama-cpp-models directory - I'll generalize it later.
#
# You can use it by running:
# ./download-model.py namespace/repo/model.gguf
#
# For example:
# ./download-model.py PsiPi/liuhaotian_llava-v1.5-13b-GGUF/llava-v1.5-13b-Q2_K.gguf
import argparse
from urllib.parse import urlparse
import subprocess
from pathlib import Path


# backport for earlier python versions
def removeprefix(s, p):
    if s.startswith(p):
        return s[len(p) :]
    return s


def main(models):
    for model in models:
        s = urlparse(model).path
        s = removeprefix(s, "/")
        fields = s.split("/")
        namespace = fields[0]
        repo = fields[1]
        file = fields[-1]
        download_url = f"https://huggingface.co/{namespace}/{repo}/resolve/main/{file}?download=true"
        output_file = Path("/media/plugin-data/llama-cpp-models", namespace, repo, file)

        # do not download if already exists
        if output_file.exists():
            print(f"model {output_file} already downloaded. skipping.")
            continue

        output_file.parent.mkdir(exist_ok=True, parents=True)

        download_file = output_file.with_suffix(".gguf.download")
        subprocess.check_call(["wget", "-N", download_url, "-O", str(download_file)])
        download_file.rename(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("models", nargs="+")
    args = parser.parse_args()
    main(args.models)
