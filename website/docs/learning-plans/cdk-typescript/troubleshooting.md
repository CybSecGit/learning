# CDK TypeScript Troubleshooting Guide
*"When things go wrong (and they will), here's how to fix them"*

> **ULTRATHINKING Insight**: This guide covers real-world issues you'll encounter when deploying enterprise security infrastructure with CDK TypeScript. These aren't theoretical problems - they're battle-tested solutions from production environments.

---

## 🚨 Critical Issues & Emergency Procedures

### 🔥 Emergency Scenarios

#### **Scenario 1: Runaway Costs During Learning**
**Symptoms**: AWS billing alarm triggered, unexpected charges

**Immediate Actions**:
```bash
# 1. Stop all running CDK deployments
pkill -f "cdk deploy"

# 2. List all your CDK stacks
cdk list --profile learning

# 3. Nuclear option - destroy everything
cdk destroy --all --force --profile learning

# 4. Check for orphaned resources
aws ec2 describe-instances --filters "Name=tag:aws:cloudformation:stack-name,Values=*" --profile learning
aws s3 ls --profile learning
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --profile learning
```

**Root Cause Analysis**:
```typescript
// Common cost mistakes in CDK
// ❌ Expensive mistake
new rds.DatabaseInstance(this, 'DB', {
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.XLARGE4), // $$$
  multiAz: true // More $$$
});

// ✅ Learning-friendly approach
new rds.DatabaseInstance(this, 'DB', {
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
  multiAz: false,
  removalPolicy: RemovalPolicy.DESTROY // Critical for learning!
});
```

#### **Scenario 2: CDK Bootstrap Corruption**
**Symptoms**: `cdk deploy` fails with "Unable to resolve AWS account to use"

**Resolution Steps**:
```bash
# 1. Check current bootstrap status
aws cloudformation describe-stacks --stack-name CDKToolkit --profile learning

# 2. If corrupted, delete and re-bootstrap
aws cloudformation delete-stack --stack-name CDKToolkit --profile learning

# 3. Wait for deletion to complete
aws cloudformation wait stack-delete-complete --stack-name CDKToolkit --profile learning

# 4. Re-bootstrap with proper configuration
cdk bootstrap aws://$(aws sts get-caller-identity --query Account --output text)/us-east-1 \
  --profile learning \
  --toolkit-stack-name CDKToolkit \
  --qualifier learning
```

#### **Scenario 3: TypeScript Compilation Hell**
**Symptoms**: Cryptic TypeScript errors, `tsc` hanging, module resolution failures

**Diagnostic Commands**:
```bash
# 1. Clear all caches
rm -rf node_modules/ package-lock.json cdk.out/ .tsbuildinfo
npm cache clean --force

# 2. Reinstall dependencies
npm install

# 3. Check TypeScript configuration
npx tsc --showConfig

# 4. Compile with verbose output
npx tsc --verbose

# 5. Test CDK synthesis without build
npx cdk synth --no-build
```

---

## 🔧 Development Environment Issues

### Node.js and NPM Problems

#### **Issue: Node Version Conflicts**
**Error**: `error @aws-cdk/core@1.x requires a peer of constructs@^3.0.0`

**Solution**:
```bash
# 1. Check all Node versions
nvm list

# 2. Use consistent Node version
nvm use 18
nvm alias default 18

# 3. Clear global npm cache
npm cache clean --force

# 4. Reinstall CDK CLI
npm uninstall -g aws-cdk
npm install -g aws-cdk@latest

# 5. Verify installation
cdk --version
```

#### **Issue: Permission Denied on npm Global Install**
**Error**: `EACCES: permission denied, mkdir '/usr/local/lib/node_modules'`

**Solution**:
```bash
# Option 1: Configure npm prefix (recommended)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Option 2: Use nvm (best option)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### TypeScript Configuration Issues

#### **Issue: Module Resolution Failures**
**Error**: `Cannot find module '@aws-cdk/aws-s3' or its corresponding type declarations`

**Solution**:
```json
// tsconfig.json - Ensure proper configuration
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  },
  "include": ["lib/**/*", "bin/**/*"],
  "exclude": ["node_modules", "cdk.out"]
}
```

```bash
# Clear TypeScript build cache
rm -f .tsbuildinfo

# Reinstall type definitions
npm install --save-dev @types/node@latest
```

#### **Issue: CDK v1 vs v2 Confusion**
**Error**: Mixed import statements causing compilation errors

**Migration Guide**:
```typescript
// ❌ CDK v1 style (deprecated)
import * as s3 from '@aws-cdk/aws-s3';
import * as core from '@aws-cdk/core';

export class MyStack extends core.Stack {
  constructor(scope: core.Construct, id: string, props?: core.StackProps) {
    super(scope, id, props);
    
    new s3.Bucket(this, 'MyBucket');
  }
}

// ✅ CDK v2 style (current)
import { Stack, StackProps } from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export class MyStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);
    
    new s3.Bucket(this, 'MyBucket');
  }
}
```

**Automated Migration**:
```bash
# Use CDK migration tool
npx cdk-migrate
```

---

## 🔐 AWS Configuration and Permissions

### Credential Issues

#### **Issue: AWS Credentials Not Found**
**Error**: `Unable to locate credentials`

**Diagnostic Steps**:
```bash
# 1. Check current credentials
aws sts get-caller-identity

# 2. List configured profiles
aws configure list-profiles

# 3. Check credential file
cat ~/.aws/credentials
cat ~/.aws/config

# 4. Test specific profile
aws sts get-caller-identity --profile learning
```

**Resolution**:
```bash
# Option 1: Configure new profile
aws configure --profile learning

# Option 2: Use environment variables
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_DEFAULT_REGION=us-east-1

# Option 3: Use SSO
aws configure sso --profile learning
```

#### **Issue: Permission Denied During CDK Deploy**
**Error**: `AccessDenied: User is not authorized to perform: cloudformation:CreateStack`

**Required IAM Permissions for CDK Learning**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "s3:*",
        "iam:*",
        "lambda:*",
        "ec2:*",
        "logs:*",
        "events:*",
        "sns:*",
        "sqs:*",
        "dynamodb:*",
        "apigateway:*",
        "cloudfront:*",
        "route53:*",
        "acm:*",
        "ssm:*",
        "secretsmanager:*",
        "kms:*",
        "config:*",
        "cloudtrail:*",
        "guardduty:*",
        "securityhub:*",
        "inspector2:*"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sts:AssumeRole"
      ],
      "Resource": "arn:aws:iam::*:role/cdk-*"
    }
  ]
}
```

### Bootstrap Issues

#### **Issue: Bootstrap Version Mismatch**
**Error**: `This CDK CLI is not compatible with the CDK library used by your application`

**Solution**:
```bash
# 1. Check CDK versions
cdk --version
npm list aws-cdk-lib

# 2. Upgrade CDK CLI
npm install -g aws-cdk@latest

# 3. Upgrade CDK library in project
npm install aws-cdk-lib@latest

# 4. Re-bootstrap if necessary
cdk bootstrap --force
```

---

## 🏗️ CDK Specific Issues

### Construct and Stack Problems

#### **Issue: Circular Dependencies Between Stacks**
**Error**: `Circular dependency between resources`

**Problem Code**:
```typescript
// ❌ Creates circular dependency
export class StackA extends Stack {
  public readonly resource: SomeResource;
  
  constructor(scope: Construct, id: string, props: {stackB: StackB}) {
    super(scope, id);
    this.resource = new SomeResource(this, 'Resource', {
      dependency: props.stackB.someOutput
    });
  }
}

export class StackB extends Stack {
  public readonly someOutput: string;
  
  constructor(scope: Construct, id: string, props: {stackA: StackA}) {
    super(scope, id);
    // This creates a circular dependency
    const resource = new AnotherResource(this, 'Resource', {
      reference: props.stackA.resource
    });
    this.someOutput = resource.output;
  }
}
```

**Solution**:
```typescript
// ✅ Break circular dependency with shared construct
export class SharedResourcesStack extends Stack {
  public readonly sharedResource: SharedResource;
  
  constructor(scope: Construct, id: string) {
    super(scope, id);
    this.sharedResource = new SharedResource(this, 'Shared');
  }
}

export class StackA extends Stack {
  constructor(scope: Construct, id: string, props: {shared: SharedResourcesStack}) {
    super(scope, id);
    new SomeResource(this, 'Resource', {
      dependency: props.shared.sharedResource
    });
  }
}

export class StackB extends Stack {
  constructor(scope: Construct, id: string, props: {shared: SharedResourcesStack}) {
    super(scope, id);
    new AnotherResource(this, 'Resource', {
      reference: props.shared.sharedResource
    });
  }
}
```

#### **Issue: Resource Naming Conflicts**
**Error**: `Resource with name 'MyResource' already exists`

**Solution**:
```typescript
// ❌ Potential naming conflict
new s3.Bucket(this, 'MyBucket', {
  bucketName: 'my-bucket' // Hardcoded name
});

// ✅ CDK-generated names with logical IDs
new s3.Bucket(this, 'DataBucket', {
  // Let CDK generate unique name
});

// ✅ Environment-specific naming
new s3.Bucket(this, 'DataBucket', {
  bucketName: `my-app-data-${props.environment}-${this.account}`
});
```

### Deployment Issues

#### **Issue: CloudFormation Stack Stuck in UPDATE_ROLLBACK_FAILED**
**Error**: Stack cannot complete rollback

**Resolution**:
```bash
# 1. Check stack events
aws cloudformation describe-stack-events --stack-name YourStackName

# 2. Continue rollback (skip problematic resources)
aws cloudformation continue-update-rollback --stack-name YourStackName

# 3. If that fails, delete specific resources manually
aws cloudformation cancel-update-stack --stack-name YourStackName

# 4. Last resort: delete and redeploy stack
cdk destroy YourStackName --force
cdk deploy YourStackName
```

#### **Issue: Resource Already Exists in Different Stack**
**Error**: `Resource already exists`

**Diagnostic**:
```bash
# Find which stack owns the resource
aws cloudformation describe-stack-resources --logical-resource-id YourResourceId

# Or search by physical resource ID
aws cloudformation describe-stack-resources --physical-resource-id YourActualResourceId
```

**Solutions**:
```typescript
// Option 1: Import existing resource
const existingBucket = s3.Bucket.fromBucketName(this, 'ExistingBucket', 'actual-bucket-name');

// Option 2: Use different logical ID
new s3.Bucket(this, 'NewUniqueBucketId');

// Option 3: Add to removal policy for learning
new s3.Bucket(this, 'Bucket', {
  removalPolicy: RemovalPolicy.DESTROY,
  autoDeleteObjects: true // For learning only!
});
```

---

## 🧪 Testing and Debugging

### CDK Testing Issues

#### **Issue: Tests Failing with Template Assertions**
**Error**: `Template.hasResourceProperties` not working

**Common Mistakes**:
```typescript
// ❌ Incorrect test approach
import { Template } from 'aws-cdk-lib/assertions';

test('creates S3 bucket', () => {
  const template = Template.fromStack(stack);
  
  // This might fail due to CDK-generated properties
  template.hasResourceProperties('AWS::S3::Bucket', {
    BucketName: 'my-bucket'
  });
});
```

**Better Testing Approach**:
```typescript
// ✅ More flexible testing
import { Template, Match } from 'aws-cdk-lib/assertions';

test('creates S3 bucket with encryption', () => {
  const template = Template.fromStack(stack);
  
  // Test for presence and key properties
  template.hasResourceProperties('AWS::S3::Bucket', {
    BucketEncryption: {
      ServerSideEncryptionConfiguration: [
        {
          ServerSideEncryptionByDefault: {
            SSEAlgorithm: 'AES256'
          }
        }
      ]
    }
  });
  
  // Count resources
  template.resourceCountIs('AWS::S3::Bucket', 1);
  
  // Use matchers for flexible assertions
  template.hasResourceProperties('AWS::S3::Bucket', {
    BucketName: Match.stringLikeRegexp('.*-bucket-.*')
  });
});
```

### Debugging CDK Synthesis

#### **Issue: Synth Produces Unexpected CloudFormation**
**Error**: Generated template doesn't match expectations

**Debugging Steps**:
```bash
# 1. Synthesize with verbose output
cdk synth --verbose

# 2. Output to file for inspection
cdk synth > template.json

# 3. Compare templates
cdk diff

# 4. Debug specific construct
cdk synth --exclusively YourSpecificStack
```

**Code Debugging**:
```typescript
// Add debugging output to your constructs
export class DebuggableStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);
    
    const bucket = new s3.Bucket(this, 'Bucket');
    
    // Debug output
    new CfnOutput(this, 'BucketName', {
      value: bucket.bucketName,
      description: 'The name of the S3 bucket'
    });
    
    console.log(`Creating bucket in stack ${this.stackName}`);
  }
}
```

---

## 📊 Performance and Optimization

### CDK Performance Issues

#### **Issue: Slow CDK Synthesis**
**Symptoms**: `cdk synth` takes minutes to complete

**Optimization Strategies**:
```typescript
// ❌ Performance killer
export class SlowStack extends Stack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    
    // Creating resources in loops without optimization
    for (let i = 0; i < 100; i++) {
      new lambda.Function(this, `Function${i}`, {
        runtime: lambda.Runtime.NODEJS_18_X,
        handler: 'index.handler',
        code: lambda.Code.fromInline(`
          exports.handler = async () => {
            return { statusCode: 200 };
          };
        `)
      });
    }
  }
}

// ✅ Optimized approach
export class OptimizedStack extends Stack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    
    // Create a reusable construct
    const sharedLayer = new lambda.LayerVersion(this, 'SharedLayer', {
      code: lambda.Code.fromAsset('lambda-layer'),
      compatibleRuntimes: [lambda.Runtime.NODEJS_18_X]
    });
    
    // Use shared resources efficiently
    const functionConfigs = this.getFunctionConfigs();
    functionConfigs.forEach(config => {
      new lambda.Function(this, config.id, {
        ...config.props,
        layers: [sharedLayer]
      });
    });
  }
  
  private getFunctionConfigs() {
    // Generate configurations efficiently
    return Array.from({length: 100}, (_, i) => ({
      id: `Function${i}`,
      props: {
        runtime: lambda.Runtime.NODEJS_18_X,
        handler: 'index.handler',
        code: lambda.Code.fromAsset(`lambda-functions/function-${i}`)
      }
    }));
  }
}
```

#### **Issue: Large Bundle Sizes**
**Solution**:
```typescript
// Use CDK bundling options
new lambda.Function(this, 'Function', {
  runtime: lambda.Runtime.NODEJS_18_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('lambda', {
    bundling: {
      image: lambda.Runtime.NODEJS_18_X.bundlingImage,
      command: [
        'bash', '-c',
        'npm install && npm run build && cp -r dist/* /asset-output/'
      ],
      environment: {
        NODE_ENV: 'production'
      }
    }
  })
});
```

---

## 🔍 Diagnostic Tools and Commands

### Essential Diagnostic Commands

```bash
# CDK diagnostics
cdk doctor                    # Check CDK environment
cdk diff --verbose           # Detailed differences
cdk synth --verbose          # Verbose synthesis
cdk ls --long               # List stacks with details

# AWS CloudFormation diagnostics
aws cloudformation validate-template --template-body file://template.json
aws cloudformation describe-stack-events --stack-name YourStack
aws cloudformation get-template --stack-name YourStack

# TypeScript diagnostics
npx tsc --noEmit            # Check types without compilation
npx tsc --listFiles         # Show all files being compiled
npx tsc --traceResolution   # Debug module resolution

# npm diagnostics
npm ls                      # Show dependency tree
npm audit                   # Security vulnerabilities
npm outdated               # Show outdated packages
```

### Creating Debug-Friendly CDK Apps

```typescript
// Debug-enabled CDK app
import { App, Aspects } from 'aws-cdk-lib';
import { AwsSolutionsChecks } from 'cdk-nag';

const app = new App();

// Add debugging aspects
if (process.env.CDK_DEBUG) {
  // Add comprehensive compliance checking
  Aspects.of(app).add(new AwsSolutionsChecks({ verbose: true }));
  
  // Custom debugging aspect
  Aspects.of(app).add(new class implements IAspect {
    visit(node: IConstruct): void {
      console.log(`Visiting construct: ${node.node.path}`);
      
      // Log all construct metadata
      const metadata = node.node.metadata;
      if (metadata.length > 0) {
        console.log(`Metadata:`, metadata);
      }
    }
  });
}
```

---

## 🆘 Getting Help

### When to Ask for Help

1. **After trying documented solutions** - Don't skip the basics
2. **With specific error messages** - Include full stack traces
3. **With minimal reproducible examples** - Strip out unrelated code
4. **With environment details** - CDK version, Node version, OS

### Where to Get Help

- **AWS CDK GitHub Issues**: https://github.com/aws/aws-cdk/issues
- **AWS CDK Slack**: https://cdk.dev
- **Stack Overflow**: Tag questions with `aws-cdk`
- **AWS re:Post**: https://repost.aws/tags/TArnj__D3pT2G-qUQfYHzYiQ/aws-cloud-development-kit

### How to Report Issues Effectively

```bash
# Collect diagnostic information
echo "CDK Version: $(cdk --version)"
echo "Node Version: $(node --version)"
echo "NPM Version: $(npm --version)"
echo "TypeScript Version: $(tsc --version)"
echo "OS: $(uname -a)"

# Generate debug output
cdk synth --verbose > debug-output.txt 2>&1
cdk diff --verbose >> debug-output.txt 2>&1
```

---

**Remember**: Most CDK TypeScript issues are environment-related or caused by version mismatches. Start with the basics, check versions, and always read the error messages carefully. The CDK community is helpful, but they expect you to do your homework first! 🎓