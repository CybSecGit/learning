# Module 1: TypeScript Fundamentals for AWS Wizards
*"Because you can't cast CDK spells without knowing the language"*

> **Duration**: 1-2 weeks  
> **Cost**: ~$0/day  
> **Prerequisites**: Basic programming experience, CloudFormation knowledge

---

## 🎯 Module Learning Objectives

By the end of this module, you will:
- **Master TypeScript syntax** essential for CDK development
- **Understand async patterns** critical for AWS API interactions  
- **Navigate the NPM ecosystem** for CDK dependencies
- **Set up a productive development environment** for CDK TypeScript

---

## 📚 Core Lessons

### Lesson 1.1: TypeScript Syntax Crash Course
*"Getting the basics down without the fluff"*

#### Essential TypeScript for CDK

**Interfaces and Types** (Your CDK construct props foundation):
```typescript
// CDK construct props pattern
interface DatabaseStackProps extends StackProps {
  readonly databaseName: string;
  readonly backupRetentionDays: number;
  readonly multiAz?: boolean; // Optional with default
}

// Union types for AWS resource configurations
type InstanceClass = 'db.t3.micro' | 'db.t3.small' | 'db.t3.medium';
type Environment = 'dev' | 'staging' | 'prod';

// Utility types for CDK patterns
type RequiredProps<T> = Required<Pick<T, keyof T>>;
```

**Generics** (For reusable CDK constructs):
```typescript
// Generic construct for different resource types
interface ResourceConfigProps<T> {
  readonly config: T;
  readonly tags: Record<string, string>;
}

class ConfigurableConstruct<T> extends Construct {
  constructor(scope: Construct, id: string, props: ResourceConfigProps<T>) {
    super(scope, id);
    // Implementation here
  }
}
```

**Enums and Constants** (AWS service configurations):
```typescript
// Better than magic strings in CDK
enum LogLevel {
  ERROR = 'ERROR',
  WARN = 'WARN', 
  INFO = 'INFO',
  DEBUG = 'DEBUG'
}

const SECURITY_GROUPS = {
  WEB_TIER: 'web-tier-sg',
  APP_TIER: 'app-tier-sg',
  DB_TIER: 'db-tier-sg'
} as const;
```

#### 🛠️ Hands-On Lab 1.1: Type-Safe AWS Configuration

**Challenge**: Create type-safe configuration objects for a multi-tier application.

```typescript
// Create interfaces for each tier's configuration
interface WebTierConfig {
  readonly instanceType: 't3.micro' | 't3.small' | 't3.medium';
  readonly minCapacity: number;
  readonly maxCapacity: number;
  readonly desiredCapacity: number;
}

interface DatabaseConfig {
  readonly engine: 'mysql' | 'postgres' | 'aurora-mysql';
  readonly instanceClass: string;
  readonly multiAz: boolean;
  readonly backupRetention: number;
}

// Your task: Create a complete application configuration interface
// that combines these with proper validation
```

**Success Criteria**: 
- TypeScript compiler shows no errors
- Configuration prevents invalid combinations
- IntelliSense provides helpful autocomplete

---

### Lesson 1.2: Classes, Inheritance, and Async Patterns  
*"Object-oriented infrastructure and async AWS calls"*

#### Class Patterns for CDK Constructs

**Basic CDK Construct Pattern**:
```typescript
import { Construct } from 'constructs';
import { Stack, StackProps } from 'aws-cdk-lib';

export class SecurityStack extends Stack {
  public readonly securityGroup: SecurityGroup;
  public readonly role: Role;

  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);
    
    // CDK construct creation here
    this.securityGroup = new SecurityGroup(this, 'SecurityGroup', {
      vpc: props?.vpc,
      description: 'Security group for application'
    });

    this.role = new Role(this, 'ApplicationRole', {
      assumedBy: new ServicePrincipal('lambda.amazonaws.com')
    });
  }
}
```

**Inheritance for Reusable Patterns**:
```typescript
// Base class for all your security-focused stacks
abstract class SecurityBaseStack extends Stack {
  protected readonly defaultTags: Record<string, string>;
  
  constructor(scope: Construct, id: string, props: SecurityStackProps) {
    super(scope, id, props);
    
    this.defaultTags = {
      Environment: props.environment,
      Project: props.projectName,
      ManagedBy: 'CDK'
    };
  }
  
  // Abstract method that child classes must implement
  protected abstract setupSecurityResources(): void;
}

class WebApplicationSecurityStack extends SecurityBaseStack {
  protected setupSecurityResources(): void {
    // Implementation specific to web applications
  }
}
```

#### Async/Await Patterns for AWS APIs

**AWS SDK v3 with TypeScript**:
```typescript
import { EC2Client, DescribeInstancesCommand } from '@aws-sdk/client-ec2';

class InstanceManager {
  private readonly ec2Client: EC2Client;
  
  constructor(region: string) {
    this.ec2Client = new EC2Client({ region });
  }
  
  async getRunningInstances(): Promise<Instance[]> {
    try {
      const command = new DescribeInstancesCommand({
        Filters: [
          {
            Name: 'instance-state-name',
            Values: ['running']
          }
        ]
      });
      
      const response = await this.ec2Client.send(command);
      return this.extractInstances(response);
    } catch (error) {
      console.error('Failed to get running instances:', error);
      throw new Error(`Instance query failed: ${error.message}`);
    }
  }
  
  private extractInstances(response: DescribeInstancesCommandOutput): Instance[] {
    // Type-safe extraction logic
    return response.Reservations?.flatMap(r => r.Instances || []) || [];
  }
}
```

#### 🛠️ Hands-On Lab 1.2: AWS SDK TypeScript Script

**Challenge**: Build a security auditing script that queries AWS resources.

```typescript
// Your mission: Create a SecurityAuditor class that:
// 1. Lists all security groups with overly permissive rules
// 2. Identifies unencrypted S3 buckets
// 3. Finds IAM users with admin access
// 4. Returns a type-safe audit report

interface SecurityFinding {
  readonly resourceType: 'security-group' | 's3-bucket' | 'iam-user';
  readonly resourceId: string;
  readonly severity: 'low' | 'medium' | 'high' | 'critical';
  readonly description: string;
  readonly recommendation: string;
}

interface AuditReport {
  readonly timestamp: Date;
  readonly region: string;
  readonly findings: SecurityFinding[];
  readonly summary: {
    readonly total: number;
    readonly bySeverity: Record<string, number>;
  };
}

class SecurityAuditor {
  // Your implementation here
  async runAudit(): Promise<AuditReport> {
    // Implement the audit logic
  }
}
```

**Success Criteria**:
- Script runs without TypeScript errors
- Proper error handling with try/catch
- Type-safe return values
- Real AWS API calls (use your learning account!)

---

### Lesson 1.3: NPM Ecosystem and Dependency Management
*"Navigating the package jungle like a pro"*

#### Essential NPM Commands for CDK Development

**Project Initialization**:
```bash
# Initialize a new CDK TypeScript project
npm init -y
npm install -g aws-cdk

# CDK project setup
cdk init app --language=typescript
```

**Dependency Management**:
```bash
# Core CDK dependencies
npm install aws-cdk-lib constructs

# Development dependencies
npm install --save-dev @types/node typescript jest @types/jest ts-jest

# Security and compliance tools
npm install --save-dev cdk-nag @aws-cdk/assert

# Useful CDK utilities
npm install @aws-cdk/aws-lambda-nodejs @aws-cdk/aws-apigatewayv2-alpha
```

#### Package.json for CDK Projects

**Essential Scripts**:
```json
{
  "scripts": {
    "build": "tsc",
    "watch": "tsc -w", 
    "test": "jest",
    "test:watch": "jest --watch",
    "cdk": "cdk",
    "deploy": "cdk deploy",
    "diff": "cdk diff",
    "synth": "cdk synth",
    "destroy": "cdk destroy"
  },
  "devDependencies": {
    "@types/jest": "^29.5.0",
    "@types/node": "^18.15.0",
    "jest": "^29.5.0",
    "ts-jest": "^29.1.0",
    "typescript": "^5.0.0",
    "cdk-nag": "^2.25.0"
  },
  "dependencies": {
    "aws-cdk-lib": "^2.80.0",
    "constructs": "^10.0.0"
  }
}
```

#### TypeScript Configuration for CDK

**tsconfig.json optimized for CDK**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "declaration": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": false,
    "inlineSourceMap": true,
    "inlineSources": true,
    "experimentalDecorators": true,
    "strictPropertyInitialization": false,
    "typeRoots": ["./node_modules/@types"],
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "exclude": ["cdk.out"]
}
```

#### 🛠️ Hands-On Lab 1.3: CDK Project Setup

**Challenge**: Set up a complete CDK TypeScript project with all best practices.

**Your Mission**:
1. Initialize a new CDK TypeScript project
2. Configure proper TypeScript settings
3. Add essential development dependencies
4. Set up Jest testing framework
5. Configure cdk-nag for compliance checking
6. Create a "hello world" stack that deploys successfully

**Project Structure Goal**:
```
my-cdk-project/
├── bin/
│   └── app.ts              # CDK app entry point
├── lib/
│   ├── stacks/
│   │   └── hello-world-stack.ts
│   └── constructs/
├── test/
│   └── hello-world.test.ts
├── package.json
├── tsconfig.json
├── cdk.json
└── jest.config.js
```

**Success Criteria**:
- `npm run build` completes without errors
- `npm test` runs and passes
- `cdk synth` generates CloudFormation template
- `cdk deploy` deploys successfully
- `cdk destroy` cleans up resources

---

### Lesson 1.4: IDE Setup for Maximum Productivity
*"Turning your editor into a CDK powerhouse"*

#### VS Code Setup for CDK TypeScript

**Essential Extensions**:
```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-vscode.vscode-typescript-next",
    "amazonwebservices.aws-toolkit-vscode", 
    "ms-vscode.vscode-json",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-eslint"
  ]
}
```

**Workspace Settings**:
```json
// .vscode/settings.json
{
  "typescript.preferences.quoteStyle": "single",
  "typescript.format.insertSpaceAfterFunctionKeywordForAnonymousFunctions": false,
  "typescript.updateImportsOnFileMove.enabled": "always",
  "editor.codeActionsOnSave": {
    "source.organizeImports": true,
    "source.fixAll.eslint": true
  },
  "aws.cdk.explorer.enabled": true,
  "aws.telemetry": false
}
```

**Code Snippets for CDK**:
```json
// .vscode/cdk-snippets.code-snippets
{
  "CDK Stack": {
    "prefix": "cdk-stack",
    "body": [
      "import { Stack, StackProps } from 'aws-cdk-lib';",
      "import { Construct } from 'constructs';",
      "",
      "export class ${1:StackName} extends Stack {",
      "  constructor(scope: Construct, id: string, props?: StackProps) {",
      "    super(scope, id, props);",
      "    ",
      "    $0",
      "  }",
      "}"
    ],
    "description": "Create a new CDK Stack"
  },
  "CDK Construct": {
    "prefix": "cdk-construct",
    "body": [
      "import { Construct } from 'constructs';",
      "",
      "export interface ${1:ConstructName}Props {",
      "  $2",
      "}",
      "",
      "export class ${1:ConstructName} extends Construct {",
      "  constructor(scope: Construct, id: string, props: ${1:ConstructName}Props) {",
      "    super(scope, id);",
      "    ",
      "    $0",
      "  }",
      "}"
    ],
    "description": "Create a new CDK Construct"
  }
}
```

#### Debugging Configuration

**Launch Configuration for CDK**:
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug CDK Synth",
      "program": "${workspaceFolder}/node_modules/aws-cdk/bin/cdk",
      "args": ["synth"],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "env": {
        "NODE_ENV": "development"
      }
    },
    {
      "type": "node",
      "request": "launch", 
      "name": "Debug Jest Tests",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": ["--runInBand"],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    }
  ]
}
```

#### 🛠️ Hands-On Lab 1.4: Complete Development Environment

**Challenge**: Set up the ultimate CDK TypeScript development environment.

**Your Mission**:
1. Configure VS Code with all essential extensions
2. Set up TypeScript IntelliSense for CDK constructs
3. Configure debugging for CDK applications
4. Set up auto-formatting and linting
5. Test the environment with a simple CDK construct

**Validation Steps**:
1. **IntelliSense Test**: Type `new` in a CDK stack and verify autocomplete shows AWS constructs
2. **Debugging Test**: Set breakpoint in CDK code and debug successfully
3. **Formatting Test**: Auto-format messy TypeScript code
4. **Error Detection**: Verify TypeScript errors appear inline as you type

**Success Criteria**:
- Code completion works for CDK constructs
- Debugging session can step through CDK code  
- Auto-formatting works on save
- Syntax errors highlighted in real-time
- AWS CDK Explorer shows your stacks

---

## 📋 Module 1 Assessment

### Knowledge Check Quiz

**Question 1**: Which TypeScript feature is most important for CDK construct props?
- a) Classes
- b) Interfaces ✓
- c) Enums  
- d) Functions

**Question 2**: What's the correct way to handle async AWS API calls in TypeScript?
- a) Callbacks
- b) Promises with .then()
- c) async/await ✓
- d) Synchronous calls

**Question 3**: Which NPM script is essential for CDK development?
- a) `npm run build` ✓
- b) `npm run start`
- c) `npm run serve`
- d) `npm run generate`

### Practical Assessment

**Mini-Project**: Build a "CDK Environment Validator"

Create a TypeScript utility that:
1. **Validates your CDK development environment**
2. **Checks for required dependencies**
3. **Tests AWS credentials and permissions**
4. **Generates a type-safe environment report**

```typescript
interface EnvironmentCheck {
  readonly name: string;
  readonly status: 'pass' | 'fail' | 'warning';
  readonly message: string;
  readonly recommendation?: string;
}

interface EnvironmentReport {
  readonly timestamp: Date;
  readonly overallStatus: 'healthy' | 'issues' | 'critical';
  readonly checks: EnvironmentCheck[];
}

class CDKEnvironmentValidator {
  async validateEnvironment(): Promise<EnvironmentReport> {
    // Your implementation:
    // 1. Check Node.js version
    // 2. Verify CDK CLI installation
    // 3. Test AWS credentials
    // 4. Validate TypeScript configuration
    // 5. Check required dependencies
  }
}
```

**Success Criteria**:
- TypeScript compiles without errors
- Utility successfully validates your environment
- Report includes actionable recommendations
- Code demonstrates proper async/await usage
- Interface design shows TypeScript best practices

---

## 🚀 Ready for Module 2?

**Before proceeding, ensure you can:**
- ✅ Write TypeScript interfaces for CDK props
- ✅ Use async/await with AWS SDK v3
- ✅ Set up and configure a CDK TypeScript project  
- ✅ Navigate your IDE efficiently for CDK development

**Next Up**: [Module 2: CDK Foundations & Mental Model Shift](/learning-plans/cdk-typescript/module-2)

---

## 💡 Reflection Prompts

1. **How does TypeScript's type system help prevent infrastructure bugs compared to CloudFormation?**

2. **What async patterns from this module will be most useful for CDK development?**

3. **How would you explain the benefits of TypeScript for infrastructure code to a CloudFormation expert?**

---

*Remember: You're building the TypeScript foundation for CDK mastery. Every interface, every async function, every type annotation is preparing you for infrastructure wizardry! 🧙‍♂️*