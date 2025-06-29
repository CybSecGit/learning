# TypeScript & Deno Learning Concepts
## *Or: How I Learned to Stop Worrying and Love the Types (With a Runtime That Makes Sense)*

> "Any application that can be written in JavaScript, will eventually be written in JavaScript." - Jeff Atwood  
> "...but it'll be better with TypeScript!" - Every TypeScript Developer

This comprehensive guide explains TypeScript and Deno concepts using the Feynman technique, building on your Python knowledge. We'll explore how TypeScript adds sanity to JavaScript and how Deno makes the runtime actually pleasant to use.

## Table of Contents

### 🎯 TypeScript Fundamentals
- [TypeScript vs Python: Type Systems Compared](#typescript-vs-python-type-systems-compared)
- [Basic Types and Annotations](#basic-types-and-annotations)
- [Interfaces and Type Aliases](#interfaces-and-type-aliases)
- [Classes and OOP](#classes-and-oop)
- [Functions and Generics](#functions-and-generics)
- [Union and Intersection Types](#union-and-intersection-types)
- [Type Guards and Narrowing](#type-guards-and-narrowing)
- [Utility Types](#utility-types)

### 🦕 Deno: The Better Runtime
- [Why Deno? (Node.js Done Right)](#why-deno-nodejs-done-right)
- [Security First](#security-first)
- [Built-in Tooling](#built-in-tooling)
- [URL Imports](#url-imports)
- [Standard Library](#standard-library)
- [Web APIs Everywhere](#web-apis-everywhere)

### 📦 Module System and Dependencies
- [ES Modules Only](#es-modules-only)
- [Import Maps](#import-maps)
- [Dependency Management](#dependency-management)

### 🔄 Async Programming
- [Promises and Async/Await](#promises-and-asyncawait)
- [Top-Level Await](#top-level-await)

### 🛠️ Development Workflow
- [Testing with Deno](#testing-with-deno)
- [HTTP Servers](#http-servers)

---

## TypeScript vs Python: Type Systems Compared

**Simple Explanation:** If Python's type hints are like friendly suggestions ("Hey, this should be a string"), TypeScript's types are like strict bouncers at a club ("No string? No entry!"). TypeScript enforces types at compile time, catching bugs before they run.

### Key Differences

| Python | TypeScript | Key Difference |
|--------|------------|----------------|
| Optional type hints | Required types (can be inferred) | TS won't compile with type errors |
| Checked by mypy (optional) | Checked by compiler (mandatory) | Built into the language |
| Duck typing at runtime | Structural typing at compile | Shape matters more than name |
| `Any` type exists | `any` exists but discouraged | TS pushes for type safety |
| Gradual typing | Can be gradual or strict | Configure strictness level |

### Mental Model Shift

**Python:**
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

# This runs fine (type hints ignored at runtime)
greet(123)  # Returns "Hello, 123!"
```

**TypeScript:**
```typescript
function greet(name: string): string {
    return `Hello, ${name}!`;
}

// This won't compile!
greet(123);  // Error: Argument of type 'number' is not assignable to parameter of type 'string'
```

---

## Basic Types and Annotations

**Simple Explanation:** TypeScript types are like labels on boxes - they tell you exactly what can go inside. No more "I wonder if this variable is a string or a number" at 3 AM!

### Primitive Types

```typescript
// Basic types
let name: string = "Alice";
let age: number = 30;
let isActive: boolean = true;
let nothing: null = null;
let notDefined: undefined = undefined;

// Type inference (TS figures it out)
let inferredString = "Hello";  // Type: string
let inferredNumber = 42;       // Type: number

// Arrays
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ["a", "b", "c"];  // Generic syntax

// Tuples (fixed-length arrays with known types)
let person: [string, number] = ["Alice", 30];
// person[0] is string, person[1] is number

// Python equivalent:
// from typing import Tuple
// person: Tuple[str, int] = ("Alice", 30)
```

### Object Types

```typescript
// Object type annotation
let user: {
    name: string;
    age: number;
    email?: string;  // Optional property
} = {
    name: "Alice",
    age: 30
    // email is optional, so we can omit it
};

// Better: Use interface or type alias (see next section)
```

### Special Types

```typescript
// any: Escape hatch (avoid when possible!)
let anything: any = 42;
anything = "now I'm a string";
anything = { weird: true };

// unknown: Safe any (must check before using)
let mystery: unknown = getData();
if (typeof mystery === 'string') {
    console.log(mystery.toUpperCase());  // OK after check
}

// void: No return value (like Python's None return)
function logMessage(msg: string): void {
    console.log(msg);
    // implicitly returns undefined
}

// never: Function never returns (throws or infinite loop)
function fail(msg: string): never {
    throw new Error(msg);
}
```

---

## Interfaces and Type Aliases

**Simple Explanation:** Interfaces are like contracts or blueprints. They say "If you want to be a User, you must have these properties." Type aliases are like nicknames for types.

### Interfaces (Object Shapes)

```typescript
// Define the shape of a user
interface User {
    id: number;
    name: string;
    email: string;
    age?: number;  // Optional
    readonly createdAt: Date;  // Can't be modified
}

// Use the interface
const user: User = {
    id: 1,
    name: "Alice",
    email: "alice@example.com",
    createdAt: new Date()
};

// user.createdAt = new Date();  // Error! readonly

// Extending interfaces (like inheritance)
interface Admin extends User {
    permissions: string[];
}

// Python equivalent:
// from typing import Protocol, Optional
// class User(Protocol):
//     id: int
//     name: str
//     email: str
//     age: Optional[int]
//     created_at: datetime
```

### Type Aliases

```typescript
// Type alias for primitives
type ID = string | number;  // Union type
type Age = number;

// Type alias for objects
type Point = {
    x: number;
    y: number;
};

// Type alias for functions
type GreetFunction = (name: string) => string;

const greet: GreetFunction = (name) => `Hello, ${name}!`;

// Complex type compositions
type Status = "pending" | "approved" | "rejected";  // Literal types
type Response<T> = {
    data: T;
    status: Status;
    timestamp: Date;
};
```

### Interface vs Type Alias

```typescript
// Interfaces can be extended and merged
interface Animal {
    name: string;
}

interface Animal {
    age: number;  // Merged with above
}

// Type aliases can't be merged but can do more
type StringOrNumber = string | number;  // Can't do this with interface
type Tuple = [string, number];  // Can't do this with interface
```

---

## Classes and OOP

**Simple Explanation:** TypeScript classes are like Python classes with strict type checking. You get all the OOP goodness but with compile-time safety.

### Basic Classes

**Python:**
```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self._id = generate_id()  # "private"
    
    def greet(self) -> str:
        return f"Hello, I'm {self.name}"
```

**TypeScript:**
```typescript
class User {
    name: string;
    email: string;
    private _id: string;  // Actually private!
    
    constructor(name: string, email: string) {
        this.name = name;
        this.email = email;
        this._id = generateId();
    }
    
    greet(): string {
        return `Hello, I'm ${this.name}`;
    }
}

// Shorthand constructor
class UserShort {
    private _id = generateId();
    
    constructor(
        public name: string,    // Creates this.name
        public email: string,   // Creates this.email
        private age?: number    // Creates private this.age
    ) {}
}
```

### Inheritance and Abstract Classes

```typescript
abstract class Animal {
    constructor(public name: string) {}
    
    abstract makeSound(): string;  // Must be implemented
    
    move(): void {
        console.log(`${this.name} is moving`);
    }
}

class Dog extends Animal {
    constructor(name: string, public breed: string) {
        super(name);
    }
    
    makeSound(): string {
        return "Woof!";
    }
    
    // Override parent method
    move(): void {
        console.log(`${this.name} is running`);
    }
}
```

### Access Modifiers

```typescript
class BankAccount {
    private _balance: number = 0;
    protected accountNumber: string;  // Accessible in subclasses
    public owner: string;  // Default, accessible everywhere
    
    get balance(): number {  // Getter
        return this._balance;
    }
    
    set balance(value: number) {  // Setter
        if (value < 0) throw new Error("Balance cannot be negative");
        this._balance = value;
    }
}
```

---

## Functions and Generics

**Simple Explanation:** Generics are like function templates - "I don't care what type you give me, I'll work with it!" Think of them as type variables that make your code reusable.

### Function Types

```typescript
// Function type annotations
function add(a: number, b: number): number {
    return a + b;
}

// Arrow function
const multiply = (a: number, b: number): number => a * b;

// Optional and default parameters
function greet(name: string, greeting: string = "Hello"): string {
    return `${greeting}, ${name}!`;
}

// Rest parameters
function sum(...numbers: number[]): number {
    return numbers.reduce((a, b) => a + b, 0);
}

// Function overloading (multiple signatures)
function parse(value: string): number;
function parse(value: number): string;
function parse(value: string | number): string | number {
    if (typeof value === 'string') {
        return parseInt(value);
    }
    return value.toString();
}
```

### Generics Basics

```typescript
// Generic function (like Python's TypeVar)
function identity<T>(value: T): T {
    return value;
}

// Usage
const num = identity<number>(42);     // Explicit
const str = identity("hello");        // Inferred

// Generic with constraints
function getLength<T extends { length: number }>(obj: T): number {
    return obj.length;
}

getLength("hello");     // OK: string has length
getLength([1, 2, 3]);   // OK: array has length
// getLength(123);      // Error: number has no length

// Python equivalent:
// from typing import TypeVar
// T = TypeVar('T')
// def identity(value: T) -> T:
//     return value
```

### Generic Classes and Interfaces

```typescript
// Generic class
class Box<T> {
    constructor(private value: T) {}
    
    getValue(): T {
        return this.value;
    }
    
    map<U>(fn: (value: T) => U): Box<U> {
        return new Box(fn(this.value));
    }
}

const numberBox = new Box(42);
const stringBox = numberBox.map(n => n.toString());

// Generic interface
interface Repository<T> {
    findById(id: string): Promise<T | null>;
    save(item: T): Promise<T>;
    delete(id: string): Promise<boolean>;
}

class UserRepository implements Repository<User> {
    async findById(id: string): Promise<User | null> {
        // Implementation
        return null;
    }
    
    async save(user: User): Promise<User> {
        // Implementation
        return user;
    }
    
    async delete(id: string): Promise<boolean> {
        // Implementation
        return true;
    }
}
```

---

## Union and Intersection Types

**Simple Explanation:** Union types are like "or" statements (this OR that), while intersection types are like "and" statements (this AND that). They let you compose types in powerful ways.

### Union Types

```typescript
// Can be one type OR another
type StringOrNumber = string | number;

function processValue(value: StringOrNumber): void {
    if (typeof value === 'string') {
        console.log(value.toUpperCase());
    } else {
        console.log(value.toFixed(2));
    }
}

// Discriminated unions (tagged unions)
type Success = {
    status: 'success';
    data: any;
};

type Error = {
    status: 'error';
    message: string;
};

type Result = Success | Error;

function handleResult(result: Result) {
    if (result.status === 'success') {
        console.log(result.data);  // TS knows this is Success
    } else {
        console.log(result.message);  // TS knows this is Error
    }
}

// Python equivalent (Python 3.10+):
// Result = Success | Error
```

### Intersection Types

```typescript
// Combines multiple types (has ALL properties)
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged;  // Has both name AND age

const person: Person = {
    name: "Alice",
    age: 30
};

// Mixing interfaces
interface Timestamped {
    createdAt: Date;
    updatedAt: Date;
}

interface User {
    id: string;
    email: string;
}

type TimestampedUser = User & Timestamped;
```

---

## Type Guards and Narrowing

**Simple Explanation:** Type guards are like security checkpoints that verify what type something is. Once verified, TypeScript knows exactly what you're working with.

### Built-in Type Guards

```typescript
function processValue(value: string | number | boolean) {
    if (typeof value === 'string') {
        // TS knows value is string here
        return value.toUpperCase();
    } else if (typeof value === 'number') {
        // TS knows value is number here
        return value.toFixed(2);
    } else {
        // TS knows value is boolean here
        return value ? 'yes' : 'no';
    }
}

// instanceof for classes
class Cat {
    meow() { return "Meow!"; }
}

class Dog {
    bark() { return "Woof!"; }
}

function makeNoise(animal: Cat | Dog) {
    if (animal instanceof Cat) {
        return animal.meow();
    } else {
        return animal.bark();
    }
}
```

### Custom Type Guards

```typescript
// Type predicate functions
interface Bird {
    fly(): void;
    layEggs(): void;
}

interface Fish {
    swim(): void;
    layEggs(): void;
}

// Custom type guard
function isBird(pet: Bird | Fish): pet is Bird {
    return (pet as Bird).fly !== undefined;
}

function movePet(pet: Bird | Fish) {
    if (isBird(pet)) {
        pet.fly();  // TS knows pet is Bird
    } else {
        pet.swim();  // TS knows pet is Fish
    }
}
```

---

## Utility Types

**Simple Explanation:** Utility types are like pre-built Lego pieces - TypeScript gives you these handy type transformers to modify existing types without rewriting them.

### Common Utility Types

```typescript
interface User {
    id: string;
    name: string;
    email: string;
    age: number;
}

// Partial: Makes all properties optional
type PartialUser = Partial<User>;
// Same as: { id?: string; name?: string; email?: string; age?: number; }

// Required: Makes all properties required
type RequiredUser = Required<PartialUser>;

// Readonly: Makes all properties readonly
type ReadonlyUser = Readonly<User>;

// Pick: Select specific properties
type UserPreview = Pick<User, 'id' | 'name'>;
// Same as: { id: string; name: string; }

// Omit: Exclude specific properties
type UserWithoutAge = Omit<User, 'age'>;
// Same as: { id: string; name: string; email: string; }

// Record: Create object type with specific keys
type UserRoles = Record<string, User>;
// Same as: { [key: string]: User }

// Extract and Exclude for unions
type Status = 'pending' | 'approved' | 'rejected' | 'deleted';
type ActiveStatus = Exclude<Status, 'deleted'>;  // 'pending' | 'approved' | 'rejected'
type InactiveStatus = Extract<Status, 'deleted' | 'rejected'>;  // 'deleted' | 'rejected'
```

### Advanced Utility Types

```typescript
// ReturnType: Get function return type
function getData() {
    return { id: 1, name: "Alice" };
}
type Data = ReturnType<typeof getData>;  // { id: number; name: string; }

// Parameters: Get function parameters as tuple
type AddParams = Parameters<typeof add>;  // [number, number]

// Awaited: Unwrap Promise type
type PromiseString = Promise<string>;
type StringType = Awaited<PromiseString>;  // string
```

---

## Why Deno? (Node.js Done Right)

**Simple Explanation:** If Node.js is like Python 2, Deno is like Python 3 - it learned from all the mistakes and built something better from the ground up. Created by the same person who made Node.js, Ryan Dahl.

### Key Improvements Over Node.js

| Node.js Problems | Deno Solutions |
|------------------|----------------|
| Insecure by default | Secure by default (permissions) |
| npm/node_modules mess | URL imports, no node_modules |
| No built-in TypeScript | First-class TypeScript support |
| Callback-based APIs | Promise-based APIs |
| require() (CommonJS) | ES modules only |
| package.json complexity | Single deno.json config |
| Separate tools | Built-in formatter, linter, tester |

### Philosophy Differences

```typescript
// Node.js way
const fs = require('fs');
const data = fs.readFileSync('file.txt', 'utf8');

// Deno way
const data = await Deno.readTextFile('file.txt');
// Note: Needs --allow-read permission!
```

---

## Security First

**Simple Explanation:** Deno is like a smartphone app - it asks for permissions before accessing your files, network, or system. No more "npm install" giving random packages full access to everything!

### Permission System

```bash
# No permissions (safe sandbox)
deno run script.ts

# Read files
deno run --allow-read script.ts
deno run --allow-read=/specific/path script.ts

# Network access
deno run --allow-net script.ts
deno run --allow-net=api.example.com script.ts

# Environment variables
deno run --allow-env script.ts

# All permissions (like Node.js)
deno run -A script.ts  # or --allow-all
```

### Permission Examples

```typescript
// This needs --allow-read
const data = await Deno.readTextFile("config.json");

// This needs --allow-net
const response = await fetch("https://api.example.com/data");

// This needs --allow-write
await Deno.writeTextFile("output.txt", "Hello");

// This needs --allow-env
const apiKey = Deno.env.get("API_KEY");

// Check permissions programmatically
const status = await Deno.permissions.query({ name: "read", path: "/home" });
if (status.state === "granted") {
    // Safe to read
}
```

---

## Built-in Tooling

**Simple Explanation:** Deno is like a Swiss Army knife - everything you need is built-in. No more installing eslint, prettier, jest, typescript, etc. separately!

### All-in-One CLI

```bash
# Format code (like prettier)
deno fmt

# Lint code (like eslint)
deno lint

# Type check
deno check script.ts

# Run tests
deno test

# Bundle for browsers
deno bundle script.ts output.js

# Compile to executable
deno compile script.ts

# Generate documentation
deno doc script.ts

# Benchmark performance
deno bench

# Start REPL
deno repl

# Upgrade Deno
deno upgrade
```

### Configuration (deno.json)

```json
{
  "tasks": {
    "dev": "deno run --watch --allow-net server.ts",
    "test": "deno test --allow-read",
    "build": "deno compile --output=app server.ts"
  },
  "imports": {
    "@std/": "https://deno.land/std@0.208.0/",
    "oak": "https://deno.land/x/oak@v12.6.1/mod.ts"
  },
  "fmt": {
    "options": {
      "lineWidth": 100,
      "indentWidth": 2
    }
  },
  "lint": {
    "rules": {
      "tags": ["recommended"]
    }
  }
}
```

---

## URL Imports

**Simple Explanation:** Instead of npm installing packages into node_modules, Deno imports directly from URLs like a web browser. Packages are cached locally, versioned by URL.

### Basic URL Imports

```typescript
// Import from Deno standard library
import { serve } from "https://deno.land/std@0.208.0/http/server.ts";

// Import from third-party modules
import { Application } from "https://deno.land/x/oak@v12.6.1/mod.ts";

// Import from any URL
import { utils } from "https://raw.githubusercontent.com/user/repo/main/utils.ts";

// Import JSON
import config from "./config.json" with { type: "json" };
```

### Import Maps

```json
// deno.json
{
  "imports": {
    "@std/": "https://deno.land/std@0.208.0/",
    "oak": "https://deno.land/x/oak@v12.6.1/mod.ts",
    "@utils/": "./src/utils/"
  }
}
```

```typescript
// Now you can use mapped imports
import { serve } from "@std/http/server.ts";
import { Application } from "oak";
import { helpers } from "@utils/helpers.ts";
```

---

## Standard Library

**Simple Explanation:** Deno's standard library is like Python's - batteries included! High-quality, reviewed modules for common tasks.

### Common Modules

```typescript
// File system
import { ensureDir, exists, walk } from "@std/fs/mod.ts";

await ensureDir("./logs");
if (await exists("config.json")) {
    // File exists
}

// Path manipulation
import { join, dirname, basename } from "@std/path/mod.ts";

const fullPath = join("src", "utils", "helpers.ts");

// HTTP server
import { serve } from "@std/http/server.ts";

serve((req) => new Response("Hello!"), { port: 8000 });

// Testing assertions
import { assertEquals, assertThrows } from "@std/assert/mod.ts";

Deno.test("math works", () => {
    assertEquals(2 + 2, 4);
});

// Datetime
import { format } from "@std/datetime/mod.ts";

const formatted = format(new Date(), "yyyy-MM-dd");

// Crypto
import { crypto } from "@std/crypto/mod.ts";

const hash = await crypto.subtle.digest("SHA-256", data);
```

---

## Web APIs Everywhere

**Simple Explanation:** Deno uses the same APIs as web browsers wherever possible. If you know how to fetch() in the browser, you know how to fetch() in Deno!

### Browser-Compatible APIs

```typescript
// Fetch API (no node-fetch needed!)
const response = await fetch("https://api.example.com/data");
const data = await response.json();

// Web Crypto API
const encoder = new TextEncoder();
const data = encoder.encode("Hello, World!");
const hash = await crypto.subtle.digest("SHA-256", data);

// FormData
const form = new FormData();
form.append("name", "Alice");
form.append("file", new File(["content"], "test.txt"));

// URLSearchParams
const params = new URLSearchParams({ q: "deno", limit: "10" });
const url = `https://api.example.com/search?${params}`;

// setTimeout/setInterval (no more confusing Node timers)
setTimeout(() => console.log("Later!"), 1000);

// Web Storage API (localStorage)
localStorage.setItem("key", "value");
const value = localStorage.getItem("key");

// WebSocket
const ws = new WebSocket("ws://localhost:8080");
ws.onmessage = (event) => console.log(event.data);
```

---

## ES Modules Only

**Simple Explanation:** Deno only uses ES modules (import/export) - the modern standard. No more require(), module.exports, or wondering which module system to use!

### Module Syntax

```typescript
// Named exports
export function add(a: number, b: number): number {
    return a + b;
}

export const PI = 3.14159;

export class Calculator {
    // ...
}

// Default export
export default function main() {
    console.log("Main function");
}

// Re-exports
export { add, subtract } from "./math.ts";
export * from "./utils.ts";

// Type exports
export type { User, Admin } from "./types.ts";

// Importing
import main, { add, PI, Calculator } from "./module.ts";
import * as math from "./math.ts";
import type { User } from "./types.ts";
```

### Module Resolution

```typescript
// Relative imports (must include extension!)
import { helper } from "./utils.ts";  // ✓ Good
// import { helper } from "./utils";   // ✗ Bad - no extension

// Absolute imports (URLs)
import { serve } from "https://deno.land/std/http/server.ts";

// Import assertions for non-JS
import data from "./data.json" with { type: "json" };
import styles from "./styles.css" with { type: "text" };
```

---

## Import Maps

**Simple Explanation:** Import maps are like phone books for your code - they let you use short, memorable names instead of long URLs. Think of them as shortcuts for your imports.

### Basic Import Maps

```json
// deno.json
{
  "imports": {
    "std/": "https://deno.land/std@0.208.0/",
    "oak": "https://deno.land/x/oak@v12.6.1/mod.ts",
    "react": "https://esm.sh/react@18.2.0",
    "utils/": "./src/utils/"
  }
}
```

```typescript
// Before import maps (verbose)
import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
import { Application } from "https://deno.land/x/oak@v12.6.1/mod.ts";

// After import maps (clean)
import { serve } from "std/http/server.ts";
import { Application } from "oak";
```

---

## Dependency Management

**Simple Explanation:** Deno's dependency management is refreshingly simple - no package.json nightmares, no node_modules black holes. Dependencies are just URLs, and Deno handles the rest.

### How Dependencies Work

```typescript
// deps.ts - Centralize your dependencies
export { serve } from "https://deno.land/std@0.208.0/http/server.ts";
export { Application, Router } from "https://deno.land/x/oak@v12.6.1/mod.ts";
export { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";

// main.ts - Import from your deps file
import { serve, Application } from "./deps.ts";
```

### Dependency Commands

```bash
# Cache dependencies
deno cache deps.ts

# See dependency info
deno info https://deno.land/x/oak/mod.ts

# Update dependencies (edit URLs in deps.ts)
# No special command needed - just change the version!
```

---

## Promises and Async/Await

**Simple Explanation:** JavaScript's async/await is like Python's, but Promises are the foundation. Think of Promises as "IOUs" for future values.

### Promise Basics

```typescript
// Creating promises
const promise = new Promise<string>((resolve, reject) => {
    setTimeout(() => {
        resolve("Success!");
        // or reject(new Error("Failed!"));
    }, 1000);
});

// Using promises
promise
    .then(result => console.log(result))
    .catch(error => console.error(error))
    .finally(() => console.log("Done"));

// Python equivalent:
// import asyncio
// future = asyncio.Future()
// future.set_result("Success!")
```

### Async/Await

```typescript
// Async functions return promises
async function fetchData(): Promise<Data> {
    const response = await fetch("/api/data");
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
}

// Error handling
async function safelyFetchData(): Promise<Data | null> {
    try {
        return await fetchData();
    } catch (error) {
        console.error("Failed to fetch:", error);
        return null;
    }
}

// Parallel execution
async function fetchMultiple() {
    // Sequential (slow)
    const user = await fetchUser();
    const posts = await fetchPosts();
    
    // Parallel (fast)
    const [user, posts] = await Promise.all([
        fetchUser(),
        fetchPosts()
    ]);
    
    // Race condition
    const fastest = await Promise.race([
        fetchFromServer1(),
        fetchFromServer2()
    ]);
}
```

---

## Top-Level Await

**Simple Explanation:** In Deno, you can use await at the top level of your files, no wrapper function needed! It's like Python's synchronous code but with async superpowers.

### No More Wrapper Functions

```typescript
// Node.js way (old)
async function main() {
    const data = await fetch("/api/data");
    console.log(data);
}
main();

// Deno way (clean!)
const data = await fetch("/api/data");
console.log(data);

// Real example
const config = await Deno.readTextFile("config.json");
const settings = JSON.parse(config);

// Dynamic imports
const module = await import("./module.ts");
```

---

## Testing with Deno

**Simple Explanation:** Deno's testing is built-in and uses a similar style to Python's pytest - descriptive test names, simple assertions, and great output.

### Basic Testing

```typescript
// math_test.ts
import { assertEquals, assertThrows } from "@std/assert/mod.ts";
import { add, divide } from "./math.ts";

Deno.test("add() returns sum of two numbers", () => {
    assertEquals(add(2, 3), 5);
    assertEquals(add(-1, 1), 0);
});

Deno.test("divide() handles division by zero", () => {
    assertThrows(
        () => divide(10, 0),
        Error,
        "Division by zero"
    );
});

// Async tests
Deno.test("fetches user data", async () => {
    const user = await fetchUser(1);
    assertEquals(user.name, "Alice");
});

// Test steps (like subtests)
Deno.test("user operations", async (t) => {
    await t.step("create user", async () => {
        const user = await createUser({ name: "Bob" });
        assertEquals(user.name, "Bob");
    });
    
    await t.step("update user", async () => {
        const updated = await updateUser(1, { name: "Bobby" });
        assertEquals(updated.name, "Bobby");
    });
});
```

### Running Tests

```bash
# Run all tests
deno test

# Run specific file
deno test math_test.ts

# Run with permissions
deno test --allow-read --allow-net

# Watch mode
deno test --watch

# Coverage
deno test --coverage=cov
deno coverage cov
```

---

## HTTP Servers

**Simple Explanation:** Building HTTP servers in Deno is like using Python's built-in http.server but with modern async/await and the Fetch API you already know from browsers.

### Basic Server

```typescript
// Using Deno.serve (recommended)
Deno.serve({ port: 8000 }, (request) => {
    const url = new URL(request.url);
    
    if (url.pathname === "/") {
        return new Response("Hello, Deno!");
    }
    
    if (url.pathname === "/json") {
        return Response.json({ message: "Hello, JSON!" });
    }
    
    return new Response("Not Found", { status: 404 });
});

// With routing
const routes = new Map([
    ["GET /users", handleGetUsers],
    ["POST /users", handleCreateUser],
    ["GET /users/:id", handleGetUser],
]);

Deno.serve(async (request) => {
    const method = request.method;
    const url = new URL(request.url);
    const key = `${method} ${url.pathname}`;
    
    const handler = routes.get(key);
    if (handler) {
        return await handler(request);
    }
    
    return new Response("Not Found", { status: 404 });
});
```

### Using Oak Framework

```typescript
// Oak is like Express for Deno
import { Application, Router } from "oak";

const app = new Application();
const router = new Router();

// Middleware
app.use(async (ctx, next) => {
    console.log(`${ctx.request.method} ${ctx.request.url}`);
    await next();
});

// Routes
router
    .get("/", (ctx) => {
        ctx.response.body = "Hello, Oak!";
    })
    .get("/users", async (ctx) => {
        ctx.response.body = await getUsers();
    })
    .post("/users", async (ctx) => {
        const body = await ctx.request.body().value;
        const user = await createUser(body);
        ctx.response.body = user;
    });

app.use(router.routes());
app.use(router.allowedMethods());

await app.listen({ port: 8000 });
```

---

## Final Thoughts

TypeScript with Deno combines the best of both worlds: 
- **Type safety** catches bugs before runtime
- **Modern JavaScript** features make coding enjoyable
- **Security by default** keeps your system safe
- **Built-in tooling** eliminates setup complexity
- **Web standards** mean less to learn

Coming from Python, you'll appreciate:
- The familiar async/await patterns
- Built-in testing that just works
- Type hints that actually enforce safety
- A standard library you can trust
- No more dependency hell

**Remember:**
- Start with strict TypeScript settings
- Use the built-in tools before reaching for external ones
- Leverage web standards APIs
- Keep your permissions minimal
- When in doubt, check the Deno manual

> "Simplicity is the ultimate sophistication." - Leonardo da Vinci

Welcome to the world of TypeScript and Deno - where JavaScript finally makes sense! 🦕✨