# Debugging Exercise

Test your debugging skills with this challenging exercise that simulates real-world debugging scenarios.

## The Challenge

**File:** `course/exercises/debugging-exercise-01.py`

You're given a broken changelog scraper with multiple bugs. Your mission: fix them all using systematic debugging techniques.

### Known Issues (But Not Their Causes!)

1. The scraper times out on some websites
2. It crashes with a mysterious error on others
3. Sometimes it returns empty results when there should be data
4. The rate limiting doesn't seem to work properly

### Your Toolkit

- Print debugging (the classic)
- Python debugger (`pdb`)
- Logging statements
- Type checking
- Unit tests

### To Start

```bash
# Run the broken scraper
python course/exercises/debugging-exercise-01.py

# You'll see various errors - your job is to fix them!
```

## Debugging Strategy

### 1. Reproduce the Issue
- Run the code and observe the error
- Note the exact error message and stack trace
- Try to consistently reproduce the problem

### 2. Form a Hypothesis
- Based on the error, what might be wrong?
- Consider edge cases
- Think about timing issues

### 3. Test Your Theory
- Add logging or print statements
- Use the debugger to step through code
- Isolate the problematic section

### 4. Fix and Verify
- Implement your fix
- Test that it resolves the issue
- Ensure you haven't broken anything else

## Common Debugging Patterns

### The "It Works on My Machine" Bug
Often related to:
- Environment differences
- Missing dependencies
- Hardcoded paths

### The "Intermittent Failure"
Usually caused by:
- Race conditions
- Network timeouts
- Resource limitations

### The "Silent Failure"
Watch out for:
- Swallowed exceptions
- Empty catch blocks
- Missing error checks

## Tips for This Exercise

1. **Start with the stack trace** - It usually points to the problem area
2. **Check your assumptions** - What you think the code does vs. what it actually does
3. **Simplify to isolate** - Comment out code until the error disappears
4. **One fix at a time** - Don't try to fix everything at once
5. **Write tests** - Ensure your fixes actually work

## Learning Objectives

By completing this exercise, you'll practice:
- Reading and understanding error messages
- Using debugging tools effectively
- Thinking systematically about problems
- Writing defensive code
- Adding proper error handling

## Spoiler-Free Hints

<details>
<summary>Hint 1: Timeout Issues</summary>

Check the default timeout values. Are they reasonable for all scenarios?
</details>

<details>
<summary>Hint 2: Mysterious Crashes</summary>

Look for places where the code assumes something exists that might not.
</details>

<details>
<summary>Hint 3: Empty Results</summary>

Is the HTML parser looking for the right elements? Has the website structure changed?
</details>

<details>
<summary>Hint 4: Rate Limiting</summary>

How is time being tracked? Is it thread-safe?
</details>

## After Completing

Once you've fixed all the bugs:

1. **Document your fixes** - What was wrong and how you fixed it
2. **Add tests** - Ensure the bugs don't come back
3. **Share your experience** - What debugging technique worked best?
4. **Level up** - Try adding new features without breaking anything

Remember: Every bug fixed makes you a better developer! 🐛➡️🦋