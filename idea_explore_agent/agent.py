from google.adk.agents.llm_agent import Agent
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

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

def generate_image(prompt: str, output_filename: str) -> str:
    """
    Generates an image using the 'Nano Banana Pro' (Gemini 3 Pro Image) model.
    
    Args:
        prompt: The description of the image to generate.
        output_filename: The path where to save the resulting image.
        
    Returns:
        str: A status message confirming the file path.
    """
    print(f"🎨 Generating image for: '{prompt}'...")
    
    # Ensure directory exists for output_filename
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp", 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig()
            )
        )
        
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    # Found the image data!
                    image_bytes = part.inline_data.data
                    img = Image.open(BytesIO(image_bytes))
                    img.save(output_filename)
                    return ToolResponse(True, f"Image saved to {output_filename}")
        else:
            return ToolResponse(False, "No image data received from model")

    except Exception as e:
        return ToolResponse(False, str(e))

root_agent = Agent(
    model='gemini-2.0-flash-exp',
    name='root_agent',
    description='A helpful assistant to help you explore new ideas and generate new content',
    instruction='''
    Support the user in exploring new ideas and generating new content
    Answer user questions to the best of your knowledge
    
    You can use the following tools:
    - `create_new_markdown`: Create a new markdown file
    - `generate_image`: Generate an image based on a prompt
    ''',
    tools=[create_new_markdown, generate_image],
)

if __name__ == '__main__':
    # print(generate_image('a cat', 'idea_explore_agent/outputs/generated_image.png'))
    pass