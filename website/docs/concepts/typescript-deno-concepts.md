# TypeScript & Deno Learning Concepts

Learn TypeScript and Deno with clear explanations and practical examples, especially designed for Python developers.

## About This Guide

The full TypeScript/Deno concepts guide is available at: [`learning_concepts_typescript_deno.md`](https://github.com/YOUR_USERNAME/learning/blob/main/learning_concepts_typescript_deno.md)

This guide covers:
- TypeScript's type system
- Deno runtime features
- Modern JavaScript patterns
- Practical web development

## Quick TypeScript Reference

### Basic Types

```typescript
// Primitive types
let name: string = "Alice";
let age: number = 30;
let isActive: boolean = true;

// Arrays
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ["a", "b", "c"];

// Objects
let user: {
    name: string;
    age: number;
    email?: string;  // Optional property
} = {
    name: "Alice",
    age: 30
};
```

### Interfaces and Types

```typescript
// Interface (for objects)
interface User {
    id: number;
    name: string;
    email: string;
    isActive?: boolean;  // Optional
    readonly createdAt: Date;  // Can't be changed
}

// Type alias (more flexible)
type ID = string | number;  // Union type
type Status = "pending" | "active" | "inactive";  // Literal types

// Generic types
interface Box<T> {
    value: T;
}

let stringBox: Box<string> = { value: "hello" };
let numberBox: Box<number> = { value: 42 };
```

### Functions

```typescript
// Function with types
function greet(name: string): string {
    return `Hello, ${name}!`;
}

// Arrow function
const add = (a: number, b: number): number => a + b;

// Optional and default parameters
function createUser(
    name: string,
    email: string,
    age?: number,
    role: string = "user"
): User {
    return { id: 1, name, email, createdAt: new Date() };
}

// Generic function
function identity<T>(value: T): T {
    return value;
}
```

### Classes

```typescript
class User {
    private id: number;
    public name: string;
    protected email: string;
    
    constructor(name: string, email: string) {
        this.id = Math.random();
        this.name = name;
        this.email = email;
    }
    
    greet(): string {
        return `Hello, I'm ${this.name}`;
    }
    
    // Getter
    get userId(): number {
        return this.id;
    }
}

// Inheritance
class Admin extends User {
    permissions: string[];
    
    constructor(name: string, email: string, permissions: string[]) {
        super(name, email);
        this.permissions = permissions;
    }
}
```

### Error Handling with Types

```typescript
// Result type pattern
type Result<T, E = Error> = 
    | { ok: true; value: T }
    | { ok: false; error: E };

async function fetchUser(id: number): Promise<Result<User>> {
    try {
        const user = await api.getUser(id);
        return { ok: true, value: user };
    } catch (error) {
        return { ok: false, error: error as Error };
    }
}

// Usage
const result = await fetchUser(123);
if (result.ok) {
    console.log(result.value.name);
} else {
    console.error(result.error.message);
}
```

## Quick Deno Reference

### Why Deno?

- **Secure by default** - No file/network access without permission
- **TypeScript built-in** - No configuration needed
- **Modern APIs** - Uses web standards (fetch, etc.)
- **No node_modules** - Dependencies via URLs
- **Built-in tooling** - Formatter, linter, test runner

### Basic Deno Script

```typescript
// hello.ts
console.log("Hello, Deno!");

// Read a file (needs --allow-read)
const text = await Deno.readTextFile("data.txt");

// Make HTTP request (needs --allow-net)
const response = await fetch("https://api.example.com/data");
const data = await response.json();

// Write file (needs --allow-write)
await Deno.writeTextFile("output.txt", "Hello, World!");
```

### Running Deno

```bash
# Basic run
deno run script.ts

# With permissions
deno run --allow-read --allow-net script.ts

# Watch mode (auto-restart)
deno run --watch script.ts

# Type check only
deno check script.ts
```

### Deno Features

```typescript
// Import from URL
import { serve } from "https://deno.land/std@0.208.0/http/server.ts";

// Top-level await (no wrapper needed!)
const data = await fetch("/api/data");

// Built-in test runner
Deno.test("addition works", () => {
    assertEquals(2 + 2, 4);
});

// Web APIs work out of the box
const ws = new WebSocket("ws://localhost:8080");
localStorage.setItem("key", "value");
```

## TypeScript Best Practices

### 1. Avoid `any`
```typescript
// ❌ Bad
let data: any = getData();

// ✅ Good
let data: unknown = getData();
if (typeof data === 'string') {
    console.log(data.toUpperCase());
}
```

### 2. Use Strict Mode
```json
// tsconfig.json or deno.json
{
  "compilerOptions": {
    "strict": true
  }
}
```

### 3. Prefer Interfaces for Objects
```typescript
// ✅ Interfaces can be extended and merged
interface User {
    name: string;
}

interface User {
    age: number;  // Merged!
}
```

### 4. Use Type Guards
```typescript
function isUser(obj: any): obj is User {
    return obj && typeof obj.name === 'string';
}

if (isUser(data)) {
    // TypeScript knows data is User here
    console.log(data.name);
}
```

## Common Patterns

### Async/Await (Like Python!)
```typescript
async function fetchData(): Promise<Data> {
    const response = await fetch("/api/data");
    return await response.json();
}
```

### Modules (ES Modules)
```typescript
// math.ts
export function add(a: number, b: number): number {
    return a + b;
}

// main.ts
import { add } from "./math.ts";
```

### Type Utilities
```typescript
// Make all properties optional
type PartialUser = Partial<User>;

// Make all properties required
type RequiredUser = Required<User>;

// Pick specific properties
type UserPreview = Pick<User, "id" | "name">;

// Omit properties
type UserWithoutEmail = Omit<User, "email">;
```

## Learning Path

1. **TypeScript Basics** - Types, interfaces, classes
2. **Advanced Types** - Generics, utility types, conditional types
3. **Deno Fundamentals** - Permissions, modules, built-in APIs
4. **Build Projects** - CLI tools, web servers, APIs

For the complete guide, see [learning_concepts_typescript_deno.md](https://github.com/YOUR_USERNAME/learning/blob/main/learning_concepts_typescript_deno.md).

Happy TypeScript coding! 🦕