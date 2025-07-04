/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  courseSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: '🏠 Wiki Overview',
    },
    
    // Core Development Concepts
    'concepts/containerization',
    'concepts/python-project-setup',
    'concepts/failure-driven-development',
    'concepts/testing-like-you-mean-it',
    
    // AI Development Tools
    'concepts/mastering-claude-code',
    'concepts/claude-code-workshop', 
    'concepts/mastering-gemini-cli',
    'concepts/playwright-mcp-mastery',
    
    // Frontend Development
    'frontend/gui-implementation-patterns',
    'frontend/webassembly-the-fast-lane',
    'frontend/websockets-realtime-communication',
    'frontend/simple-vs-modern-web',
    
    // Backend Development
    'backend/modern-web-scraping',
    'backend/database-architecture',
    'backend/privacy-first-llm-architecture',
    'backend/pattern-based-ai-automation',
    'backend/model-context-protocol-mcp-architecture',
    'concepts/modern-dependency-management',
    
    // Security
    'security/user-agents-and-stealth',
    'security/docker-first-production-security',
    
    // Programming Languages
    'concepts/python-concepts',
    'concepts/golang-concepts',
    'concepts/typescript-deno-concepts',
    
    // Learning Plans
    {
      type: 'doc',
      id: 'learning-plans/index',
      label: '🎯 Learning Plans Overview',
    },
    'learning-plans/plan-1-threat-intelligence',
    'learning-plans/plan-2-static-analysis',
    'learning-plans/plan-3-api-security',
    
    // Hands-on Exercises
    'exercises/claude-code-exercises',
    'exercises/language-exercises',
    'exercises/debugging-exercise',
    
    // Debugging & Troubleshooting
    'debugging-journey',
    
    // Resources & Guides
    'resources/docker-quick-start',
    'resources/security-note',
    'resources/contributing',
  ],
};

module.exports = sidebars;