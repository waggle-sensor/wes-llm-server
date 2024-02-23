#!/usr/bin/env python3
# Adapted from OpenAI's Vision example
import argparse
import base64
from openai import OpenAI


def main(addr, paths):
    # Point to the local server
    client = OpenAI(
        base_url=f"http://{addr}/v1", api_key="not-needed"
    )  # api_key not used

    for path in paths:
        # Read the image and encode it to base64:
        base64_image = ""
        try:
            image = open(path.replace("'", ""), "rb").read()
            base64_image = base64.b64encode(image).decode("utf-8")
        except:
            print(
                "Couldn't read the image. Make sure the path is correct and the file exists."
            )
            exit()

        completion = client.chat.completions.create(
            model="local-model",  # not used
            messages=[
                {
                    "role": "system",
                    "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
            max_tokens=1000,
            stream=True,
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--addr", default="127.0.0.1:1234")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    main(args.addr, args.paths)
