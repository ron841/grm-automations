"""
editor_skill.py — Get Rooted Media Brand Voice Editor
=====================================================
This script takes raw content (a caption, blog excerpt, or social post draft)
and uses the Claude API to rewrite it in GRM's brand voice. It outputs two
versions: a short one for Instagram (under 150 characters) and a long one
(full caption with hashtags). Results are saved as a dated markdown file.

Usage:
    python editor_skill.py "Your raw content here"

Requirements:
    pip install anthropic
    Set your ANTHROPIC_API_KEY environment variable before running.
"""

# ── Imports ──────────────────────────────────────────────────────────────
import os           # For reading environment variables and building file paths
import sys          # For reading command-line arguments
from datetime import date  # For generating today's date in filenames

import anthropic    # The official Anthropic Python library for calling Claude


# ── Configuration ────────────────────────────────────────────────────────
# We read the API key from an environment variable so it is NEVER in our code.
# If the key is missing, we stop immediately with a helpful message.
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("ERROR: ANTHROPIC_API_KEY environment variable is not set.")
    print("Set it with:  export ANTHROPIC_API_KEY='sk-ant-...'")
    sys.exit(1)

# Create the Anthropic client — this is our connection to the Claude API.
client = anthropic.Anthropic(api_key=api_key)

# The model we send requests to. claude-haiku-4-5 is fast and affordable,
# which is ideal for a straightforward editing task like this.
MODEL_ID = "claude-haiku-4-5"


# ── System prompt ────────────────────────────────────────────────────────
# This tells Claude WHO it is and HOW it should write. Think of it as the
# "personality instructions" that shape every response.
SYSTEM_PROMPT = """You are the brand voice editor for Get Rooted Media LLC, a local media company based in Ocala, Florida.

GET ROOTED MEDIA publishes two print publications:
- The Closing Table — a monthly publication for top-producing real estate agents in Marion and Sumter Counties, FL.
- The Front Porch — a quarterly publication for new homeowners moving to Marion County, FL.

BRAND VOICE RULES — follow these exactly:
1. Warm, locally rooted, authoritative but approachable.
2. Write like a trusted neighbor who happens to know everything about Marion County.
3. Reference local landmarks naturally: Ocala National Forest, Silver Springs, the horse farms, World Equestrian Center, downtown Ocala square, The Villages proximity, SR 200 corridor.
4. Never sound like a national brand. Sound like the local insider publication people actually read.
5. Speak TO the audience, not AT them. Use "you" and "your" often.
6. Keep it real — no fluff, no hype, no corporate jargon.

AUDIENCE:
- Top-producing real estate agents in Marion and Sumter Counties
- New homeowners who just moved to Marion County

When given raw content, return EXACTLY this format with no extra commentary:

## Short Version
(Under 150 characters. Punchy, scroll-stopping. No hashtags.)

## Long Version
(Full caption — 3 to 5 sentences in GRM brand voice. End with a line break, then 15–20 relevant hashtags on a single line. Include #GetRootedMedia #OcalaFL #MarionCounty in every set.)"""


# ── Function: call Claude to edit content ────────────────────────────────
def edit_content(raw_text: str) -> str:
    """
    Sends the raw content to Claude with our brand voice instructions.
    Returns Claude's edited response as a string.

    Parameters:
        raw_text (str): The unedited caption, post, or excerpt.

    Returns:
        str: The edited content with Short Version and Long Version sections.
    """
    # client.messages.create() sends a request to the Claude API.
    # - model: which Claude model to use
    # - max_tokens: the maximum length of Claude's response (in tokens, ~4 chars each)
    # - system: the system prompt that sets Claude's role and rules
    # - messages: the conversation — here, just one user message with our raw content
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Edit this raw content for Get Rooted Media's brand voice:\n\n{raw_text}"
            }
        ]
    )

    # The response comes back as a list of content blocks.
    # We loop through and grab the text from any block of type "text".
    result_text = ""
    for block in response.content:
        if block.type == "text":
            result_text += block.text

    return result_text


# ── Function: save the output to a markdown file ────────────────────────
def save_output(edited_content: str, raw_text: str) -> str:
    """
    Saves the edited content as a markdown file in the output/ folder.
    The filename includes today's date so each day gets its own file.

    Parameters:
        edited_content (str): The edited text returned by Claude.
        raw_text (str): The original input (included for reference).

    Returns:
        str: The file path where the output was saved.
    """
    # Build the output directory path relative to this script's location.
    # os.path.dirname(__file__) gives us the folder this script lives in.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")

    # Create the output folder if it doesn't already exist.
    # exist_ok=True means "don't error if the folder is already there."
    os.makedirs(output_dir, exist_ok=True)

    # Build the filename with today's date, e.g. edited_content_2026-03-21.md
    today = date.today().isoformat()  # Returns "YYYY-MM-DD"
    filename = f"edited_content_{today}.md"
    filepath = os.path.join(output_dir, filename)

    # Build the markdown content we'll write to the file.
    # We include the original input at the top for reference.
    markdown = f"""# GRM Edited Content — {today}

---

## Original Input
{raw_text}

---

{edited_content}
"""

    # Write the file. "a" = append mode, so if you run the script multiple
    # times in one day, each edit gets added to the same file.
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(markdown)
        f.write("\n---\n\n")  # Separator between multiple edits

    return filepath


# ── Main: tie it all together ────────────────────────────────────────────
def main():
    """
    Main entry point. Reads raw content from the command line,
    sends it to Claude for editing, and saves the result.
    """
    # Check that the user provided content as a command-line argument.
    # sys.argv[0] is the script name, sys.argv[1] is the first argument.
    if len(sys.argv) < 2:
        print("Usage: python editor_skill.py \"Your raw content here\"")
        print()
        print("Example:")
        print('  python editor_skill.py "Check out this amazing new listing in Ocala!"')
        sys.exit(1)

    # Grab the raw content from the command line.
    raw_text = sys.argv[1]

    print("Sending content to Claude for brand voice editing...")
    print()

    # Step 1: Send to Claude and get the edited versions back.
    # We wrap this in a try/except so that API errors (bad key, rate limit,
    # network issues) print a clear message instead of a raw Python traceback.
    try:
        edited = edit_content(raw_text)
    except anthropic.AuthenticationError:
        print("ERROR: Invalid API key. Check your ANTHROPIC_API_KEY.")
        sys.exit(1)
    except anthropic.RateLimitError:
        print("ERROR: Rate limited by the API. Wait a minute and try again.")
        sys.exit(1)
    except anthropic.APIConnectionError:
        print("ERROR: Could not connect to the Anthropic API. Check your internet.")
        sys.exit(1)
    except anthropic.APIStatusError as e:
        print(f"ERROR: API returned status {e.status_code}: {e.message}")
        sys.exit(1)

    # Step 2: Print the result to the terminal so you can see it right away.
    print(edited)
    print()

    # Step 3: Save to a markdown file for your records.
    filepath = save_output(edited, raw_text)
    print(f"Saved to: {filepath}")


# This block runs only when you execute the script directly (not when imported).
# It's a Python convention — think of it as the "start here" marker.
if __name__ == "__main__":
    main()
