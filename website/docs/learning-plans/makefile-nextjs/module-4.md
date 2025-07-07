# Module 4: Building Production Next.js Applications
## Week 4: From localhost:3000 to Actual Users Breaking Your App

> "Development is when everything works perfectly on your machine. Production is when you discover that your machine was lying to you."

## 🎯 Module Objectives

By the end of this module, you will:
- Implement authentication that doesn't store passwords in localStorage
- Master state management without Redux-induced nightmares
- Build API routes that handle real-world chaos gracefully
- Optimize performance because users have the patience of caffeinated squirrels
- Deploy applications that survive contact with actual humans

## 📚 Part 1: Authentication - Because "Admin/Admin" Isn't Secure

### Modern Authentication with NextAuth.js

```bash
# First, let's set up authentication properly
pnpm add next-auth @auth/prisma-adapter
```

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import { PrismaAdapter } from '@auth/prisma-adapter';
import GithubProvider from 'next-auth/providers/github';
import GoogleProvider from 'next-auth/providers/google';
import CredentialsProvider from 'next-auth/providers/credentials';
import { prisma } from '@/lib/prisma';
import bcrypt from 'bcryptjs';

const handler = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    // OAuth providers (the easy way)
    GithubProvider({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    
    // Email/Password (because some people insist)
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          throw new Error('Invalid credentials');
        }
        
        const user = await prisma.user.findUnique({
          where: { email: credentials.email },
        });
        
        if (!user || !user.password) {
          throw new Error('User not found');
        }
        
        const isValid = await bcrypt.compare(
          credentials.password,
          user.password
        );
        
        if (!isValid) {
          throw new Error('Invalid password');
        }
        
        return {
          id: user.id,
          email: user.email,
          name: user.name,
        };
      },
    }),
  ],
  
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  
  callbacks: {
    async jwt({ token, user, account }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }
      return token;
    },
    
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.role = token.role as string;
      }
      return session;
    },
  },
  
  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
  },
});

export { handler as GET, handler as POST };
```

### Protecting Routes: Server and Client Side

```typescript
// middleware.ts - Protect routes at the edge
import { withAuth } from 'next-auth/middleware';
import { NextResponse } from 'next/server';

export default withAuth(
  function middleware(req) {
    const token = req.nextauth.token;
    const isAdmin = token?.role === 'admin';
    const isAdminRoute = req.nextUrl.pathname.startsWith('/admin');
    
    if (isAdminRoute && !isAdmin) {
      return NextResponse.redirect(new URL('/denied', req.url));
    }
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token,
    },
  }
);

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*', '/api/protected/:path*'],
};

// app/dashboard/page.tsx - Server-side protection
import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';
import { authOptions } from '@/app/api/auth/[...nextauth]/route';

export default async function DashboardPage() {
  const session = await getServerSession(authOptions);
  
  if (!session) {
    redirect('/auth/signin');
  }
  
  return (
    <div>
      <h1>Welcome, {session.user?.name}!</h1>
      {/* Dashboard content */}
    </div>
  );
}

// components/ClientProtected.tsx - Client-side protection
'use client';

import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export function ClientProtected({ children }: { children: React.ReactNode }) {
  const { data: session, status } = useSession();
  const router = useRouter();
  
  useEffect(() => {
    if (status === 'loading') return;
    if (!session) router.push('/auth/signin');
  }, [session, status, router]);
  
  if (status === 'loading') {
    return <div>Loading...</div>;
  }
  
  if (!session) {
    return null;
  }
  
  return <>{children}</>;
}
```

## 🎨 Part 2: State Management That Doesn't Suck

### Zustand: State Management for Humans

```typescript
// stores/useStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartStore {
  items: CartItem[];
  total: number;
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartStore>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],
        total: 0,
        
        addItem: (item) => set((state) => {
          const existing = state.items.find(i => i.id === item.id);
          
          if (existing) {
            return {
              items: state.items.map(i =>
                i.id === item.id
                  ? { ...i, quantity: i.quantity + 1 }
                  : i
              ),
              total: state.total + item.price,
            };
          }
          
          return {
            items: [...state.items, { ...item, quantity: 1 }],
            total: state.total + item.price,
          };
        }),
        
        removeItem: (id) => set((state) => {
          const item = state.items.find(i => i.id === id);
          if (!item) return state;
          
          return {
            items: state.items.filter(i => i.id !== id),
            total: state.total - (item.price * item.quantity),
          };
        }),
        
        updateQuantity: (id, quantity) => set((state) => {
          if (quantity <= 0) {
            return get().removeItem(id), state;
          }
          
          const item = state.items.find(i => i.id === id);
          if (!item) return state;
          
          const diff = quantity - item.quantity;
          
          return {
            items: state.items.map(i =>
              i.id === id ? { ...i, quantity } : i
            ),
            total: state.total + (item.price * diff),
          };
        }),
        
        clearCart: () => set({ items: [], total: 0 }),
      }),
      {
        name: 'cart-storage',
      }
    )
  )
);

// Using the store in components
'use client';

export function Cart() {
  const { items, total, removeItem } = useCartStore();
  
  return (
    <div>
      {items.map(item => (
        <div key={item.id}>
          <span>{item.name}</span>
          <span>${item.price * item.quantity}</span>
          <button onClick={() => removeItem(item.id)}>Remove</button>
        </div>
      ))}
      <div>Total: ${total.toFixed(2)}</div>
    </div>
  );
}
```

### Server State Management with React Query

```typescript
// lib/api-client.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      gcTime: 5 * 60 * 1000, // 5 minutes
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});

// hooks/useProducts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useProducts(category?: string) {
  return useQuery({
    queryKey: ['products', category],
    queryFn: async () => {
      const params = category ? `?category=${category}` : '';
      const res = await fetch(`/api/products${params}`);
      if (!res.ok) throw new Error('Failed to fetch products');
      return res.json();
    },
  });
}

export function useCreateProduct() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (product: CreateProductDto) => {
      const res = await fetch('/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(product),
      });
      if (!res.ok) throw new Error('Failed to create product');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}

// Using in components
'use client';

export function ProductList() {
  const { data: products, isLoading, error } = useProducts();
  const createProduct = useCreateProduct();
  
  if (isLoading) return <ProductSkeleton />;
  if (error) return <ErrorMessage error={error} />;
  
  return (
    <div>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
      
      <button
        onClick={() => createProduct.mutate({ name: 'New Product' })}
        disabled={createProduct.isPending}
      >
        Add Product
      </button>
    </div>
  );
}
```

## 🚀 Part 3: API Design for the Real World

### Error Handling That Actually Helps

```typescript
// lib/api-utils.ts
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public errors?: any
  ) {
    super(message);
  }
}

export function handleApiError(error: unknown) {
  console.error('API Error:', error);
  
  if (error instanceof ApiError) {
    return NextResponse.json(
      {
        error: error.message,
        errors: error.errors,
      },
      { status: error.statusCode }
    );
  }
  
  if (error instanceof z.ZodError) {
    return NextResponse.json(
      {
        error: 'Validation failed',
        errors: error.errors,
      },
      { status: 400 }
    );
  }
  
  return NextResponse.json(
    { error: 'Internal server error' },
    { status: 500 }
  );
}

// app/api/products/route.ts
import { z } from 'zod';

const createProductSchema = z.object({
  name: z.string().min(1).max(100),
  price: z.number().positive(),
  description: z.string().optional(),
  categoryId: z.string().uuid(),
});

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const data = createProductSchema.parse(body);
    
    // Check if category exists
    const category = await prisma.category.findUnique({
      where: { id: data.categoryId },
    });
    
    if (!category) {
      throw new ApiError(400, 'Category not found');
    }
    
    const product = await prisma.product.create({
      data,
    });
    
    return NextResponse.json(product, { status: 201 });
  } catch (error) {
    return handleApiError(error);
  }
}
```

### Rate Limiting and Security

```typescript
// middleware/rateLimit.ts
import { LRUCache } from 'lru-cache';

type Options = {
  uniqueTokenPerInterval?: number;
  interval?: number;
};

export function rateLimit(options?: Options) {
  const tokenCache = new LRUCache({
    max: options?.uniqueTokenPerInterval || 500,
    ttl: options?.interval || 60000,
  });
  
  return {
    check: (res: Response, limit: number, token: string) =>
      new Promise<void>((resolve, reject) => {
        const tokenCount = (tokenCache.get(token) as number[]) || [0];
        if (tokenCount[0] === 0) {
          tokenCache.set(token, tokenCount);
        }
        tokenCount[0] += 1;
        
        const currentUsage = tokenCount[0];
        const isRateLimited = currentUsage >= limit;
        res.headers.set('X-RateLimit-Limit', limit.toString());
        res.headers.set(
          'X-RateLimit-Remaining',
          isRateLimited ? '0' : (limit - currentUsage).toString()
        );
        
        return isRateLimited ? reject() : resolve();
      }),
  };
}

// app/api/protected/route.ts
const limiter = rateLimit({
  interval: 60 * 1000, // 1 minute
  uniqueTokenPerInterval: 500,
});

export async function GET(request: Request) {
  const response = new Response();
  const identifier = request.headers.get('x-forwarded-for') ?? 'anonymous';
  
  try {
    await limiter.check(response, 10, identifier); // 10 requests per minute
  } catch {
    return new Response('Too Many Requests', {
      status: 429,
      headers: response.headers,
    });
  }
  
  // Your API logic here
  return NextResponse.json({ data: 'Protected data' }, {
    headers: response.headers,
  });
}
```

## 🎭 Part 4: Performance Optimization

### Image Optimization That Actually Works

```tsx
// components/OptimizedImage.tsx
import Image from 'next/image';
import { useState } from 'react';

interface OptimizedImageProps {
  src: string;
  alt: string;
  priority?: boolean;
  className?: string;
}

export function OptimizedImage({
  src,
  alt,
  priority = false,
  className,
}: OptimizedImageProps) {
  const [isLoading, setLoading] = useState(true);
  
  return (
    <div className={`relative overflow-hidden ${className}`}>
      <Image
        src={src}
        alt={alt}
        fill
        priority={priority}
        className={`
          duration-700 ease-in-out
          ${isLoading
            ? 'scale-110 blur-2xl grayscale'
            : 'scale-100 blur-0 grayscale-0'
          }
        `}
        onLoadingComplete={() => setLoading(false)}
        sizes="(max-width: 640px) 100vw,
               (max-width: 1024px) 50vw,
               33vw"
      />
    </div>
  );
}

// next.config.js - Image optimization config
module.exports = {
  images: {
    domains: ['images.unsplash.com', 'cdn.example.com'],
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
};
```

### Bundle Size Optimization

```javascript
// next.config.js
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  webpack: (config, { isServer, dev }) => {
    // Analyze bundle in production build
    if (!dev && !isServer) {
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          reportFilename: './analyze.html',
          generateStatsFile: true,
        })
      );
    }
    
    // Tree shake lodash
    config.resolve.alias = {
      ...config.resolve.alias,
      'lodash': 'lodash-es',
    };
    
    return config;
  },
  
  // Split chunks optimally
  experimental: {
    optimizeCss: true,
  },
};

// Dynamic imports for code splitting
const HeavyComponent = dynamic(
  () => import('@/components/HeavyComponent'),
  {
    loading: () => <ComponentSkeleton />,
    ssr: false, // Only load on client
  }
);
```

## 🏗️ Module Project: E-Commerce Platform

Let's build a production-ready e-commerce platform:

```typescript
// Makefile for production setup
cat > Makefile << 'EOF'
# Production Next.js E-Commerce
include .env
export

.PHONY: setup
setup: ## Complete project setup
	@echo "🏗️  Setting up e-commerce platform..."
	pnpm install
	pnpx prisma generate
	pnpx prisma db push
	pnpm run seed
	@echo "✅ Setup complete!"

.PHONY: dev
dev: ## Start development with monitoring
	@tmux new-session -d -s dev 'pnpm dev'
	@tmux split-window -h 'pnpx prisma studio'
	@tmux split-window -v 'pnpm run monitor'
	@tmux attach-session -t dev

.PHONY: test
test: ## Run all tests
	pnpm test:unit
	pnpm test:integration
	pnpm test:e2e

.PHONY: analyze
analyze: ## Analyze bundle size
	ANALYZE=true pnpm build

.PHONY: lighthouse
lighthouse: ## Run Lighthouse CI
	pnpm build
	pnpm start &
	sleep 5
	lighthouse http://localhost:3000 \
		--output=json \
		--output-path=./lighthouse-report.json
	kill %1

.PHONY: deploy
deploy: test ## Deploy to production
	pnpm build
	vercel --prod
EOF
```

### Key Features Implementation

```typescript
// Complete e-commerce features
// 1. Product catalog with search and filters
// 2. Shopping cart with persistence
// 3. Checkout flow with Stripe
// 4. Order management
// 5. Admin dashboard
// 6. Email notifications
// 7. Inventory tracking
// 8. Analytics dashboard
```

## 🧪 Hands-On Exercises

### Exercise 1: Multi-tenant SaaS
Build a SaaS platform with:
- Organization-based data isolation
- Role-based permissions
- Subscription management
- Usage tracking

### Exercise 2: Real-time Features
Add real-time capabilities:
- Live notifications
- Collaborative editing
- Real-time analytics
- WebSocket integration

### Exercise 3: Advanced Caching
Implement caching strategies:
- Redis integration
- Edge caching
- Static regeneration
- API response caching

## ✅ Module Completion Checklist

Before moving to Module 5, ensure you can:

- [ ] Implement secure authentication flows
- [ ] Manage complex application state
- [ ] Build robust API endpoints
- [ ] Optimize images and bundle size
- [ ] Handle errors gracefully
- [ ] Implement caching strategies
- [ ] Deploy production applications

## 📚 Additional Resources

- [Next.js Production Checklist](https://nextjs.org/docs/going-to-production)
- [Web Performance Metrics](https://web.dev/metrics/)
- [Security Best Practices](https://nextjs.org/docs/security)

## 🎯 Next Steps

You've built production-ready Next.js applications! You can now:
- Handle real-world complexity
- Optimize for performance
- Implement secure authentication
- Deploy with confidence

**Ready to combine powers?** Continue to [Module 5: Makefile + Next.js Integration](/learning-plans/makefile-nextjs/module-5)

---

*Remember: The difference between development and production is like the difference between a rehearsal and opening night. In development, mistakes are learning opportunities. In production, they're Twitter threads.*