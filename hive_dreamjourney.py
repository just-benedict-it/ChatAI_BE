from dotenv import load_dotenv
import os
import requests
from typing import Optional, Dict
import asyncio
import random

load_dotenv()
API_KEY = os.getenv("HIVE_API")

STYLE_TEMPLATES = {
    "single_portrait": """{prompt}, professional headshot portrait, hyperrealistic, 
shot on Canon EOS R5, 85mm f/1.2 lens, natural studio lighting,
8k resolution, detailed skin texture and pores,
natural eye reflections, detailed iris, focused eyes,
individual hair strands, professional color grading,
perfect exposure, subtle smile, relaxed pose,
shallow depth of field, soft bokeh background,
professional retouching, award winning portrait
--no artificial skin, no oversaturation,
no unnatural shadows, no unrealistic proportions,
no watermark, no text, no asymmetrical face""",


    "group_portrait": """{prompt}, professional group photograph,
cinematic composition, perfect framing,
shot on Sony A7R IV, natural studio lighting,
8k resolution, detailed skin textures,
clear focused eyes, natural expressions,
individual features, balanced positioning,
coordinated poses, perfect exposure,
professional retouching, commercial quality
--no overlapping faces, no missing limbs,
no unnatural spacing, no identical faces,
no artificial skin, no oversaturation,
no unrealistic proportions, no watermark,
no text, no asymmetrical faces""",

"anime": """{prompt}, anime illustration, by Studio Ghibli, Makoto Shinkai style, masterpiece quality,
highres, studio anime quality,
vibrant colors, clean sharp lines, cell shaded,
beautiful detailed eyes, reflective pupil highlights,
dynamic lighting, soft ambient occlusion,
detailed hair strands with highlights,
precise linework, smooth color gradients,
professional color composition, stunning details,
cinematic composition,
--no pixelation, no blur, no jagged edges,
no inconsistent lines, no rough shading,
no anatomical errors, no unnatural proportions""",

    "photo_realistic": """{prompt}, hyperrealistic photograph,
ultra detailed, photorealistic rendering,
shot on Phase One IQ4 150MP, optimal exposure,
perfect composition, award winning photography,
natural lighting, physically accurate materials,
true color reproduction, controlled depth of field,
professional retouching, extreme details,
8k resolution, RAW quality, perfect focus,
published in National Geographic
--no artificial effects, no oversaturation,
no unrealistic lighting, no digital artifacts,
no unnatural shadows, no lens distortion""",

    "logo": """{prompt}, professional logo design,
minimal clean vector style, perfect symmetry,
iconic design, corporate branding quality,
perfect geometry, golden ratio proportions,
professional typography, scalable design,
modern corporate aesthetic, timeless style,
white background, perfect balance,
award winning logo design, featured in Behance
--no gradients, no complex patterns,
no photorealistic elements, no busy details,
no text unless specified, no drop shadows""",

    "watercolor": """{prompt}, traditional watercolor painting,
professional artist quality, wet on wet technique,
organic paint flows, natural pigment granulation,
visible paper texture, controlled color bleeds,
masterful brush strokes, subtle color variations,
traditional watercolor paper texture,
gallery quality artwork, exhibited in art museum,
painted by William Turner
--no digital effects, no sharp edges,
no artificial colors, no photorealistic elements,
no harsh contrast, no dark blacks""",

    "minimalist": """{prompt}, minimalist art design,
clean geometric shapes, perfect composition,
limited color palette, strategic negative space,
professional graphic design, perfect balance,
museum quality minimalism, crisp edges,
modern art style, gallery exhibition quality,
inspired by Mondrian and Malevich
--no complex patterns, no gradients,
no busy details, no realistic elements,
no texture, no organic shapes""",

    "fantasy": """{prompt}, high fantasy artwork,
epic fantasy scene, magical atmosphere,
volumetric god rays, particle effects,
professional digital painting, detailed ornaments,
epic scale, dramatic lighting, detailed environment,
award winning fantasy art, perfect composition,
featured in Wizards of the Coast
--no anime style, no cartoonish elements,
no modern objects, no contemporary clothing,
no historical inaccuracies, no lens flares""",


"cinematic": """{prompt}, cinematic scene,
professional cinema still, movie quality shot,
anamorphic lens, IMAX camera quality,
perfect cinematic lighting, film grain,
dramatic atmosphere, perfect composition,
color graded, spectacular shot, epic scene,
depth of field, professional production value,
shot by Roger Deakins, Christopher Nolan film,
Hollywood blockbuster quality
--no artificial lighting, no staged looking,
no amateur composition, no flat lighting,
no overexposed areas, no digital artifacts""",

    "isometric": """{prompt}, isometric design,
perfect 45-degree angle, clean 3D rendering,
professional architectural visualization,
detailed miniature scene, perfect perspective,
clean sharp edges, professional lighting,
subtle shadows, high attention to detail,
award winning 3D design, featured in Behance,
trending on Artstation
--no incorrect perspective, no mixed angles,
no realistic photography, no lens effects,
no motion blur, no depth of field""",

}

class AsyncHiveImageGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = "https://api.thehive.ai/api/v3/hive/flux-schnell-enhanced"
        
    def _build_prompt(self, base_prompt: str, style: Optional[str] = None) -> str:
        """스타일에 따른 프롬프트 생성"""
        if not style or style not in STYLE_TEMPLATES:
            final_prompt = base_prompt
        else:
            final_prompt = STYLE_TEMPLATES[style].format(prompt=base_prompt)
        
        # 900자로 제한
        return final_prompt[:900] if len(final_prompt) > 900 else final_prompt
    # def _build_prompt(self, base_prompt: str, style: Optional[str] = None) -> str:
    #     """스타일에 따른 프롬프트 생성"""
    #     if not style or style not in STYLE_TEMPLATES:
    #         return base_prompt
    #     return STYLE_TEMPLATES[style].format(prompt=base_prompt)

    async def generate_image(
        self, 
        prompt: str, 
        style: Optional[str] = None,
        size: str = "1024x1024",
    ) -> Dict[str, str]:
        """이미지 생성 함수"""
        try:
            final_prompt = self._build_prompt(prompt, style)
            print("final_prompt: ", final_prompt)
            
            # Parse size string (e.g., "1024x1024") into width and height
            width, height = map(int, size.split('x'))

            
            headers = {
                'authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            }
            
            json_data = {
                'input': {
                    'prompt': final_prompt,
                    'image_size': {
                        'width': width,
                        'height': height
                    },
                    'num_inference_steps': 2,
                    'num_images': 1,
                    'seed': -1,
                    'output_format': 'png',
                }
            }
            
            # Run HTTP request in a thread pool to avoid blocking
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: requests.post(
                    self.endpoint,
                    headers=headers,
                    json=json_data
                )
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status code {response.status_code}")
                
            response_data = response.json()
            
            return {
                "status": "success",
                "url": response_data["output"][0]["url"],
                "prompt": final_prompt
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "prompt": final_prompt if 'final_prompt' in locals() else prompt
            }

    def get_available_styles(self) -> list[str]:
        """사용 가능한 스타일 목록 반환"""
        return list(STYLE_TEMPLATES.keys())

async def get_hive_response_dreamjourney(prompt: str, style: str = None):
    generator = AsyncHiveImageGenerator(API_KEY)
    result = await generator.generate_image(
        prompt=prompt,
        style=style
    )
    
    print("result", result)

    return result