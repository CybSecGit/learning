# Chapter 1: Project Setup
## *The "Hello World" of Existential Dread*

Welcome to the first chapter of our journey into the exciting world of... project setup. Yes, we're starting with the part everyone skips in tutorials. You're welcome.

## Learning Objectives

By the end of this riveting chapter, you'll be able to:
- Set up a Python project without crying (much)
- Understand why virtual environments exist (spoiler: trust issues)
- Install dependencies like a professional (copy-paste expert)
- Configure quality assurance tools (because we pretend we write perfect code)

## The Philosophical Question of Virtual Environments

*"If a Python project runs without a virtual environment, does it make a sound when it breaks?"*

Virtual environments are like personal bubbles for your Python projects. They prevent your code from arguing with other code about which version of a library to use. It's basically relationship counseling for software dependencies.

### Why Virtual Environments Matter

Imagine you're cooking in a shared kitchen (your computer). Without virtual environments, it's like:
- Everyone uses the same spice rack (global packages)
- Recipe A needs "Salt v2.0" but Recipe B needs "Salt v1.5"
- Someone inevitably ruins everything by using the wrong version
- Kitchen explodes (metaphorically... usually)

With virtual environments, each recipe gets its own mini-kitchen. Problem solved, sanity preserved.

## The Modern Python Setup: Enter UV

We're using `uv` instead of the traditional `pip` + `venv` combo because:
1. It's faster (10-100x faster, which matters when you have commitment issues)
2. It's more reliable (fewer "it works on my machine" moments)
3. It's modern (and we like to pretend we're cutting-edge)

Think of `uv` as the Tesla of Python package managers - unnecessarily fast but undeniably cool.

## Hands-On Lab: Setting Up Your Environment

### Step 1: Install UV (The Easy Part)

```bash
# On Linux/macOS (the chosen ones)
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (we don't judge... much)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If `uv` isn't found after installation, you probably need to add it to your PATH. Don't worry, we've all been there.

```bash
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Step 2: Create Your Virtual Environment

```bash
# Navigate to your project (presumably you can handle this)
cd changelogger

# Create the virtual environment (magic happens here)
uv venv

# Activate it (now you're in the bubble)
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows
```

You'll know it worked when your terminal prompt shows `(.venv)`. Congratulations, you're now living in a simulation... within a simulation.

### Step 3: Install Dependencies (The Fun Part)

We're installing some seriously modern packages:

```bash
# The core team
uv pip install rnet selectolax tenacity python-dotenv

# The quality assurance squad
uv pip install pytest black ruff mypy pre-commit bandit
```

#### Meet Your New Dependencies

**`rnet`**: The James Bond of HTTP clients
- Fast, stealthy, and pretends to be a browser
- Makes requests so convincing, websites invite it for coffee

**`selectolax`**: The speed demon HTML parser
- 5-10x faster than BeautifulSoup
- Named by someone who clearly peaked in Latin class

**`tenacity`**: The never-give-up HTTP retry library
- Implements exponential backoff (fancy way of saying "try harder")
- More persistent than a telemarketer

**`python-dotenv`**: The secret keeper
- Loads environment variables from `.env` files
- Prevents you from accidentally committing your API keys (you're welcome)

## Quality Assurance: Or "How to Pretend You Write Perfect Code"

### Initialize Git (Because Version Control is Life)

```bash
git init
git branch -m main  # Because we're progressive
```

### Configure Pre-commit Hooks

Pre-commit hooks are like having a very judgmental friend who checks your code before you share it with the world. They'll catch your mistakes before they become "learning opportunities."

```bash
pre-commit install
```

Our pre-commit configuration includes:
- **Black**: Formats your code (because arguments about indentation are pointless)
- **Ruff**: Lints your code (finds problems you didn't know you had)
- **MyPy**: Type checks your code (pretends Python is statically typed)
- **Bandit**: Security scanner (finds ways hackers could ruin your day)

### Manual Quality Checks

You can run these anytime you feel like your code needs judgment:

```bash
black .        # Make it pretty
ruff check .   # Find the problems
mypy .         # Check the types
pytest         # Run the tests (when you have some)
```

## What We've Accomplished

In this chapter, we've:
- Set up a modern Python development environment
- Learned about virtual environments (and why they matter)
- Installed our toolkit of modern dependencies
- Configured quality assurance tools
- Successfully avoided writing any actual code

## Key Takeaways

1. **Virtual environments prevent dependency hell** (which is a real place, and it's awful)
2. **Modern tools like `uv` make setup faster** (and developers happier)
3. **Quality assurance tools catch mistakes early** (before your users do)
4. **Automation is your friend** (unlike that coworker who "forgets" to run tests)

## Next Chapter Preview

In Chapter 2, we'll dive into the thrilling world of web scraping with `rnet`. We'll learn how to make HTTP requests so convincing that websites will think we're just another human desperately refreshing their changelog page at 3 AM.

Spoiler alert: We'll discuss the art of not getting banned from websites, which is harder than it sounds in today's bot-detection arms race.

---

*"The only way to make sense out of change is to plunge into it, move with it, and join the dance."* - Alan Watts (who clearly never had to monitor software changelogs)

## Exercises

1. **Environment Check**: Verify your virtual environment is working by running `python -c "import rnet; print('Success!')"`
2. **Tool Verification**: Run all the quality assurance tools on your empty project (they should all pass... there's nothing to fail)
3. **Dependency Exploration**: Use `uv pip list` to see what packages were installed as dependencies of your dependencies (welcome to dependency inception)

**Bonus Challenge**: Try to explain to a non-programmer why you need a separate environment for each project. Watch their eyes glaze over. Realize why we automate everything.
