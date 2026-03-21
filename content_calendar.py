"""
content_calendar.py
-------------------
Generates a weekly Instagram content calendar for @getrootedmedia
using the Claude API. Outputs a markdown file with 5 posts (one per
content pillar) including topic, hook, caption, hashtags, and timing.

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python content_calendar.py
"""

# ──────────────────────────────────────────────────────────────────────
# 1. IMPORTS — the libraries we need
# ──────────────────────────────────────────────────────────────────────
import os                   # read environment variables
import sys                  # exit with error codes
from datetime import date   # get today's date for the filename
import anthropic            # official Anthropic Python SDK

# ──────────────────────────────────────────────────────────────────────
# 2. CONFIGURATION — things you can tweak without touching the logic
# ──────────────────────────────────────────────────────────────────────

# The Claude model to use. "claude-sonnet-4-6" is fast and affordable
# for content generation. Switch to "claude-opus-4-6" if you want the
# most creative/nuanced output (costs more per request).
MODEL = "claude-sonnet-4-6"

# Maximum tokens (words ≈ tokens × 0.75) Claude can return.
MAX_TOKENS = 4096

# The five content pillars for @getrootedmedia.
# Each pillar targets a different audience segment.
PILLARS = [
    {
        "name": "FOUNDER",
        "description": (
            "Behind-the-scenes of running Get Rooted Media LLC in Ocala, FL. "
            "Personal stories, lessons learned, wins, and the founder journey "
            "of publishing two local print publications."
        ),
    },
    {
        "name": "LISTINGS",
        "description": (
            "Showcasing featured listings, market stats, and real estate trends "
            "in Marion and Sumter Counties. Tied to The Closing Table magazine "
            "(monthly publication for top real estate agents)."
        ),
    },
    {
        "name": "PLAYBOOK",
        "description": (
            "Actionable marketing tips, social media strategies, and business "
            "advice for real estate agents in our market. Positions Get Rooted "
            "Media as a go-to resource for agent growth."
        ),
    },
    {
        "name": "FOLLOWUP",
        "description": (
            "Client follow-up strategies, relationship-building tips, and CRM "
            "best practices for real estate agents. Helps agents stay top-of-mind "
            "after the transaction closes."
        ),
    },
    {
        "name": "NEWOWNER",
        "description": (
            "Content for new homeowners in Marion County — home maintenance tips, "
            "local business spotlights, community events, and settling-in advice. "
            "Tied to The Front Porch magazine (quarterly for new homeowners)."
        ),
    },
]


# ──────────────────────────────────────────────────────────────────────
# 3. BUILD THE PROMPT — tell Claude exactly what we want back
# ──────────────────────────────────────────────────────────────────────

def build_prompt() -> str:
    """
    Constructs the user prompt that tells Claude what to generate.
    We describe the brand, the pillars, and the exact format we expect.
    """

    # Build a numbered list of pillars with their descriptions
    pillar_block = "\n".join(
        f"  {i+1}. **{p['name']}** — {p['description']}"
        for i, p in enumerate(PILLARS)
    )

    # The full prompt sent to Claude
    prompt = f"""\
You are a social media strategist for Get Rooted Media LLC, a local media
company in Ocala, Florida. They publish two print publications:

• The Closing Table — a monthly magazine for top real estate agents in
  Marion and Sumter Counties.
• The Front Porch — a quarterly magazine for new homeowners in Marion County.

Their Instagram handle is @getrootedmedia.

Generate a weekly content calendar with exactly 5 Instagram posts — one for
each content pillar listed below. The week starts on Monday.

Content pillars:
{pillar_block}

For EACH post, provide:
1. **Pillar** — the pillar name in ALL CAPS
2. **Topic** — a specific, timely topic (1 sentence)
3. **Hook** — an attention-grabbing first line for the caption (must stop
   the scroll — use a question, bold statement, or surprising fact)
4. **Caption** — exactly 3 sentences that expand on the hook, deliver value,
   and include a call to action
5. **Hashtags** — exactly 5 relevant hashtags (mix of local, niche, and broad)
6. **Best Day & Time** — the recommended day (Mon–Fri) and time (ET) to post,
   with a brief reason why

Format each post as a markdown section using this exact template:

---

## [PILLAR NAME] — [Day, e.g. Monday]

**Topic:** ...

**Hook:** ...

**Caption:**
...

**Hashtags:** #tag1 #tag2 #tag3 #tag4 #tag5

**Best Time to Post:** Day at Time ET — Reason

---

Make the content feel authentic to Ocala/Marion County. Reference local
landmarks, events, or community vibes when possible. Keep the tone
approachable, confident, and community-first.
"""
    return prompt


# ──────────────────────────────────────────────────────────────────────
# 4. CALL THE CLAUDE API — send the prompt and get a response
# ──────────────────────────────────────────────────────────────────────

def generate_calendar() -> str:
    """
    Sends our prompt to Claude and returns the generated markdown text.
    The Anthropic client automatically reads ANTHROPIC_API_KEY from the
    environment, so we never hardcode the key.
    """

    # Create the API client. It looks for the ANTHROPIC_API_KEY env var.
    client = anthropic.Anthropic()

    # Make the API call using the Messages endpoint
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": build_prompt(),
            }
        ],
    )

    # The response contains a list of content blocks.
    # We grab the text from the first text block.
    for block in response.content:
        if block.type == "text":
            return block.text

    # If somehow no text block was returned, raise an error
    raise RuntimeError("Claude returned no text content in the response.")


# ──────────────────────────────────────────────────────────────────────
# 5. SAVE TO FILE — write the markdown to the output folder
# ──────────────────────────────────────────────────────────────────────

def save_calendar(markdown_content: str) -> str:
    """
    Saves the generated content to output/weekly_calendar_YYYY-MM-DD.md.
    Returns the file path so we can print it to the terminal.
    """

    # Get today's date in YYYY-MM-DD format (e.g. 2026-03-19)
    today = date.today().isoformat()

    # Build the output directory path relative to this script's location.
    # os.path.dirname(__file__) gives us the folder this script lives in.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")

    # Create the output folder if it doesn't exist yet
    os.makedirs(output_dir, exist_ok=True)

    # Build the full file path
    filename = f"weekly_calendar_{today}.md"
    filepath = os.path.join(output_dir, filename)

    # Write the markdown content to the file (UTF-8 encoding)
    with open(filepath, "w", encoding="utf-8") as f:
        # Add a title header at the top of the file
        f.write(f"# @getrootedmedia Weekly Content Calendar\n")
        f.write(f"**Week of {today}**\n\n")
        f.write(markdown_content)

    return filepath


# ──────────────────────────────────────────────────────────────────────
# 6. MAIN — tie it all together
# ──────────────────────────────────────────────────────────────────────

def main():
    """
    Entry point: validates the API key is set, calls Claude,
    saves the result, and prints a confirmation.
    """

    # Check that the API key exists before we try to call the API.
    # This gives a clear error message instead of a cryptic SDK error.
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set.")
        print("Run:  export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    print(f"Generating weekly content calendar for @getrootedmedia...")
    print(f"Using model: {MODEL}")

    # Call Claude and get the markdown content.
    # We wrap this in a try/except so that API errors (bad key, rate limit,
    # network issues) print a clear message instead of a raw Python traceback.
    try:
        markdown = generate_calendar()
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

    # Save to a file
    filepath = save_calendar(markdown)

    print(f"Done! Calendar saved to:\n  {filepath}")


# This block runs only when you execute the script directly
# (not when it's imported as a module by another script).
if __name__ == "__main__":
    main()
