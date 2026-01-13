import asyncio
from idea_explore_agent.agent import root_agent

async def main():
    try:
        print("Running agent with prompt: 'Hello'")
        response = await root_agent.run_async("Hello")
        print(f"Response type: {type(response)}")
        print(f"Response: {response}")
        
        # Check if response has text attribute
        if hasattr(response, 'text'):
            print(f"Response text: {response.text}")

        # print("\nRunning agent with prompt: 'Create a markdown file named test_verification with content verification'")
        # response = await root_agent.run_async("Create a markdown file named test_verification with content verification")
        # print(f"Response: {response}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
