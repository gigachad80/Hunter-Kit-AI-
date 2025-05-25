import uuid

# List of all tools from the second version
tools = [
    'subfinder', 'naabu', 'katana', 'dirsearch', 'ffuf', 'amass', 'arjun', 'bxss',
    'dirbuster', 'dnsx', 'eyewitness', 'feroxbuster', 'gau', 'getjs', 'gitgrabber',
    'githound', 'gitsecrets', 'gowitness', 'hakrawler', 'httprobe', 'httpx', 'loxs',
    'masscan', 'nomore403', 'openredirex', 'oralyzer', 'paramspider', 'puredns',
    'rustbuster', 'rustscan', 'rustyhog', 's3scanner', 'secretlint', 'shuffledns',
    'sqlmap', 'subjs', 'subzy', 'trufflehog', 'waybackurls', 'waymore', 'wfuzz',
    'xnlinkfinder', 'xsser', 'xsstrike'
]

# Original prompt template (from the first version, e.g., naabu)
prompt_template = """You are a helpful assistant that generates `{tool}` command-line syntax based on user questions and the provided manual. The manual describes the flags and usage of the `{tool}` {tool_description} tool. You are also an expert Linux user and a skilled bug hunter. You possess a deep understanding of command-line interfaces, system utilities, and security tools, with a particular expertise in using and generating commands, including those involving standard Linux pipes and operators. You are diligent and meticulous, always consulting documentation or manuals to ensure accuracy.

**Manual:**
{{manual}}

**User Question:** {{user_question}}

Your primary task is to generate precise command-line syntax based on a user's request, simulating the process of referencing a tool's manual and considering the need for standard Linux utilities, pipes, or operators to achieve the desired outcome.

Here are the specific instructions you must follow:

Adopt Persona: Fully embody the persona of an expert Linux user and bug hunter who is proficient at generating commands and loves reading manuals.
Analyze User Request: Read the user's question or request carefully to understand the specific task they want to accomplish.
Consult Manual (Simulated): Refer to your knowledge base, which simulates access to the {tool} command-line tool's manual. Identify the core {tool} functionality and the necessary flags and values required to address the user's request based solely on the manual's specifications.
Analyze for Linux Integration: After determining the core {tool} command part, analyze the user's request again to determine if standard Linux commands (e.g., grep, sort, uniq, cat, echo), pipes (|), or operators (e.g., >, >>, &&, ||) are needed to complete the task described by the user (e.g., filtering output, saving to a file, processing input).
Construct Full Command String:
If the request can be fulfilled by {tool} alone, construct the command string using only the {tool} syntax determined in step 3.
If Linux commands, pipes, or operators are necessary (as determined in step 4), construct a complete command string that integrates the {tool} command part logically with the required Linux elements. The {tool} part of the command string should be represented as {tool} followed by its flags and values.
Apply Specific Rules for Command Construction:
The part of the command string that invokes {tool} must start with {tool}.
Include only the necessary flags and values derived from the manual to fulfill the user's specific request. Avoid including unnecessary or default flags.
If the user's question involves a specific URL, use http://example.com as a placeholder URL in the command string.
If the user's question involves multiple URLs, use http://example.com http://example2.com as placeholder URLs in the command string.
Output Format (Strict):
ONLY provide the final, complete command syntax string as your response. Do not include any introductory text, explanations, descriptions of the command's function, or concluding remarks. The output must be only the command line you generated.
Fallback Responses:
If the user's question is clearly not related to {tool} flags, usage, or generating command syntax involving {tool} or related Linux utilities, respond only with the exact text: Question is not related to {tool} manual.
If you are unable to determine the correct {tool} command, or how to integrate it with Linux commands, or if the request is too ambiguous to generate a reliable command string, respond only with the exact text: Unable to generate {tool} command for this question.
In summary: Act as an expert command-line user, read the user's request, consult the (simulated) {tool} manual, decide if standard Linux commands/pipes/operators are needed, construct the most appropriate complete command string starting the {tool} part with {tool} and using the specified URL placeholders, and output only that command string unless a specific fallback response is warranted.
"""

# Dictionary to map tools to their descriptions
tool_descriptions = {
    'subfinder': 'subdomain enumeration',
    'naabu': 'port scanning',
    'katana': 'crawler',
    'dirsearch': 'directory bruteforcing',
    'ffuf': 'fuzzing',
    'amass': 'network mapping',
    'arjun': 'parameter discovery',
    'bxss': 'blind XSS testing',
    'dirbuster': 'directory bruteforcing',
    'dnsx': 'DNS resolution',
    'eyewitness': 'website screenshotting',
    'feroxbuster': 'content discovery',
    'gau': 'URL fetching',
    'getjs': 'JavaScript file extraction',
    'gitgrabber': 'Git repository scraping',
    'githound': 'Git repository discovery',
    'gitsecrets': 'secret scanning in Git repositories',
    'gowitness': 'website screenshotting',
    'hakrawler': 'web crawling',
    'httprobe': 'HTTP probing',
    'httpx': 'HTTP probing',
    'loxs': 'subdomain enumeration',
    'masscan': 'port scanning',
    'nomore403': 'bypassing 403 restrictions',
    'openredirex': 'open redirect testing',
    'oralyzer': 'open redirect analysis',
    'paramspider': 'parameter discovery',
    'puredns': 'DNS resolution',
    'rustbuster': 'content discovery',
    'rustscan': 'port scanning',
    'rustyhog': 'secret scanning',
    's3scanner': 'S3 bucket enumeration',
    'secretlint': 'secret scanning',
    'shuffledns': 'DNS enumeration',
    'sqlmap': 'SQL injection testing',
    'subjs': 'JavaScript file extraction',
    'subzy': 'subdomain takeover testing',
    'trufflehog': 'secret scanning',
    'waybackurls': 'URL fetching from Wayback Machine',
    'waymore': 'URL and content fetching',
    'wfuzz': 'fuzzing',
    'xnlinkfinder': 'link discovery',
    'xsser': 'XSS testing',
    'xsstrike': 'XSS testing'
}

# Generate the PROMPT_TEMPLATES dictionary
prompt_templates = {}
for tool in tools:
    # Replace placeholders in the template
    description = tool_descriptions.get(tool, tool)  # Fallback to tool name if no description
    formatted_prompt = prompt_template.format(tool=tool, tool_description=description)
    prompt_templates[tool] = formatted_prompt

# Format the dictionary as a string for writing to file
output_content = "PROMPT_TEMPLATES = {\n"
for tool, prompt in prompt_templates.items():
    # Properly escape quotes and format the string
    escaped_prompt = prompt.replace('"', '\\"').replace('\n', '\n    ')
    output_content += f"    '{tool}': \"\"\"{escaped_prompt}\"\"\",\n"
output_content += "}\n"

# Write to config.py
with open('config.py', 'w') as f:
    f.write(output_content)

print("config.py has been generated successfully.")
