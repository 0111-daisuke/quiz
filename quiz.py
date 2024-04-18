import random
import torch 
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = "cuda" if torch.cuda.is_available() else "cpu"

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

#ランダムに単語を選択
def radword():
  
  # 単語のリストを用意する
  words = ["apple", "banana", "orange", "grape", "pineapple", "watermelon", "strawberry", "kiwi", "peach", "melon"]
  
  # リストからランダムに1つの要素を選ぶ
  selected_word = random.choice(words)
  
  return selected_word

#画像生成
def imgcreate(text):
  
  model_id = "stabilityai/stable-diffusion-2-1-base"
  
  scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
  pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler)
  pipe = pipe.to(device)
  
  prompt = text
  image = pipe(prompt).images[0]

  return image

#キャプション生成に必要なステップ
def predict_step(image_paths):
  images = []
  for image_path in image_paths:
     i_image = Image.open(image_path)
     if i_image.mode != "RGB":
       i_image = i_image.convert(mode="RGB")
        
     images.append(i_image)

  pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
  pixel_values = pixel_values.to(device)
    
  output_ids = model.generate(pixel_values, **gen_kwargs)
    
  preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
  preds = [pred.strip() for pred in preds]
  return preds

#キャプション生成
def captioning(img):

  caption = predict_step([img]) # ['a woman in a hospital bed with a woman in a hospital bed']
  return caption

#メイン文
def main():
  word = radword()
  print('prompt',word)
  
  image = imgcreate(word)
  image = "generated_image.png"
  image.save("generated_image.png")

  caption = captioning(image)
  print(caption)

#実行
main()