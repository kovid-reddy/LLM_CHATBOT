"""
Full Agentic AI System
Main program that uses Gemini LLM + tools to break down and execute multi-step tasks
"""

import os
import re
import json
import logging
import time
from typing import List, Dict, Any, Tuple
from datetime import datetime

import google.generativeai as genai
from dotenv import load_dotenv
from colorama import init, Fore, Style

from calculator_tool import calculate
from translator_tool import translate_to_german

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

class AgenticAI:
    """
    Main Agentic AI class that orchestrates Gemini LLM-based task breakdown and execution
    """
    
    def __init__(self):
        """Initialize the agent with Gemini API key and tools"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Available action types
        self.action_types = ['calculate', 'translate', 'translate_to', 'answer']
        
        # Initialize interaction counter
        self.interaction_count = 0
    
    def create_step_breakdown_prompt(self, user_input: str) -> str:
        """
        Create a prompt that instructs the LLM to break down the input into steps.
        
        Args:
            user_input (str): The user's natural language input
            
        Returns:
            str: Formatted prompt for the LLM
        """
        return f"""You are an AI task planner. Your job is to break down the user's request into specific steps that can be executed by different tools.

IMPORTANT: You should NOT execute the steps yourself. Only classify and break down the tasks.

Available action types:
- calculate: For mathematical operations (addition, multiplication)
- translate: For translating English phrases to German
- translate_to: For translating phrases to a specific language (e.g., "Hello" to "Hola")
- answer: For direct question answering that doesn't require tools

User input: "{user_input}"

Break this down into steps using the following format:
Step 1: action: <action_type>, content: <task or content>
Step 2: action: <action_type>, content: <task or content>
...

Examples:
- For "Add 5 and 3, then translate 'hello' to German":
  Step 1: action: calculate, content: add 5 and 3
  Step 2: action: translate, content: hello

- For "Translate 'Good Morning' to Japanese":
  Step 1: action: translate_to, content: Good Morning to Japanese

- For "What is the capital of France?":
  Step 1: action: answer, content: What is the capital of France?

- For "Multiply 4 and 6, then add 10 and 20":
  Step 1: action: calculate, content: multiply 4 and 6
  Step 2: action: calculate, content: add 10 and 20

- For "Translate 'Hello' to Spanish and add 5 and 3":
  Step 1: action: translate_to, content: Hello to Spanish
  Step 2: action: calculate, content: add 5 and 3

Please break down the user's request into steps:"""

    def parse_llm_response(self, response: str) -> List[Dict[str, str]]:
        """
        Parse the LLM response to extract steps.
        
        Args:
            response (str): LLM response containing steps
            
        Returns:
            List[Dict[str, str]]: List of parsed steps with action and content
        """
        steps = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('Step'):
                # Extract step number, action, and content
                match = re.match(r'Step \d+: action: (\w+), content: (.+)', line)
                if match:
                    action = match.group(1).lower()
                    content = match.group(2).strip()
                    
                    if action in self.action_types:
                        steps.append({
                            'action': action,
                            'content': content
                        })
        
        return steps

    def execute_calculation(self, content: str) -> str:
        """
        Execute a calculation step.
        
        Args:
            content (str): Calculation content (e.g., "add 5 and 3")
            
        Returns:
            str: Result of the calculation
        """
        try:
            # Extract numbers and operation from content
            content_lower = content.lower()
            
            if 'add' in content_lower or 'addition' in content_lower:
                # Find numbers in the content
                numbers = re.findall(r'\d+', content)
                if len(numbers) >= 2:
                    result = calculate('add', float(numbers[0]), float(numbers[1]))
                    return f"Addition result: {result}"
                else:
                    return f"Error: Could not extract two numbers from '{content}'"
            
            elif 'multiply' in content_lower or 'multiplication' in content_lower:
                # Find numbers in the content
                numbers = re.findall(r'\d+', content)
                if len(numbers) >= 2:
                    result = calculate('multiply', float(numbers[0]), float(numbers[1]))
                    return f"Multiplication result: {result}"
                else:
                    return f"Error: Could not extract two numbers from '{content}'"
            
            else:
                return f"Error: Unsupported calculation operation in '{content}'"
                
        except Exception as e:
            return f"Error executing calculation '{content}': {str(e)}"

    def execute_translation(self, content: str) -> str:
        """
        Execute a translation step.
        
        Args:
            content (str): Translation content (e.g., "hello" or "Hello to Japanese")
            
        Returns:
            str: Translation result
        """
        try:
            # Clean the content (remove quotes if present)
            clean_content = content.strip().strip('"\'')
            
            # Check if this is a multi-language translation (contains "to [Language]")
            if " to " in clean_content.lower():
                # Parse for multi-language translation
                parts = clean_content.split(" to ")
                if len(parts) == 2:
                    text_to_translate = parts[0].strip()
                    target_language = parts[1].strip()
                    
                    # Import the multi-language translator
                    from translator_tool import translate_to_language
                    result = translate_to_language(text_to_translate, target_language)
                    
                    # Get translation method for feedback
                    from translator_tool import translator
                    method = translator.get_translation_method()
                    
                    return f"Translation ({method}): {result}"
            
            # Default to German translation (backward compatibility)
            result = translate_to_german(clean_content)
            
            # Get translation method for feedback
            from translator_tool import translator
            method = translator.get_translation_method()
            
            return f"Translation ({method}): {result}"
        except Exception as e:
            return f"Error executing translation '{content}': {str(e)}"

    def execute_answer(self, content: str) -> str:
        """
        Execute a direct answer step using the Gemini LLM.
        
        Args:
            content (str): Question content
            
        Returns:
            str: LLM's answer
        """
        try:
            response = self.model.generate_content(content)
            return f"Answer: {response.text.strip()}"
        except Exception as e:
            return f"Error getting answer for '{content}': {str(e)}"

    def execute_step(self, step: Dict[str, str]) -> str:
        """
        Execute a single step based on its action type.
        
        Args:
            step (Dict[str, str]): Step with 'action' and 'content' keys
            
        Returns:
            str: Result of the step execution
        """
        action = step['action']
        content = step['content']
        
        if action == 'calculate':
            return self.execute_calculation(content)
        elif action == 'translate':
            return self.execute_translation(content)
        elif action == 'translate_to':
            return self.execute_translation(content) # Assuming translate_to is also a translation
        elif action == 'answer':
            return self.execute_answer(content)
        else:
            return f"Error: Unknown action type '{action}'"

    def process_user_input(self, user_input: str) -> Tuple[List[Dict[str, str]], List[str]]:
        """
        Process user input through the complete agentic pipeline.
        
        Args:
            user_input (str): User's natural language input
            
        Returns:
            Tuple[List[Dict[str, str]], List[str]]: Steps and results
        """
        start_time = time.time()
        api_calls = 0
        tokens_used = 0
        
        try:
            # Step 1: Use LLM to break down the input into steps
            prompt = self.create_step_breakdown_prompt(user_input)
            
            logging.info(f"Breaking down user input: {user_input}")
            
            response = self.model.generate_content(prompt)
            api_calls += 1
            llm_response = response.text.strip()
            
            logging.info(f"LLM breakdown response: {llm_response}")
            
            # Step 2: Parse the LLM response to extract steps
            steps = self.parse_llm_response(llm_response)
            logging.info(f"Parsed {len(steps)} steps: {steps}")
            
            if not steps:
                return [], ["Error: Could not parse any steps from LLM response"]
            
            # Step 3: Execute each step sequentially
            results = []
            for i, step in enumerate(steps, 1):
                logging.info(f"Executing step {i}: {step}")
                result = self.execute_step(step)
                results.append(f"Step {i} ({step['action']}): {result}")
                logging.info(f"Step {i} result: {result}")
            
            return steps, results
            
        except Exception as e:
            logging.error(f"Error processing user input: {str(e)}")
            return [], [f"Error: {str(e)}"]

    def run_interactive(self):
        """Run the agent in interactive CLI mode"""
        print(f"{Fore.CYAN}🤖 Agentic AI System - Interactive Mode{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'quit' or 'exit' to stop the program{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'help' to see example inputs{Style.RESET_ALL}\n")
        
        while True:
            try:
                user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"{Fore.CYAN}Goodbye! 👋{Style.RESET_ALL}")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if not user_input:
                    continue
                
                # Process the input
                steps, results = self.process_user_input(user_input)
                
                # Display results
                print(f"\n{Fore.BLUE}🤖 Agent Results:{Style.RESET_ALL}")
                if results:
                    for result in results:
                        print(f"  {Fore.WHITE}• {result}{Style.RESET_ALL}")
                else:
                    print(f"  {Fore.RED}No results generated{Style.RESET_ALL}")
                
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}Goodbye! 👋{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                logging.error(f"Interactive mode error: {str(e)}")

    def show_help(self):
        """Show help with example inputs"""
        print(f"\n{Fore.CYAN}📚 Example Inputs:{Style.RESET_ALL}")
        examples = [
            "Translate 'Good Morning' into German and then multiply 5 and 6.",
            "Add 10 and 20, then translate 'Have a nice day' into German.",
            "Tell me the capital of Italy, then multiply 12 and 12.",
            "Add 2 and 2 and multiply 3 and 3.",
            "What is the distance between Earth and Mars?"
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"  {Fore.YELLOW}{i}.{Style.RESET_ALL} {example}")
        print()

def main():
    """Main function to run the agentic AI system"""
    try:
        agent = AgenticAI()
        agent.run_interactive()
    except ValueError as e:
        print(f"{Fore.RED}Configuration Error: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please set your GEMINI_API_KEY environment variable.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
        logging.error(f"Main function error: {str(e)}")

if __name__ == "__main__":
    main()