---
id: index
title: Learning Plans Overview
sidebar_label: 📚 Overview
description: Overview of comprehensive learning plans that combine programming skills with security concepts
keywords: [learning, golang, security, overview, plans]
---

# Learning Plans
## *Or: How I Learned to Code While Accidentally Becoming a Cybersecurity Expert*

> "The best way to learn two complex topics simultaneously is to build something slightly dangerous with both." - Anonymous Developer Who Definitely Shouldn't Give Advice

This section contains comprehensive learning plans that combine programming skills with security concepts. Each plan is designed as a complete journey from "what's a variable?" to "I can't believe I just built that!" using the Feynman technique (explain it like you're 5) with enough dark humor to keep you caffeinated.

## Why Learning Plans?

Traditional tutorials teach you syntax. Learning plans teach you to **think** like a developer while **understanding** security implications. Instead of building another todo app, you'll build tools that could theoretically get you in trouble with your IT department (but won't, because we're responsible developers who read security guidelines).

Think of these as "choose your own adventure" books, but instead of fighting dragons, you're fighting segmentation faults and learning why password hashing exists.

## Why Go? (And Not Python or Rust)

### 🐍 Why Go Over Python?
*"Python is great, but sometimes you need to go fast... really fast."*

**The Honest Truth**: Python is fantastic for learning programming concepts, but when you're building security tools that need to:
- Process thousands of network requests per second
- Handle massive datasets without eating all your RAM
- Deploy as single binaries without dependency hell
- Scale horizontally without the Global Interpreter Lock (GIL) getting in your way

...Go starts looking pretty attractive.

**Real-World Example**: A Python vulnerability scanner might analyze 10 files per second. The same logic in Go? Try 1000+ files per second. When you're scanning enterprise codebases with millions of lines of code, that difference matters.

**But Here's the Thing**: Go's simplicity means you can focus on learning security concepts instead of wrestling with language complexity. Python has 7 ways to do everything; Go has 1 good way. This actually makes learning faster, not slower.

### 🦀 Why Go Instead of Rust?
*"Rust is incredible, but learning memory management while learning security is like learning to juggle while riding a unicycle."*

**The Memory Safety Conversation**: Yes, Rust has superior memory safety. Yes, it's blazingly fast. Yes, it prevents an entire class of security vulnerabilities. But here's what nobody tells you: **Rust's learning curve is a cliff**.

**Go's Sweet Spot**: Go gives you:
- Memory safety through garbage collection (good enough for 99% of security tools)
- Concurrency that's actually fun to use (goroutines > threads)
- Compilation speed that doesn't make you question your life choices
- A standard library that handles networking, HTTP, and JSON without external dependencies
- Code that your future self (and teammates) can actually read

**When You'd Choose Rust**: Building a cryptographic library, writing a kernel module, or creating a performance-critical parser that processes terabytes of data. For learning security concepts through hands-on projects? Go hits the sweet spot.

**The Bottom Line**: You can learn Go in weeks and start building real security tools. Rust takes months to feel comfortable with, and you'll spend more time fighting the borrow checker than learning about taint analysis.

## Available Learning Plans

### 🎯 Current Learning Plans

- **[Plan 1: Go + Dark Web Intelligence Gathering](./plan-1-threat-intelligence)** 
  - For when you want to learn Go and accidentally become a threat intelligence analyst
  - **Skills Learned**: Go fundamentals, HTTP clients, Tor networking, data parsing, security mindset
  - **Duration**: 4-6 weeks (3-4 hours/week)
  - **Prerequisites**: Basic programming knowledge, ability to install software without breaking your computer

- **[Plan 2: Go + Static Code Analysis & Security Tooling](./plan-2-static-analysis)**
  - For when you want to build the tools that find vulnerabilities before attackers do
  - **Skills Learned**: AST parsing, taint analysis, symbolic execution, ML for code analysis, dataflow analysis
  - **Duration**: 6-8 weeks (4-5 hours/week)
  - **Prerequisites**: Completion of Plan 1 or equivalent Go experience

- **[Plan 3: API Security Testing & Automation](./plan-3-api-security)**
  - For when you want to secure and automate API security testing
  - **Skills Learned**: API security testing, OAuth flows, OWASP API Top 10, automation
  - **Duration**: 4-6 weeks (3-4 hours/week)
  - **Prerequisites**: Basic HTTP knowledge, programming experience

- **[Plan 4: AWS CDK TypeScript Mastery](./plan-4-aws-cdk-typescript)**
  - From CloudFormation veteran to CDK wizard with TypeScript
  - **Skills Learned**: TypeScript, CDK constructs, event-driven architecture, enterprise patterns
  - **Duration**: 7-8 weeks intensive learning
  - **Prerequisites**: CloudFormation proficiency, AWS knowledge, basic programming

- **[Plan 5: Makefile Mastery & Next.js Development](./plan-5-makefile-nextjs)**
  - From command line chaos to full-stack orchestration
  - **Skills Learned**: Makefile automation, Next.js 15+, TypeScript, testing, CI/CD
  - **Duration**: 6-7 weeks of deliberate practice
  - **Prerequisites**: Basic command line, JavaScript knowledge

- **[Plan 6: Go TUI Development with Charm](./plan-6-go-tui-charm)**
  - From command line peasant to terminal UI aristocrat
  - **Skills Learned**: Bubble Tea framework, Lip Gloss styling, reactive TUI patterns, SSH apps
  - **Duration**: 6-8 weeks of terminal enlightenment
  - **Prerequisites**: Basic Go knowledge, terminal comfort, hatred for boring CLIs

### 🚀 Future Learning Plans

- **Plan 7: Python + Vulnerability Scanner Builder** - Learn Python while building a network security scanner
- **Plan 8: TypeScript + Browser Security Extension** - Frontend skills meets security tooling
- **Plan 9: Rust + Cryptographic Tool Suite** - Memory safety meets cryptography
- **Plan 10: C + Reverse Engineering Lab** - Low-level programming meets malware analysis (defensive only!)

## Getting Started

Each learning plan is designed to be:
- **Self-contained**: You can start with any plan that matches your skill level
- **Hands-on**: Every concept is learned by building real, working software
- **Production-ready**: By the end, you'll have deployable tools you can actually use
- **Thoroughly tested**: Comprehensive testing ensures your code works correctly
- **Security-focused**: All plans emphasize defensive security practices

Choose a plan that interests you, set up your development environment, and start building! Remember: The goal isn't to rush through this. Take time to understand each concept deeply. The security field rewards those who think thoroughly, not those who code quickly.

---

*"In learning, you will teach, and in teaching, you will learn."* - Phil Collins (yes, the drummer, but it applies to programming too)