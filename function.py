# -*- coding: utf-8 -*-
"""contents_maker.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xjeL6QHiKx-YvWx4wTwKVVgVKyxGkxVs

마케팅 사진을 만드는 코드입니다.  
과정은 다음과 같습니다.
1. chatGPT: 아이디어(input)->__마케팅 그림 묘사문__, 키워드
2. Stable Diffusion: 키워드->__그림__
3. Output: 그림(images)+묘사문(sentence)
"""
import openai
import torch
from diffusers import DiffusionPipeline
from PIL import Image

def answer(prompt:str):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", 
                "content": prompt}
                ]
        )
        result=completion.choices[0].message["content"]
        return result

class text_generation():
    def __init__(self,input:str):
        self.input=input
        self.roleplay=f"You're a marketer. You have a great talent and knowledges for advertising and marketing.\
        My idea is {self.input}."

    def idea_text(self):
        request="Perform the following actions:\
        1 - Create name for idea.\
        2 - Write catchphrase for idea.\
        Use the following format:\
        Name: <idea name>\
        Catchphrase: <idea catchphrase>"

        return answer(self.roleplay+request)

    def stp_text(self):
        request="Write the STP strategy for idea using macro and micro environment analysis.\
        Use the following format:\
        -Segmentation\
        ∙ Demographic: <demographic segmentation strategy>\
        ∙ Psychographic: <Psychographic segmentation strategy>\
        ∙ Behavioral: <Behavioral segmentation strategy>\
        -Targeting\
        <Targeting strategy>\
        -Positioning\
        <Positioning strategy>"

        return answer(self.roleplay+request)

    def content_text(self):
        request="I want to make a picture for advertising idea, but I don't know what scene is suitable for marketing.\
        You can imagine a picture for idea. \
        Please describe the scene of photo for advertising idea in 4 lines."
        
        sentence=answer(self.roleplay+request)
        keyword=answer(f"I write the description for photo.\
        description is {sentence}.\
        Please extract and list 8 keywords for the scene of photo. \
        You should write keywords using ',' symbol only. Other symbols must not be used.")

        return sentence, keyword
    
    def returns(self):
        inputs=text_generation(self.input)
        return inputs.idea_text(),inputs.stp_text(),inputs.content_text(),

pos_default="masterpiece, raw photo, extremely detailed skin, extremely detailed face, 8k uhd, \
dslr, soft lighting,  film grain, Fujifilm XT3, instagram, realstic" 

neg_default="(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4),\
text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, duplicate, morbid, mutilated,\
extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, blurry, dehydrated, bad anatomy,\
bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms,\
extra legs, fused fingers, too many fingers, long neck, (nsfw:2), (sexual content:2)"

class image_generation():
    def __init__(self,input:str,pos=pos_default,neg=neg_default):
        self.input=input
        self.pos=pos
        self.neg=neg
        repo_id="SG161222/Realistic_Vision_V2.0"
        self.pipeline=DiffusionPipeline.from_pretrained(repo_id, torch_dtype=torch.float16).to("cuda")
        
    def implement(self):
        pos, neg=self.pos, self.neg
        pipeline=self.pipeline
        pipeline.enable_xformers_memory_efficient_attention()
        images = pipeline(num_inference_steps=30, 
                          prompt=pos+','+self.input,
                          negative_prompt=neg,
                          num_images_per_prompt=8).images
        return images

class output_process():
    def __init__(self,image,sentence):
        def image_grid(imgs, rows=2, cols=4):
            assert len(imgs) == rows*cols

            w, h = imgs[0].size
            grid = Image.new('RGB', size=(cols*w, rows*h))
            
            for i, img in enumerate(imgs):
                grid.paste(img, box=(i%cols*w, i//cols*h))
            return grid
        self.image=image
        self.grid=image_grid(image)
        self.sentence=sentence
        
    def returns(self):
        return self.grid, self.sentence

    def show(self):
        self.grid.show()
        print(self.sentence)
