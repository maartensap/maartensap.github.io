#!/usr/bin/env python3

from  generateWebsite import *
# import pdfgen

import argparse
import base64

from openai import OpenAI
openai_api_key = "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"

if __name__=="__main__":
  themes, oldPubs = loadResearchThemes()

  # Rewrite themes to image prompts
  client = OpenAI(api_key=openai_api_key)

  prompt = "Take this name and description of a research theme and generate a very detailed caption for a simple clipart / graphic / abstract style drawing or image that depicts the main point of the theme. Do not suggest image captions that have text in them. Respond with only the caption, no formatting or bullets or anything.\n"

  imagePrompts = {}
  for i, (t, d) in enumerate(themes.items()):
    chat_completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": prompt+t+"\n"+d}]
    )
    caption = chat_completion.choices[0].message.content
    imagePrompts[t] = caption

    result = client.images.generate(
      model="gpt-image-1",
      # model="dall-e-3",
      prompt=caption,
      n=1,
      size="1024x1024",
      # response_format="b64_json"
    )
    
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    
    # Save the image to a file
    with open(f"images/themes/theme{i}.png", "wb") as f:
      f.write(image_bytes)
