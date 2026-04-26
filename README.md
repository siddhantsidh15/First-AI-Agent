Things covered in this AI agent implementation
    1. Read, write, get content from out files based on the prompt we provided to the agent.
    2. We have used Google Gemini API
    3. We have allowed our agent to perform operation in the specified directory to prevent any security flaws


# Functionalities implemented in the project ( find them in ./functions directory)

    1. Get File Content - The purpose of this function is to read and return the file contents upto a specified character limit so we don't let AI increase our token count while performing any task
    2. Get File Info - This function gives the information about of a particular file in terms of size, name, is_dir. If the path doesnot exist is_dir is false3. 
    3. Run Python file - It uses subprocess to run a particular python file. We have added checks to prevent it from running any non python file
    4. Write file - If there is any bug, any issue or any information we need and our agent needs to write something in any function we need to give it the access to it using this write file functionality. We have ensured checks that if our agent is in specified working directory then only it will have permission to write any file

# All of the operations are permitted to be performed inside the Calculator directory of this project

To run the project locally provide API keys and run the following command to install dependencies from pyproject.toml / uv.lock

``` 
uv sync

```

# Sample task

Write this in your terminal once project is complete

uv run main.py "Inside the lorem.txt currently it is written something else, can you write me a 200 characters post about ai agents in that file"

uv run main.py "Can you add a modulo operator functionality in my calculator file" -> After this to test the output run 

``` 
uv run calculator/main.py "7 % 3"