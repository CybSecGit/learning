# TypeScript Project CLAUDE.md

## Project Overview
This is a full-stack TypeScript application using Next.js 14 with App Router, React Server Components, and Prisma ORM. The project emphasizes type safety, performance, and modern web standards.

## Core Development Principles

### TypeScript Configuration
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Architecture Patterns
- Server Components by default
- Client Components only when necessary
- API routes for external integrations
- Server Actions for mutations
- Middleware for auth and redirects

## Project Structure
```
project/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth group routes
│   ├── api/               # API routes
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # Presentational components
│   └── features/         # Feature-specific components
├── lib/                  # Shared utilities
│   ├── db.ts            # Database client
│   ├── auth.ts          # Auth utilities
│   └── utils.ts         # Helper functions
├── hooks/               # Custom React hooks
├── services/           # Business logic
├── types/             # TypeScript types
├── prisma/           # Database schema
└── public/          # Static assets
```

## Type Safety Patterns

### Strict Type Definitions
```typescript
// Avoid 'any' at all costs
type User = {
  id: string;
  email: string;
  profile: {
    name: string;
    avatar?: string; // Optional properties explicit
  };
  createdAt: Date;
};

// Use discriminated unions for state
type AsyncState<T> = 
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// Const assertions for literals
const ROLES = ['admin', 'user', 'guest'] as const;
type Role = typeof ROLES[number];
```

### Zod for Runtime Validation
```typescript
import { z } from 'zod';

// Define schema once, infer types
const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  role: z.enum(['admin', 'user', 'guest']),
});

type UserInput = z.infer<typeof UserSchema>;

// Validate at runtime
export async function createUser(input: unknown) {
  const validated = UserSchema.parse(input);
  // validated is fully typed
}
```

## React Patterns

### Server Components
```typescript
// app/users/page.tsx
import { prisma } from '@/lib/db';

// This runs on the server only
export default async function UsersPage() {
  const users = await prisma.user.findMany();
  
  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

### Client Components
```typescript
'use client';

import { useState, useTransition } from 'react';
import { updateUser } from '@/app/actions';

export function UserForm({ user }: { user: User }) {
  const [isPending, startTransition] = useTransition();
  
  function handleSubmit(formData: FormData) {
    startTransition(async () => {
      await updateUser(formData);
    });
  }
  
  return (
    <form action={handleSubmit}>
      {/* Form fields */}
    </form>
  );
}
```

### Server Actions
```typescript
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function updateUser(formData: FormData) {
  const session = await getSession();
  if (!session) {
    throw new Error('Unauthorized');
  }
  
  const data = Object.fromEntries(formData);
  const validated = UserUpdateSchema.parse(data);
  
  await prisma.user.update({
    where: { id: session.userId },
    data: validated,
  });
  
  revalidatePath('/profile');
  redirect('/profile');
}
```

## State Management

### For Server State
```typescript
// Use React Query/SWR for server state
import useSWR from 'swr';

export function useUser(id: string) {
  return useSWR<User>(`/api/users/${id}`, fetcher, {
    revalidateOnFocus: false,
    dedupingInterval: 60000,
  });
}
```

### For Client State
```typescript
// Zustand for complex client state
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface AppState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useAppStore = create<AppState>()(
  immer((set) => ({
    theme: 'light',
    sidebarOpen: true,
    toggleSidebar: () => set((state) => {
      state.sidebarOpen = !state.sidebarOpen;
    }),
    setTheme: (theme) => set((state) => {
      state.theme = theme;
    }),
  }))
);
```

## Testing Strategy

### Component Testing
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('UserForm', () => {
  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    
    render(<UserForm onSubmit={onSubmit} />);
    
    await user.type(screen.getByLabelText('Email'), 'test@example.com');
    await user.click(screen.getByRole('button', { name: 'Submit' }));
    
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
    });
  });
});
```

### API Testing
```typescript
import { createMocks } from 'node-mocks-http';
import handler from '@/app/api/users/route';

describe('/api/users', () => {
  it('returns users list', async () => {
    const { req, res } = createMocks({
      method: 'GET',
    });
    
    await handler(req, res);
    
    expect(res._getStatusCode()).toBe(200);
    expect(JSON.parse(res._getData())).toHaveLength(3);
  });
});
```

## Performance Optimization

### Image Optimization
```typescript
import Image from 'next/image';

export function Avatar({ user }: { user: User }) {
  return (
    <Image
      src={user.avatar || '/default-avatar.png'}
      alt={user.name}
      width={40}
      height={40}
      quality={85}
      placeholder="blur"
      blurDataURL={user.avatarBlur}
    />
  );
}
```

### Code Splitting
```typescript
import dynamic from 'next/dynamic';

// Load heavy components only when needed
const RichTextEditor = dynamic(
  () => import('@/components/RichTextEditor'),
  { 
    loading: () => <EditorSkeleton />,
    ssr: false,
  }
);
```

### Data Fetching
```typescript
// Parallel data fetching
export default async function DashboardPage() {
  const [user, posts, comments] = await Promise.all([
    getUser(),
    getPosts(),
    getComments(),
  ]);
  
  return <Dashboard user={user} posts={posts} comments={comments} />;
}
```

## Security Best Practices

### Input Sanitization
```typescript
import DOMPurify from 'isomorphic-dompurify';

export function sanitizeHTML(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href'],
  });
}
```

### Authentication
```typescript
import { cookies } from 'next/headers';
import { verify } from 'jsonwebtoken';

export async function getSession() {
  const token = cookies().get('session')?.value;
  if (!token) return null;
  
  try {
    const payload = verify(token, process.env.JWT_SECRET!);
    return payload as SessionPayload;
  } catch {
    return null;
  }
}

// Protect routes with middleware
export async function middleware(request: NextRequest) {
  const session = await getSession();
  
  if (!session && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}
```

## Error Handling

### Error Boundaries
```typescript
'use client';

export function ErrorBoundary({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
    logErrorToService(error);
  }, [error]);
  
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Type-Safe Error Handling
```typescript
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
  }
}

export async function apiHandler<T>(
  handler: () => Promise<T>
): Promise<ApiResponse<T>> {
  try {
    const data = await handler();
    return { success: true, data };
  } catch (error) {
    if (error instanceof AppError) {
      return {
        success: false,
        error: {
          code: error.code,
          message: error.message,
        },
      };
    }
    return {
      success: false,
      error: {
        code: 'UNKNOWN_ERROR',
        message: 'An unexpected error occurred',
      },
    };
  }
}
```

## Development Workflow

### Scripts
```json
{
  "scripts": {
    "dev": "next dev --turbo",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .ts,.tsx",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:e2e": "playwright test",
    "db:push": "prisma db push",
    "db:studio": "prisma studio"
  }
}
```

### Git Hooks with Husky
```bash
# .husky/pre-commit
#!/bin/sh
npm run lint
npm run type-check
npm run test
```

### VS Code Settings
```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

## Performance Metrics
- Core Web Vitals all green
- Lighthouse score > 95
- Bundle size < 200KB (First Load JS)
- Time to Interactive < 3s
- API response time < 200ms (p95)

## Deployment Checklist
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Build succeeds without warnings
- [ ] All tests pass
- [ ] Security headers configured
- [ ] Error tracking enabled
- [ ] Analytics configured
- [ ] Performance monitoring active

## Import External Standards
@../imports/error-handling.md
@../imports/testing-conventions.md
@../imports/security-guidelines.md
@../imports/git-workflow.md
@../imports/style-guide.md