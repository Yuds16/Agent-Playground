from google.adk.agents.llm_agent import Agent
from google import genai
from diffusers import DiffusionPipeline
import torch

import os
import dotenv

dotenv.load_dotenv()

class ToolResponse:
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message
    
    def __str__(self):
        return f"{'Success' if self.success else 'Failed'}: {self.message}"

def create_new_markdown(name: str, content: str):
    """Creates new markdown file if not exists with specified name and content.

    Args:
        name (str): The name of the markdown file.
        content (str): The content of the markdown file.

    Returns:
        ToolResponse: A response object containing the result of the operation.
    """

    output_dir = 'idea_explore_agent/output/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if os.path.exists(f'{output_dir}{name}.md'):
        return ToolResponse(False, f'{name}.md already exists')

    try:
        with open(f'{output_dir}{name}.md', 'w+') as f:
            f.write(content)
    except Exception as e:
        return ToolResponse(False, str(e))
    
    return ToolResponse(True, f'{name}.md created successfully')

def generate_image(prompt: str):
    client = genai.Client(
        api_key=os.getenv('GOOGLE_API_KEY', '')
    )

    prompt = f"Generate an image of the following prompt: {prompt}. Return only the image."

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt]
    )

    for part in response.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save("idea_explore_agent/outputs/generated_image.png")

    return response

def generate_image_stablediffuse(prompt: str):
    try:
        pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large-tensorrt", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")

        image = pipe(prompt=prompt).images[0]
        image.save("idea_explore_agent/outputs/generated_image.png")
    except Exception as e:
        return ToolResponse(False, str(e))
    
    return ToolResponse(True, "Image generated successfully")
    
    return image

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant to help you explore new ideas and generate new content',
#     instruction='''
#     Support the user in exploring new ideas and generating new content
#     Answer user questions to the best of your knowledge
    
#     You can use the following tools:
#     - `create_new_markdown`: Create a new markdown file
#     ''',
#     tools=[create_new_markdown],
# )

if __name__ == '__main__':
    print(generate_image_stablediffuse('a cat'))