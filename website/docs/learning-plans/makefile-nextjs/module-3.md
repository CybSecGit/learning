# Module 3: Next.js Foundations - React, But Make It Fast
## Week 3: Where We Learn Why Everyone's Migrating from Create React App

> "Next.js is what happens when React developers realize that maybe, just maybe, sending 400KB of JavaScript to render a header wasn't the best idea."

## 🎯 Module Objectives

By the end of this module, you will:
- Understand Next.js architecture and why it exists
- Master the App Router (the new way that's actually good)
- Know when to use Server vs Client Components (and why it matters)
- Implement data fetching patterns that don't make users sad
- Build layouts that are both beautiful and performant

## 📚 Part 1: The Next.js Origin Story

### Why Next.js? A Brief History of React's Growing Pains

React gave us components. Create React App gave us a starting point. But then we discovered:
- SEO was impossible (search engines don't run JavaScript)
- Initial load times were abysmal (blank white screen of patience)
- Routing required a PhD in React Router
- Code splitting was manual and painful
- Image optimization was "thoughts and prayers"

Enter Next.js: "What if we made React good by default?"

### The Fundamental Shift: From SPA to Hybrid

```jsx
// The old way (Create React App)
// Everything runs on the client
function App() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(setData);  // SEO: "What data?"
  }, []);
  
  return <div>{data?.content}</div>;
}

// The Next.js way (App Router)
// This runs on the server!
async function Page() {
  const data = await fetch('https://api.example.com/data').then(r => r.json());
  
  return <div>{data.content}</div>;  // SEO: "I can see everything!"
}
```

## 🏗️ Part 2: Next.js App Router Architecture

### Project Structure That Makes Sense

```bash
my-nextjs-app/
├── app/                    # App Router (the new hotness)
│   ├── layout.tsx         # Root layout (wraps everything)
│   ├── page.tsx           # Home page (/)
│   ├── global.css         # Global styles
│   ├── api/               # API routes
│   │   └── hello/
│   │       └── route.ts   # /api/hello endpoint
│   ├── blog/              # /blog route
│   │   ├── page.tsx       # Blog listing
│   │   ├── [slug]/        # Dynamic routes
│   │   │   └── page.tsx   # Individual blog post
│   │   └── layout.tsx     # Blog-specific layout
│   └── (marketing)/       # Route groups (organizational)
│       ├── about/
│       └── contact/
├── components/            # Shared components
├── lib/                   # Utility functions
├── public/               # Static assets
└── next.config.js        # Next.js configuration
```

### Creating Your First Next.js App

```bash
# Create with our trusty Makefile
cat > Makefile << 'EOF'
# Next.js Project Makefile
.PHONY: create
create: ## Create new Next.js app
	@read -p "Project name: " name; \
	pnpx create-next-app@latest $$name \
		--typescript \
		--tailwind \
		--app \
		--src-dir=false \
		--import-alias="@/*"

.PHONY: dev
dev: ## Start development server
	pnpm dev

.PHONY: build
build: ## Build for production
	pnpm build

.PHONY: analyze
analyze: ## Analyze bundle size
	ANALYZE=true pnpm build
EOF

make create
```

### The Layout System: Composition at Its Finest

```tsx
// app/layout.tsx - The root layout
import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'My App',
  description: 'Built with Next.js and tears of joy',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav>
          {/* This nav appears on every page */}
        </nav>
        {children}
      </body>
    </html>
  );
}
```

## 🎭 Part 3: Server Components vs Client Components

### The Great Divide: When JavaScript Runs

```tsx
// Server Component (default)
// ✅ Runs on server
// ✅ Can fetch data directly
// ✅ Zero JavaScript sent to client
// ❌ No useState, useEffect, onClick
async function ServerComponent() {
  const data = await db.query('SELECT * FROM products');
  
  return (
    <div>
      {data.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  );
}

// Client Component (opt-in with 'use client')
// ✅ Runs in browser
// ✅ Can use hooks and browser APIs
// ❌ Increases bundle size
// ❌ No direct database access
'use client';

import { useState } from 'react';

function ClientComponent() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### The Mental Model: Think Like Next.js

```tsx
// app/products/page.tsx
// This is a Server Component that fetches data
async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    cache: 'no-store', // Dynamic data
  }).then(r => r.json());
  
  return (
    <div>
      <h1>Products</h1>
      <ProductList products={products} />
      <AddToCartButton />  {/* This needs to be a Client Component */}
    </div>
  );
}

// components/ProductList.tsx
// Server Component - just displays data
function ProductList({ products }: { products: Product[] }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

// components/AddToCartButton.tsx
// Client Component - needs interactivity
'use client';

import { useState } from 'react';

function AddToCartButton({ productId }: { productId: string }) {
  const [isAdding, setIsAdding] = useState(false);
  
  const handleAddToCart = async () => {
    setIsAdding(true);
    await fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify({ productId }),
    });
    setIsAdding(false);
  };
  
  return (
    <button onClick={handleAddToCart} disabled={isAdding}>
      {isAdding ? 'Adding...' : 'Add to Cart'}
    </button>
  );
}
```

## 🚀 Part 4: Data Fetching Patterns

### The Four Ways to Fetch Data

```tsx
// 1. Static Data (fetch at build time)
async function StaticPage() {
  const data = await fetch('https://api.example.com/static-data', {
    cache: 'force-cache', // Default behavior
  }).then(r => r.json());
  
  return <div>{data.content}</div>;
}

// 2. Dynamic Data (fetch on each request)
async function DynamicPage() {
  const data = await fetch('https://api.example.com/live-data', {
    cache: 'no-store',
  }).then(r => r.json());
  
  return <div>{data.content}</div>;
}

// 3. Revalidated Data (best of both worlds)
async function RevalidatedPage() {
  const data = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 }, // Revalidate every hour
  }).then(r => r.json());
  
  return <div>{data.content}</div>;
}

// 4. Client-side Fetching (when you need real-time)
'use client';

import useSWR from 'swr';

function ClientFetchComponent() {
  const { data, error, isLoading } = useSWR(
    '/api/user',
    url => fetch(url).then(r => r.json())
  );
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading data</div>;
  
  return <div>{data.name}</div>;
}
```

### Parallel Data Fetching: Speed Matters

```tsx
// ❌ Sequential fetching (slow)
async function SlowPage() {
  const user = await fetchUser();
  const posts = await fetchPosts(user.id);
  const comments = await fetchComments(posts[0].id);
  
  return <div>...</div>;
}

// ✅ Parallel fetching (fast)
async function FastPage() {
  const [user, posts, recommendations] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchRecommendations(),
  ]);
  
  return <div>...</div>;
}

// ✅ Even better: Streaming with Suspense
import { Suspense } from 'react';

function StreamingPage() {
  return (
    <div>
      <Suspense fallback={<UserSkeleton />}>
        <UserProfile />
      </Suspense>
      
      <Suspense fallback={<PostsSkeleton />}>
        <UserPosts />
      </Suspense>
    </div>
  );
}
```

## 🎨 Part 5: Routing and Navigation

### File-based Routing: Folders Are Routes

```tsx
// app/blog/[slug]/page.tsx
interface Props {
  params: { slug: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export async function generateStaticParams() {
  const posts = await fetchAllPosts();
  
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export async function generateMetadata({ params }: Props) {
  const post = await fetchPost(params.slug);
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      images: [post.image],
    },
  };
}

export default async function BlogPost({ params }: Props) {
  const post = await fetchPost(params.slug);
  
  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}
```

### Navigation: The Right Way

```tsx
// components/Navigation.tsx
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function Navigation() {
  const pathname = usePathname();
  
  return (
    <nav>
      <Link 
        href="/"
        className={pathname === '/' ? 'active' : ''}
      >
        Home
      </Link>
      
      <Link 
        href="/blog"
        className={pathname.startsWith('/blog') ? 'active' : ''}
        prefetch={false}  // Only prefetch on hover
      >
        Blog
      </Link>
    </nav>
  );
}

// Programmatic navigation
'use client';

import { useRouter } from 'next/navigation';

function SearchForm() {
  const router = useRouter();
  
  const handleSearch = (e: FormEvent) => {
    e.preventDefault();
    const query = new FormData(e.target).get('q');
    router.push(`/search?q=${query}`);
  };
  
  return (
    <form onSubmit={handleSearch}>
      <input name="q" placeholder="Search..." />
    </form>
  );
}
```

## 🛠️ Part 6: API Routes and Backend

### API Routes: Your Backend in the Same Repo

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

// GET /api/posts
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('query');
  
  const posts = await db.posts.findMany({
    where: query ? { title: { contains: query } } : {},
  });
  
  return NextResponse.json(posts);
}

// POST /api/posts
export async function POST(request: NextRequest) {
  const body = await request.json();
  
  // Validate
  if (!body.title) {
    return NextResponse.json(
      { error: 'Title is required' },
      { status: 400 }
    );
  }
  
  const post = await db.posts.create({
    data: body,
  });
  
  return NextResponse.json(post, { status: 201 });
}

// app/api/posts/[id]/route.ts
interface Props {
  params: { id: string };
}

// GET /api/posts/:id
export async function GET(request: NextRequest, { params }: Props) {
  const post = await db.posts.findUnique({
    where: { id: params.id },
  });
  
  if (!post) {
    return NextResponse.json(
      { error: 'Post not found' },
      { status: 404 }
    );
  }
  
  return NextResponse.json(post);
}

// PATCH /api/posts/:id
export async function PATCH(request: NextRequest, { params }: Props) {
  const body = await request.json();
  
  const post = await db.posts.update({
    where: { id: params.id },
    data: body,
  });
  
  return NextResponse.json(post);
}
```

## 🏗️ Module Project: Portfolio Site with CMS

Let's build a real Next.js application with everything we've learned:

```tsx
// Makefile for our project
cat > Makefile << 'EOF'
.PHONY: create-portfolio
create-portfolio:
	pnpx create-next-app@latest portfolio \
		--typescript --tailwind --app
	cd portfolio && \
	pnpm add @prisma/client prisma \
		@tailwindcss/typography \
		react-markdown gray-matter

.PHONY: setup-db
setup-db:
	cd portfolio && \
	pnpx prisma init --datasource-provider sqlite && \
	pnpx prisma migrate dev --name init

.PHONY: dev
dev:
	cd portfolio && pnpm dev

.PHONY: studio
studio:
	cd portfolio && pnpx prisma studio
EOF
```

### The Complete App Structure

```typescript
// prisma/schema.prisma
model Post {
  id        String   @id @default(cuid())
  title     String
  slug      String   @unique
  excerpt   String
  content   String
  published Boolean  @default(false)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

// app/page.tsx - Home page
import { Posts } from '@/components/Posts';

export default async function HomePage() {
  return (
    <main>
      <section className="hero">
        <h1>Welcome to My Portfolio</h1>
        <p>Full-stack developer specializing in Next.js</p>
      </section>
      
      <section>
        <h2>Recent Posts</h2>
        <Suspense fallback={<PostsSkeleton />}>
          <Posts limit={3} />
        </Suspense>
      </section>
    </main>
  );
}

// components/Posts.tsx
import { prisma } from '@/lib/prisma';
import Link from 'next/link';

export async function Posts({ limit }: { limit?: number }) {
  const posts = await prisma.post.findMany({
    where: { published: true },
    orderBy: { createdAt: 'desc' },
    take: limit,
  });
  
  return (
    <div className="grid gap-4">
      {posts.map(post => (
        <article key={post.id}>
          <Link href={`/blog/${post.slug}`}>
            <h3>{post.title}</h3>
            <p>{post.excerpt}</p>
            <time>{post.createdAt.toLocaleDateString()}</time>
          </Link>
        </article>
      ))}
    </div>
  );
}
```

## 🧪 Hands-On Exercises

### Exercise 1: Blog with Categories
Extend the portfolio to include:
- Categories for posts
- Category pages with filtering
- Related posts suggestions
- RSS feed generation

### Exercise 2: Authentication Flow
Add user authentication:
- Login/Register pages
- Protected admin routes
- Session management
- Role-based access

### Exercise 3: Performance Optimization
Optimize the site for Core Web Vitals:
- Implement image optimization
- Add loading states
- Optimize fonts
- Measure and improve metrics

## ✅ Module Completion Checklist

Before moving to Module 4, ensure you can:

- [ ] Create Next.js apps with the App Router
- [ ] Understand Server vs Client Components
- [ ] Implement various data fetching strategies
- [ ] Create dynamic routes and layouts
- [ ] Build API routes with proper error handling
- [ ] Navigate programmatically and with Link
- [ ] Structure projects for maintainability

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [App Router Playground](https://app-router.vercel.app/)
- [Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples)

## 🎯 Next Steps

You've mastered Next.js fundamentals! You can now:
- Build fast, SEO-friendly web applications
- Choose the right rendering strategy for each use case
- Create full-stack applications in one codebase

**Ready for production patterns?** Continue to [Module 4: Building Production Next.js Applications](/learning-plans/makefile-nextjs/module-4)

---

*Remember: Next.js is like a Swiss Army knife - incredibly useful, but you don't need to use every tool for every job. Start simple, add complexity as needed.*