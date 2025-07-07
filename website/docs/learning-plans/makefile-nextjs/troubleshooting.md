# Troubleshooting Guide
## Common Issues and How to Fix Them

> "99% of programming is fixing the problems caused by the 1% of programming that's actually programming."

## 🔧 Quick Fixes

Before diving deep, try these:

```bash
# The "Turn it off and on again" of web development
rm -rf node_modules .next
pnpm install
pnpm dev

# If that doesn't work, clear ALL caches
rm -rf node_modules .next .cache ~/.npm ~/.pnpm-store
pnpm install --force
```

## 📋 Common Issues Index

- [Installation Problems](#installation-problems)
- [Build Errors](#build-errors)
- [Runtime Errors](#runtime-errors)
- [Deployment Issues](#deployment-issues)
- [Performance Problems](#performance-problems)
- [Development Environment](#development-environment)

## Installation Problems

### Issue: "EACCES: permission denied"

**Symptom:**
```
npm ERR! code EACCES
npm ERR! syscall mkdir
npm ERR! path /usr/local/lib/node_modules
```

**Solution:**
```bash
# Option 1: Change npm's default directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Option 2: Use a Node version manager (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
```

### Issue: "Cannot find module 'X'"

**Symptom:**
```
Error: Cannot find module '@/components/Header'
```

**Solutions:**

1. **Check tsconfig.json paths:**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

2. **Clear TypeScript cache:**
```bash
rm -rf tsconfig.tsbuildinfo
pnpm tsc --build --clean
```

3. **Restart TypeScript server in VS Code:**
- Press `Cmd/Ctrl + Shift + P`
- Type "TypeScript: Restart TS Server"

### Issue: "pnpm: command not found"

**Solution:**
```bash
# Install pnpm globally
npm install -g pnpm

# Or use corepack (built into Node.js 16+)
corepack enable
corepack prepare pnpm@latest --activate
```

## Build Errors

### Issue: "Cannot read properties of undefined"

**Symptom:**
```
TypeError: Cannot read properties of undefined (reading 'map')
```

**Common Causes and Solutions:**

1. **Data not loaded:**
```typescript
// WRONG
function List({ items }) {
  return items.map(item => <div>{item}</div>);
}

// RIGHT - Add safety check
function List({ items }) {
  return items?.map(item => <div>{item}</div>) || null;
}

// BETTER - With loading state
function List({ items }) {
  if (!items) return <div>Loading...</div>;
  if (items.length === 0) return <div>No items</div>;
  return items.map(item => <div key={item.id}>{item.name}</div>);
}
```

2. **Async data in Server Components:**
```typescript
// RIGHT - Await the data
async function Page() {
  const data = await fetchData(); // Don't forget await!
  return <List items={data} />;
}
```

### Issue: "Module parse failed: Unexpected token"

**Symptom:**
```
Module parse failed: Unexpected token (1:0)
You may need an appropriate loader to handle this file type.
```

**Solution:**
```javascript
// next.config.js
module.exports = {
  webpack: (config) => {
    // Add loader for special file types
    config.module.rules.push({
      test: /\.svg$/,
      use: ['@svgr/webpack'],
    });
    
    return config;
  },
};
```

### Issue: "Out of memory" During Build

**Symptom:**
```
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
```

**Solutions:**

1. **Increase Node.js memory:**
```bash
# In package.json
{
  "scripts": {
    "build": "NODE_OPTIONS='--max-old-space-size=4096' next build"
  }
}
```

2. **Optimize imports:**
```typescript
// WRONG - Imports entire library
import _ from 'lodash';

// RIGHT - Import only what you need
import debounce from 'lodash/debounce';
```

3. **Use dynamic imports for large components:**
```typescript
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false,
});
```

## Runtime Errors

### Issue: "Hydration failed"

**Full Error:**
```
Error: Hydration failed because the initial UI does not match what was rendered on the server.
```

**Common Causes and Solutions:**

1. **Date/Time rendering:**
```typescript
// WRONG
<div>{new Date().toLocaleString()}</div>

// RIGHT
function Clock() {
  const [time, setTime] = useState(null);
  
  useEffect(() => {
    setTime(new Date().toLocaleString());
  }, []);
  
  return <div>{time || 'Loading...'}</div>;
}
```

2. **Browser-only APIs:**
```typescript
// WRONG
const width = window.innerWidth;

// RIGHT
const [width, setWidth] = useState(0);

useEffect(() => {
  setWidth(window.innerWidth);
  
  const handleResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

3. **Conditional rendering based on client state:**
```typescript
// Use suppressHydrationWarning for intentional differences
<div suppressHydrationWarning>
  {typeof window !== 'undefined' ? 'Client' : 'Server'}
</div>
```

### Issue: "useState is not defined"

**Symptom:**
```
ReferenceError: useState is not defined
```

**Solution:**
```typescript
// Add 'use client' directive
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  // ...
}
```

### Issue: "Headers already sent"

**Symptom:**
```
Error: Can't set headers after they are sent to the client
```

**Solution in API Routes:**
```typescript
// WRONG - Multiple responses
export async function GET() {
  if (someCondition) {
    return NextResponse.json({ error: 'Bad request' });
  }
  // This will execute even after the return above!
  return NextResponse.json({ data: 'Success' });
}

// RIGHT - Use early return properly
export async function GET() {
  if (someCondition) {
    return NextResponse.json({ error: 'Bad request' });
  }
  
  // Only reaches here if condition is false
  return NextResponse.json({ data: 'Success' });
}
```

## Deployment Issues

### Issue: "Build failed on Vercel"

**Common Causes:**

1. **Missing environment variables:**
```bash
# Check locally with production env
NODE_ENV=production pnpm build
```

2. **Case sensitivity (works on Mac, fails on Linux):**
```typescript
// WRONG - Inconsistent casing
import Header from '@/components/header';  // File is Header.tsx

// RIGHT - Match exact file name
import Header from '@/components/Header';
```

3. **Dependencies in devDependencies:**
```json
// Move build-time deps to dependencies
{
  "dependencies": {
    "@types/node": "^20.0.0",  // Needed for build
    "typescript": "^5.0.0"      // Needed for build
  }
}
```

### Issue: "504 Gateway Timeout"

**Solution:**
```typescript
// Increase function timeout in vercel.json
{
  "functions": {
    "app/api/slow-endpoint/route.ts": {
      "maxDuration": 30
    }
  }
}

// Or use edge runtime for better performance
export const runtime = 'edge';
```

### Issue: "Static export error"

**Symptom:**
```
Error: Image Optimization using Next.js' default loader is not compatible with `next export`.
```

**Solution:**
```javascript
// next.config.js
module.exports = {
  images: {
    unoptimized: true,  // For static export
  },
  output: 'export',
};
```

## Performance Problems

### Issue: "Slow page loads"

**Diagnostic Steps:**

1. **Check bundle size:**
```bash
# Analyze bundle
ANALYZE=true pnpm build

# Check for large dependencies
npx bundle-phobia-cli package.json
```

2. **Implement code splitting:**
```typescript
// Split by route (automatic in App Router)
// Split by component
const Modal = dynamic(() => import('./Modal'));

// Split by library
const Chart = dynamic(() => import('react-chartjs-2'), {
  ssr: false,
});
```

3. **Optimize images:**
```typescript
import Image from 'next/image';

// Use Next.js Image component
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // For above-the-fold images
  placeholder="blur"
  blurDataURL={blurDataUrl}
/>
```

### Issue: "Memory leaks"

**Detection:**
```typescript
// Add memory monitoring
if (process.env.NODE_ENV === 'development') {
  setInterval(() => {
    console.log('Memory Usage:', process.memoryUsage());
  }, 10000);
}
```

**Common Causes:**
1. **Event listeners not cleaned up:**
```typescript
useEffect(() => {
  const handler = () => console.log('scroll');
  window.addEventListener('scroll', handler);
  
  // Don't forget cleanup!
  return () => window.removeEventListener('scroll', handler);
}, []);
```

2. **Timers not cleared:**
```typescript
useEffect(() => {
  const timer = setInterval(() => {
    // Do something
  }, 1000);
  
  return () => clearInterval(timer);
}, []);
```

## Development Environment

### Issue: "Port 3000 already in use"

**Solution:**
```bash
# Find and kill process
lsof -ti:3000 | xargs kill -9

# Or use a different port
PORT=3001 pnpm dev
```

### Issue: "Hot reload not working"

**Solutions:**

1. **Check for file watching limits:**
```bash
# Linux: Increase file watchers
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

2. **Clear Next.js cache:**
```bash
rm -rf .next
pnpm dev
```

3. **Check webpack config:**
```javascript
// next.config.js
module.exports = {
  webpack: (config) => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    };
    return config;
  },
};
```

### Issue: "TypeScript errors but code works"

**Solution:**
```bash
# Restart TS server
# In VS Code: Cmd/Ctrl + Shift + P -> "TypeScript: Restart TS Server"

# Clear TS cache
rm -rf tsconfig.tsbuildinfo
rm -rf node_modules/.cache/typescript

# Regenerate types
pnpm tsc --build --force
```

## 🚨 Emergency Contacts

When all else fails:

1. **Next.js Discord**: https://nextjs.org/discord
2. **Stack Overflow**: Tag with `next.js` and `makefile`
3. **GitHub Issues**: Check existing issues first
4. **Twitter**: `#nextjs` community is helpful

## 📚 Debugging Resources

- [Next.js Error Reference](https://nextjs.org/docs/messages)
- [React Error Decoder](https://react.dev/errors)
- [GNU Make Debugging](https://www.gnu.org/software/make/manual/html_node/Debugging.html)
- [Node.js Debugging Guide](https://nodejs.org/en/docs/guides/debugging-getting-started/)

---

*Remember: Every error is just a learning opportunity in disguise. A very annoying, time-consuming disguise.*