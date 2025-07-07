# CDK TypeScript Learning Environment Setup
*"Preparing your arsenal for infrastructure wizardry"*

> **ULTRATHINKING Alert**: This setup is designed for cybersecurity professionals who will be deploying enterprise-grade security infrastructure. Every tool and configuration is chosen for real-world security platform development.

---

## 🎯 Setup Objectives

By completing this setup, you will have:
- **Production-grade CDK TypeScript development environment**
- **Multi-account AWS configuration** for realistic enterprise scenarios
- **Security-focused toolchain** for compliance and vulnerability scanning
- **Cost monitoring and controls** to prevent learning budget explosions
- **Debugging and troubleshooting capabilities** for complex CDK applications

---

## 🏗️ Architecture of Your Learning Environment

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your Learning Setup                          │
├─────────────────────────────────────────────────────────────────┤
│  Development Environment                                        │
│  ├── VS Code with CDK TypeScript extensions                     │
│  ├── Node.js 18+ with TypeScript 5.0+                         │
│  ├── AWS CLI v2 with SSO configuration                         │
│  └── CDK CLI v2 with multi-account bootstrap                   │
├─────────────────────────────────────────────────────────────────┤
│  AWS Account Strategy                                           │
│  ├── Learning Account (where you'll deploy and destroy)        │
│  ├── Shared Services Account (simulated enterprise)            │
│  └── Security Account (centralized security monitoring)        │
├─────────────────────────────────────────────────────────────────┤
│  Security & Compliance Tools                                   │
│  ├── cdk-nag for compliance checking                          │
│  ├── Checkov for infrastructure security scanning              │
│  ├── Trivy for container vulnerability scanning                │
│  └── AWS Config for continuous compliance monitoring           │
├─────────────────────────────────────────────────────────────────┤
│  Cost Management & Safety                                      │
│  ├── AWS Budgets with aggressive alerts                        │
│  ├── Cost allocation tags for all resources                    │
│  ├── Automated cleanup scripts and teardown workflows          │
│  └── Resource lifecycle management                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Step 1: Development Environment Setup

### Node.js and TypeScript Configuration

**Install Node.js 18+ (LTS)**:
```bash
# Using Node Version Manager (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install --lts
nvm use --lts
nvm alias default node

# Verify installation
node --version  # Should be 18.x or higher
npm --version   # Should be 9.x or higher
```

**Global TypeScript and CDK Installation**:
```bash
# Essential global packages for CDK development
npm install -g typescript@latest
npm install -g aws-cdk@latest
npm install -g @aws-cdk/cli@latest
npm install -g ts-node
npm install -g @types/node

# Security and compliance tools
npm install -g cdk-nag
npm install -g checkov

# Verify installations
tsc --version   # Should be 5.0+
cdk --version   # Should be 2.80+
```

### VS Code Configuration for CDK TypeScript

**Essential Extensions**:
```bash
# Install via command line
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension amazonwebservices.aws-toolkit-vscode
code --install-extension ms-vscode.vscode-json
code --install-extension esbenp.prettier-vscode
code --install-extension ms-vscode.vscode-eslint
code --install-extension bridgecrew.checkov
code --install-extension ms-vscode.vscode-yaml
code --install-extension redhat.vscode-yaml
```

**Workspace Configuration** (`.vscode/settings.json`):
```json
{
  "typescript.preferences.quoteStyle": "single",
  "typescript.updateImportsOnFileMove.enabled": "always",
  "typescript.suggest.autoImports": true,
  "typescript.preferences.includePackageJsonAutoImports": "auto",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true,
    "source.fixAll.eslint": true
  },
  "aws.cdk.explorer.enabled": true,
  "aws.telemetry": false,
  "files.associations": {
    "*.yml": "yaml",
    "*.yaml": "yaml"
  },
  "yaml.schemas": {
    "https://raw.githubusercontent.com/aws/aws-cdk/main/packages/%40aws-cdk/cfnspec/spec-source/cfn.schema.json": "*.template.json"
  },
  "checkov.token": "",
  "checkov.certificate": "",
  "checkov.skipCheck": "",
  "files.exclude": {
    "**/cdk.out": true,
    "**/node_modules": true,
    "**/.git": true
  }
}
```

**Code Snippets for Security-Focused CDK** (`.vscode/security-cdk-snippets.code-snippets`):
```json
{
  "Security Stack Template": {
    "prefix": "security-stack",
    "body": [
      "import { Stack, StackProps, Tags } from 'aws-cdk-lib';",
      "import { Construct } from 'constructs';",
      "import * as iam from 'aws-cdk-lib/aws-iam';",
      "import * as ec2 from 'aws-cdk-lib/aws-ec2';",
      "",
      "export interface ${1:Security}StackProps extends StackProps {",
      "  readonly environment: 'dev' | 'staging' | 'prod';",
      "  readonly organizationName: string;",
      "  readonly complianceStandards: string[];",
      "}",
      "",
      "export class ${1:Security}Stack extends Stack {",
      "  constructor(scope: Construct, id: string, props: ${1:Security}StackProps) {",
      "    super(scope, id, props);",
      "    ",
      "    // Apply security-focused tags",
      "    Tags.of(this).add('Environment', props.environment);",
      "    Tags.of(this).add('Compliance', props.complianceStandards.join(','));",
      "    Tags.of(this).add('ManagedBy', 'CDK');",
      "    ",
      "    $0",
      "  }",
      "}"
    ],
    "description": "Create a security-focused CDK Stack"
  },
  "Secure S3 Bucket": {
    "prefix": "secure-s3",
    "body": [
      "new s3.Bucket(this, '${1:BucketName}', {",
      "  encryption: s3.BucketEncryption.S3_MANAGED,",
      "  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,",
      "  versioned: true,",
      "  lifecycleRules: [{",
      "    id: 'SecurityRetention',",
      "    noncurrentVersionExpiration: Duration.days(30),",
      "    transitions: [{",
      "      storageClass: s3.StorageClass.INTELLIGENT_TIERING,",
      "      transitionAfter: Duration.days(30)",
      "    }]",
      "  }],",
      "  removalPolicy: RemovalPolicy.${2|DESTROY,RETAIN|},",
      "  enforceSSL: true",
      "});"
    ],
    "description": "Create a security-hardened S3 bucket"
  }
}
```

---

## 🔐 Step 2: AWS Account and Security Configuration

### Multi-Account Setup Strategy

**Account Structure for Learning**:
```
Security Learning Organization
├── Management Account (Your main AWS account)
├── Security Account (Centralized security monitoring) 
├── Learning Account (Where you deploy/destroy resources)
└── Shared Services Account (Enterprise simulation)
```

**Single Account Alternative** (if you only have one AWS account):
```bash
# Create separate IAM roles to simulate multi-account
aws iam create-role --role-name CDKLearningRole --assume-role-policy-document file://trust-policy.json
aws iam create-role --role-name SecurityAuditRole --assume-role-policy-document file://trust-policy.json
```

### AWS CLI v2 Setup with SSO

**Install AWS CLI v2**:
```bash
# macOS
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version  # Should be 2.x
```

**Configure AWS SSO (Recommended)**:
```bash
# Configure SSO
aws configure sso

# Example configuration:
# SSO session name: learning-session
# SSO start URL: https://your-org.awsapps.com/start
# SSO region: us-east-1
# Account ID: 123456789012
# Role name: CDKLearningRole
# CLI default client Region: us-east-1
# CLI default output format: json
# CLI profile name: learning

# Test configuration
aws sts get-caller-identity --profile learning
```

**Alternative: Access Keys Configuration**:
```bash
# If SSO isn't available, use access keys (less secure)
aws configure --profile learning
# Enter Access Key ID, Secret Access Key, Region, Output format
```

### CDK Bootstrap for Multi-Account

**Bootstrap CDK in Learning Account**:
```bash
# Set environment variables for consistency
export CDK_DEFAULT_ACCOUNT=$(aws sts get-caller-identity --profile learning --query Account --output text)
export CDK_DEFAULT_REGION=us-east-1

# Bootstrap with custom naming for organization
cdk bootstrap aws://$CDK_DEFAULT_ACCOUNT/$CDK_DEFAULT_REGION \
  --profile learning \
  --toolkit-stack-name CDKToolkit-Learning \
  --qualifier learning

# Verify bootstrap
aws cloudformation describe-stacks \
  --stack-name CDKToolkit-Learning \
  --profile learning \
  --region us-east-1
```

---

## 🛡️ Step 3: Security and Compliance Toolchain

### Security Scanning Integration

**Checkov Configuration** (`.checkov.yaml`):
```yaml
# Checkov configuration for CDK security scanning
framework:
  - cloudformation
  - terraform
  - dockerfile
  - github_configuration

skip-check:
  # Skip checks that are handled by CDK best practices
  - CKV_AWS_18  # S3 Bucket should have access logging configured
  - CKV_AWS_21  # S3 Bucket should have versioning enabled (we handle this explicitly)

soft-fail: true
compact: true
output: cli

# Custom security standards for your organization
external-checks-dir: ./security-checks/
```

**Custom Security Checks** (`security-checks/custom_cdk_checks.py`):
```python
# Custom Checkov check for CDK TypeScript projects
from checkov.common.models.enums import TrueValue, FalseValue
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck

class CDKStackHasEnvironmentTag(BaseResourceCheck):
    def __init__(self):
        name = "Ensure CDK stacks have Environment tag"
        id = "CKV_AWS_CUSTOM_1"
        supported_resources = ['AWS::*']
        categories = []
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        tags = conf.get('Properties', {}).get('Tags', [])
        for tag in tags:
            if tag.get('Key') == 'Environment':
                return TrueValue
        return FalseValue

check = CDKStackHasEnvironmentTag()
```

### ESLint Configuration for CDK TypeScript

**ESLint Config** (`.eslintrc.js`):
```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  extends: [
    '@typescript-eslint/recommended',
    'plugin:security/recommended'
  ],
  plugins: [
    '@typescript-eslint',
    'security'
  ],
  rules: {
    // Security-focused rules for CDK
    'security/detect-hardcoded-secrets': 'error',
    'security/detect-non-literal-fs-filename': 'warn',
    'security/detect-unsafe-regex': 'error',
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-explicit-any': 'warn',
    
    // CDK-specific rules
    'prefer-const': 'error',
    'no-var': 'error',
    'eqeqeq': 'error'
  },
  env: {
    node: true,
    jest: true
  }
};
```

---

## 💰 Step 4: Cost Management and Safety Controls

### AWS Budgets Setup

**Budget Creation Script** (`scripts/setup-budgets.sh`):
```bash
#!/bin/bash
# Create learning budgets with aggressive alerts

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
EMAIL="your-email@example.com"

# Monthly budget with multiple thresholds
aws budgets create-budget \
  --account-id $ACCOUNT_ID \
  --budget '{
    "BudgetName": "CDK-Learning-Budget",
    "BudgetLimit": {
      "Amount": "50.0",
      "Unit": "USD"
    },
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST",
    "CostFilters": {
      "TagKey": ["Project"],
      "TagValue": ["CDK-Learning"]
    }
  }' \
  --notifications-with-subscribers '[
    {
      "Notification": {
        "NotificationType": "ACTUAL",
        "ComparisonOperator": "GREATER_THAN",
        "Threshold": 25
      },
      "Subscribers": [
        {
          "SubscriptionType": "EMAIL",
          "Address": "'$EMAIL'"
        }
      ]
    },
    {
      "Notification": {
        "NotificationType": "FORECASTED",
        "ComparisonOperator": "GREATER_THAN", 
        "Threshold": 80
      },
      "Subscribers": [
        {
          "SubscriptionType": "EMAIL",
          "Address": "'$EMAIL'"
        }
      ]
    }
  ]'

echo "Budget created successfully!"
```

### Automated Cleanup Scripts

**Emergency Cleanup Script** (`scripts/emergency-cleanup.sh`):
```bash
#!/bin/bash
# Nuclear option for cost control - destroys EVERYTHING

echo "🚨 EMERGENCY CLEANUP - This will destroy ALL CDK resources!"
read -p "Are you absolutely sure? Type 'DESTROY' to continue: " confirm

if [ "$confirm" != "DESTROY" ]; then
  echo "Cleanup cancelled."
  exit 1
fi

# List all CDK stacks
echo "Finding all CDK stacks..."
STACKS=$(cdk list 2>/dev/null)

if [ -z "$STACKS" ]; then
  echo "No CDK stacks found."
else
  echo "Found stacks: $STACKS"
  echo "Destroying all stacks..."
  
  # Destroy all stacks
  cdk destroy --all --force
fi

# Clean up CDK outputs
rm -rf cdk.out/

# Clean up any orphaned resources (careful with this!)
echo "Cleaning up potential orphaned resources..."

# List and optionally delete S3 buckets with learning tags
aws s3api list-buckets --query 'Buckets[?contains(Name, `cdk`) || contains(Name, `learning`)].Name' --output text | \
while read bucket; do
  if [ ! -z "$bucket" ]; then
    echo "Found potential CDK bucket: $bucket"
    read -p "Delete bucket $bucket? (y/N): " delete_bucket
    if [ "$delete_bucket" = "y" ]; then
      aws s3 rb s3://$bucket --force
    fi
  fi
done

echo "Emergency cleanup completed!"
```

---

## 🧪 Step 5: Testing and Validation Framework

### Jest Configuration for CDK Testing

**Jest Config** (`jest.config.js`):
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: [
    '**/__tests__/**/*.ts',
    '**/?(*.)+(spec|test).ts'
  ],
  transform: {
    '^.+\\.ts$': 'ts-jest'
  },
  collectCoverageFrom: [
    'lib/**/*.ts',
    '!lib/**/*.d.ts',
    '!lib/**/__tests__/**'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  setupFilesAfterEnv: ['<rootDir>/test/setup.ts']
};
```

**Test Setup File** (`test/setup.ts`):
```typescript
// Global test setup for CDK testing
import 'aws-sdk-client-mock-jest';

// Mock AWS SDK to prevent accidental real AWS calls during testing
jest.mock('aws-sdk');
jest.mock('@aws-sdk/client-s3');
jest.mock('@aws-sdk/client-iam');
jest.mock('@aws-sdk/client-ec2');

// Custom matchers for CDK constructs
expect.extend({
  toHaveResource(stack: any, resourceType: string, properties?: any) {
    const template = stack.template;
    const resources = template.Resources || {};
    
    const matches = Object.values(resources).filter((resource: any) => 
      resource.Type === resourceType &&
      (!properties || this.equals(resource.Properties, properties))
    );
    
    return {
      pass: matches.length > 0,
      message: () => `Expected stack to have resource of type ${resourceType}`
    };
  }
});
```

---

## 📋 Step 6: Environment Validation

### Validation Script

**Environment Checker** (`scripts/validate-environment.ts`):
```typescript
#!/usr/bin/env ts-node

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

interface ValidationResult {
  name: string;
  status: 'PASS' | 'FAIL' | 'WARN';
  message: string;
  details?: string;
}

class EnvironmentValidator {
  private results: ValidationResult[] = [];

  async validate(): Promise<void> {
    console.log('🔍 Validating CDK TypeScript learning environment...\n');

    // Check Node.js version
    this.checkNodeVersion();
    
    // Check TypeScript installation
    this.checkTypeScript();
    
    // Check CDK CLI
    this.checkCDKCLI();
    
    // Check AWS CLI and credentials
    await this.checkAWSConfiguration();
    
    // Check VS Code extensions
    this.checkVSCodeExtensions();
    
    // Check security tools
    this.checkSecurityTools();
    
    // Check cost controls
    this.checkCostControls();

    this.printResults();
  }

  private checkNodeVersion(): void {
    try {
      const version = execSync('node --version', { encoding: 'utf8' }).trim();
      const majorVersion = parseInt(version.substring(1).split('.')[0]);
      
      if (majorVersion >= 18) {
        this.addResult('Node.js Version', 'PASS', `${version} (>= 18.x required)`);
      } else {
        this.addResult('Node.js Version', 'FAIL', `${version} - Upgrade to 18.x or higher`);
      }
    } catch (error) {
      this.addResult('Node.js Version', 'FAIL', 'Node.js not found');
    }
  }

  private checkTypeScript(): void {
    try {
      const version = execSync('tsc --version', { encoding: 'utf8' }).trim();
      this.addResult('TypeScript', 'PASS', version);
    } catch (error) {
      this.addResult('TypeScript', 'FAIL', 'TypeScript not found - run: npm install -g typescript');
    }
  }

  private checkCDKCLI(): void {
    try {
      const version = execSync('cdk --version', { encoding: 'utf8' }).trim();
      this.addResult('CDK CLI', 'PASS', version);
    } catch (error) {
      this.addResult('CDK CLI', 'FAIL', 'CDK CLI not found - run: npm install -g aws-cdk');
    }
  }

  private async checkAWSConfiguration(): Promise<void> {
    try {
      const identity = execSync('aws sts get-caller-identity', { encoding: 'utf8' });
      const parsed = JSON.parse(identity);
      this.addResult('AWS Credentials', 'PASS', `Account: ${parsed.Account}, User: ${parsed.Arn}`);
    } catch (error) {
      this.addResult('AWS Credentials', 'FAIL', 'AWS credentials not configured - run: aws configure');
    }
  }

  private checkVSCodeExtensions(): void {
    try {
      const extensions = execSync('code --list-extensions', { encoding: 'utf8' });
      const required = [
        'amazonwebservices.aws-toolkit-vscode',
        'ms-vscode.vscode-typescript-next'
      ];
      
      const missing = required.filter(ext => !extensions.includes(ext));
      
      if (missing.length === 0) {
        this.addResult('VS Code Extensions', 'PASS', 'All required extensions installed');
      } else {
        this.addResult('VS Code Extensions', 'WARN', `Missing: ${missing.join(', ')}`);
      }
    } catch (error) {
      this.addResult('VS Code Extensions', 'WARN', 'VS Code not found or not in PATH');
    }
  }

  private checkSecurityTools(): void {
    const tools = [
      { name: 'checkov', command: 'checkov --version' },
      { name: 'cdk-nag', command: 'npm list -g cdk-nag' }
    ];

    tools.forEach(tool => {
      try {
        execSync(tool.command, { encoding: 'utf8', stdio: 'pipe' });
        this.addResult(`Security Tool: ${tool.name}`, 'PASS', 'Installed');
      } catch (error) {
        this.addResult(`Security Tool: ${tool.name}`, 'WARN', 'Not installed');
      }
    });
  }

  private checkCostControls(): void {
    // Check if budget scripts exist
    const budgetScript = path.join(process.cwd(), 'scripts', 'setup-budgets.sh');
    const cleanupScript = path.join(process.cwd(), 'scripts', 'emergency-cleanup.sh');
    
    if (fs.existsSync(budgetScript) && fs.existsSync(cleanupScript)) {
      this.addResult('Cost Control Scripts', 'PASS', 'Budget and cleanup scripts found');
    } else {
      this.addResult('Cost Control Scripts', 'WARN', 'Cost control scripts not found');
    }
  }

  private addResult(name: string, status: 'PASS' | 'FAIL' | 'WARN', message: string): void {
    this.results.push({ name, status, message });
  }

  private printResults(): void {
    console.log('\n📊 Validation Results:\n');
    
    this.results.forEach(result => {
      const icon = result.status === 'PASS' ? '✅' : result.status === 'FAIL' ? '❌' : '⚠️';
      console.log(`${icon} ${result.name}: ${result.message}`);
    });

    const failures = this.results.filter(r => r.status === 'FAIL').length;
    const warnings = this.results.filter(r => r.status === 'WARN').length;

    console.log('\n📈 Summary:');
    console.log(`✅ Passed: ${this.results.length - failures - warnings}`);
    console.log(`⚠️  Warnings: ${warnings}`);
    console.log(`❌ Failures: ${failures}`);

    if (failures === 0) {
      console.log('\n🎉 Your environment is ready for CDK TypeScript learning!');
    } else {
      console.log('\n🔧 Please fix the failures before proceeding.');
    }
  }
}

// Run validation if called directly
if (require.main === module) {
  const validator = new EnvironmentValidator();
  validator.validate();
}
```

**Make it executable**:
```bash
chmod +x scripts/validate-environment.ts
```

**Run validation**:
```bash
npm install -g ts-node  # If not already installed
./scripts/validate-environment.ts
```

---

## 🚀 Ready to Start Learning?

### Final Checklist

Before beginning Module 1, ensure you have:

- ✅ **Node.js 18+** and **TypeScript 5.0+** installed
- ✅ **AWS CLI v2** configured with valid credentials  
- ✅ **CDK CLI** installed and bootstrapped in your account
- ✅ **VS Code** configured with essential extensions
- ✅ **Security tools** (checkov, cdk-nag) installed
- ✅ **Cost controls** (budgets, cleanup scripts) in place
- ✅ **Environment validation** script passes

### Test Your Setup

**Create a test CDK project**:
```bash
mkdir cdk-test && cd cdk-test
cdk init app --language=typescript
npm run build
cdk synth
cdk deploy
cdk destroy --force
cd .. && rm -rf cdk-test
```

If this completes without errors, you're ready to begin!

---

**Next Step**: [Module 1: TypeScript Fundamentals for AWS Wizards](/learning-plans/cdk-typescript/module-1)

---

*Remember: This environment setup is designed for enterprise security workloads. Every tool and configuration will serve you throughout your CDK TypeScript mastery journey!* 🛡️