# Module 2: CDK Foundations & Mental Model Shift
*"From YAML archaeology to programmatic infrastructure poetry"*

> **Duration**: 1-2 weeks  
> **Cost**: ~$0.10-0.50/day (tear down immediately after each lab!)  
> **Prerequisites**: Module 1 completed, basic CloudFormation knowledge

---

## 🎯 Module Learning Objectives

By the end of this module, you will:
- **Understand the fundamental mental model shift** from CloudFormation to CDK
- **Master CDK constructs hierarchy** and TypeScript integration
- **Navigate CDK CLI** like a seasoned infrastructure developer
- **Build and deploy** your first multi-stack CDK TypeScript application
- **Set up GitHub Actions** for automated CDK deployment pipelines

---

## 📚 Core Lessons

### Lesson 2.1: CDK vs CloudFormation Mindset Shift
*"Rewiring your brain from YAML to TypeScript"*

#### The Great Mental Model Migration

**CloudFormation Thinking** → **CDK Thinking**

| CloudFormation Approach | CDK TypeScript Approach |
|-------------------------|-------------------------|
| Static YAML templates | Dynamic TypeScript code |
| Copy-paste configurations | Reusable construct classes |
| Manual parameter passing | Type-safe props interfaces |
| Limited logic capabilities | Full programming power |
| Verbose resource definitions | Intelligent defaults |
| Template drift concerns | Code-driven consistency |

#### From Template Engineering to Software Engineering

**Old Way (CloudFormation)**:
```yaml
# Repetitive, error-prone, limited logic
Resources:
  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub "${Environment}-vpc"
        - Key: Environment  
          Value: !Ref Environment
        - Key: Project
          Value: !Ref ProjectName
  
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: !Sub "${Environment}-private-subnet-1"
        - Key: Environment
          Value: !Ref Environment
  # ... 50 more lines of repetitive subnet definitions
```

**New Way (CDK TypeScript)**:
```typescript
// Concise, reusable, intelligent
export class NetworkingStack extends Stack {
  public readonly vpc: Vpc;
  
  constructor(scope: Construct, id: string, props: NetworkingStackProps) {
    super(scope, id, props);
    
    // CDK automatically creates subnets across AZs with best practices
    this.vpc = new Vpc(this, 'VPC', {
      maxAzs: 3,
      natGateways: props.environment === 'prod' ? 3 : 1,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'public',
          subnetType: SubnetType.PUBLIC,
        },
        {
          cidrMask: 24, 
          name: 'private',
          subnetType: SubnetType.PRIVATE_WITH_EGRESS,
        }
      ]
    });
    
    // Automatic tagging through CDK aspects
    Tags.of(this).add('Environment', props.environment);
    Tags.of(this).add('Project', props.projectName);
  }
}
```

#### Key Mental Shifts

1. **From Configuration to Programming**
   - CloudFormation: "Configure this specific resource"
   - CDK: "Build this type of infrastructure pattern"

2. **From Static to Dynamic** 
   - CloudFormation: Templates are fixed at authoring time
   - CDK: Infrastructure adapts based on runtime conditions

3. **From Copy-Paste to Composition**
   - CloudFormation: Copy similar resources, modify slightly
   - CDK: Create reusable constructs, compose into larger patterns

4. **From Parameter Hell to Type Safety**
   - CloudFormation: String parameters passed around blindly
   - CDK: TypeScript interfaces ensure correctness at compile time

#### 🛠️ Hands-On Lab 2.1: Mental Model Migration

**Challenge**: Convert a CloudFormation template to CDK TypeScript

**Given CloudFormation Template** (common security group pattern):
```yaml
Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
  
Resources:
  WebSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for web servers
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443  
          CidrIp: 0.0.0.0/0
        - !If 
          - IsDev
          - IpProtocol: tcp
            FromPort: 22
            ToPort: 22
            CidrIp: 0.0.0.0/0
          - !Ref AWS::NoValue
```

**Your Mission**: Convert to CDK TypeScript with these improvements:
- Type-safe environment handling
- Conditional logic using TypeScript
- Reusable security group patterns
- Better default configurations

**Expected CDK Output**:
```typescript
interface SecurityStackProps extends StackProps {
  readonly environment: 'dev' | 'staging' | 'prod';
  readonly vpc: IVpc;
  readonly allowSshAccess?: boolean;
}

export class SecurityStack extends Stack {
  public readonly webSecurityGroup: SecurityGroup;
  
  constructor(scope: Construct, id: string, props: SecurityStackProps) {
    super(scope, id, props);
    
    this.webSecurityGroup = new SecurityGroup(this, 'WebSecurityGroup', {
      vpc: props.vpc,
      description: 'Security group for web servers',
      allowAllOutbound: false // Security best practice
    });
    
    // HTTP/HTTPS access
    this.webSecurityGroup.addIngressRule(
      Peer.anyIpv4(),
      Port.tcp(80),
      'HTTP access'
    );
    
    this.webSecurityGroup.addIngressRule(
      Peer.anyIpv4(), 
      Port.tcp(443),
      'HTTPS access'
    );
    
    // Conditional SSH access - TypeScript way
    if (props.environment === 'dev' || props.allowSshAccess) {
      this.webSecurityGroup.addIngressRule(
        Peer.anyIpv4(),
        Port.tcp(22),
        'SSH access for development'
      );
    }
  }
}
```

**Success Criteria**:
- CDK code is more concise than original CloudFormation
- Type safety prevents invalid environment values
- Logic is clearer and more maintainable
- Deploys successfully with `cdk deploy`

---

### Lesson 2.2: Constructs Hierarchy & TypeScript Integration
*"Understanding the CDK construct universe"*

#### The Three Levels of CDK Constructs

**L1 Constructs (CFN Resources)** - Direct CloudFormation mapping:
```typescript
// L1 - Raw CloudFormation resource
const bucket = new s3.CfnBucket(this, 'MyBucket', {
  bucketName: 'my-raw-bucket',
  versioningConfiguration: {
    status: 'Enabled'
  }
});
```

**L2 Constructs (AWS Constructs)** - Opinionated, best-practice defaults:
```typescript
// L2 - AWS construct with smart defaults
const bucket = new s3.Bucket(this, 'MyBucket', {
  versioned: true,
  encryption: s3.BucketEncryption.S3_MANAGED,
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
  removalPolicy: RemovalPolicy.DESTROY // For learning only!
});
```

**L3 Constructs (Patterns)** - High-level architectural patterns:
```typescript
// L3 - Complete architectural pattern
const website = new cloudfront.Distribution(this, 'Website', {
  defaultBehavior: {
    origin: new origins.S3Origin(bucket),
    viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
  },
  errorResponses: [{
    httpStatus: 404,
    responseHttpStatus: 200,
    responsePagePath: '/index.html'
  }]
});
```

#### TypeScript Integration with Construct Props

**Props Interface Design Patterns**:
```typescript
// Base props pattern
interface BaseConstructProps {
  readonly environment: Environment;
  readonly projectName: string;
}

// Extending for specific constructs
interface DatabaseConstructProps extends BaseConstructProps {
  readonly vpc: IVpc;
  readonly instanceClass?: InstanceClass; // Optional with default
  readonly multiAz?: boolean;
  readonly backupRetention?: Duration;
}

// Props with unions for type safety
interface ApiConstructProps extends BaseConstructProps {
  readonly apiType: 'rest' | 'http' | 'websocket';
  readonly authorizers?: ApiAuthorizer[];
  readonly corsConfig?: CorsOptions;
}

// Generic props for reusable patterns
interface MonitoredConstructProps<T> extends BaseConstructProps {
  readonly resourceConfig: T;
  readonly alarmThresholds: AlarmThresholds;
  readonly dashboardConfig?: DashboardConfig;
}
```

#### Construct Composition Patterns

**Building Reusable Security Constructs**:
```typescript
export interface SecureWebAppProps {
  readonly domainName: string;
  readonly certificateArn: string;
  readonly allowedOrigins: string[];
  readonly environment: Environment;
}

export class SecureWebApp extends Construct {
  public readonly distribution: CloudFrontDistribution;
  public readonly bucket: Bucket;
  public readonly oai: OriginAccessIdentity;
  
  constructor(scope: Construct, id: string, props: SecureWebAppProps) {
    super(scope, id);
    
    // S3 bucket with security defaults
    this.bucket = new Bucket(this, 'ContentBucket', {
      encryption: BucketEncryption.S3_MANAGED,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      versioned: true,
      lifecycleRules: [{
        id: 'DeleteOldVersions',
        noncurrentVersionExpiration: Duration.days(30)
      }]
    });
    
    // Origin Access Identity for CloudFront
    this.oai = new OriginAccessIdentity(this, 'OAI', {
      comment: `OAI for ${props.domainName}`
    });
    
    this.bucket.grantRead(this.oai);
    
    // CloudFront with security headers
    this.distribution = new CloudFrontDistribution(this, 'Distribution', {
      defaultBehavior: {
        origin: new S3Origin(this.bucket, {
          originAccessIdentity: this.oai
        }),
        viewerProtocolPolicy: ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        responseHeadersPolicy: this.createSecurityHeadersPolicy()
      },
      domainNames: [props.domainName],
      certificate: Certificate.fromCertificateArn(
        this, 'Certificate', props.certificateArn
      ),
      priceClass: PriceClass.PRICE_CLASS_100
    });
  }
  
  private createSecurityHeadersPolicy(): ResponseHeadersPolicy {
    return new ResponseHeadersPolicy(this, 'SecurityHeaders', {
      securityHeadersBehavior: {
        contentTypeOptions: { override: true },
        frameOptions: { frameOption: HeadersFrameOption.DENY, override: true },
        referrerPolicy: { 
          referrerPolicy: HeadersReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN,
          override: true 
        },
        strictTransportSecurity: {
          accessControlMaxAge: Duration.seconds(31536000),
          includeSubdomains: true,
          override: true
        }
      }
    });
  }
}
```

#### 🛠️ Hands-On Lab 2.2: Build Your First Construct Library

**Challenge**: Create a reusable "SecurityBaseline" construct

**Requirements**:
1. Encapsulates common security configurations
2. Uses TypeScript interfaces for type-safe props
3. Demonstrates L1, L2, and L3 construct usage
4. Includes proper tagging and documentation

```typescript
export interface SecurityBaselineProps {
  readonly organizationName: string;
  readonly environment: 'dev' | 'staging' | 'prod';
  readonly complianceStandards: ('CIS' | 'SOC2' | 'PCI')[];
  readonly alertingEmail: string;
  readonly enableCloudTrail?: boolean;
  readonly enableConfig?: boolean;
  readonly enableSecurityHub?: boolean;
}

export class SecurityBaseline extends Construct {
  public readonly cloudTrail?: CloudTrail;
  public readonly configRecorder?: ConfigurationRecorder;
  public readonly securityHub?: CfnHub;
  public readonly alertTopic: Topic;
  
  constructor(scope: Construct, id: string, props: SecurityBaselineProps) {
    super(scope, id);
    
    // Your implementation here:
    // 1. Create SNS topic for security alerts
    // 2. Conditionally enable CloudTrail
    // 3. Set up AWS Config if requested
    // 4. Enable Security Hub with specified standards
    // 5. Apply consistent tagging
    // 6. Create CloudWatch alarms for security events
  }
  
  private setupCloudTrail(props: SecurityBaselineProps): CloudTrail {
    // Implementation
  }
  
  private setupConfig(props: SecurityBaselineProps): ConfigurationRecorder {
    // Implementation  
  }
  
  private setupSecurityHub(props: SecurityBaselineProps): CfnHub {
    // Implementation
  }
}
```

**Success Criteria**:
- Construct can be instantiated with type-safe props
- Combines L1, L2, and L3 constructs appropriately
- Conditional logic works correctly
- Produces valid CloudFormation when synthesized
- Can be imported and used by other stacks

---

### Lesson 2.3: Apps, Stacks, and Cross-Stack References
*"Orchestrating infrastructure at scale"*

#### CDK Application Architecture

**App-Level Organization**:
```typescript
// bin/app.ts - Application entry point
import { App, Environment } from 'aws-cdk-lib';
import { NetworkingStack } from '../lib/stacks/networking-stack';
import { SecurityStack } from '../lib/stacks/security-stack';
import { ApplicationStack } from '../lib/stacks/application-stack';

const app = new App();

// Environment configuration
const environments: Record<string, Environment> = {
  dev: {
    account: '123456789012',
    region: 'us-east-1'
  },
  prod: {
    account: '123456789013', 
    region: 'us-east-1'
  }
};

// Deploy to multiple environments
Object.entries(environments).forEach(([envName, env]) => {
  // Foundational networking
  const networking = new NetworkingStack(app, `${envName}-networking`, {
    env,
    environment: envName as Environment
  });
  
  // Security baseline
  const security = new SecurityStack(app, `${envName}-security`, {
    env,
    vpc: networking.vpc,
    environment: envName as Environment
  });
  
  // Application infrastructure
  const application = new ApplicationStack(app, `${envName}-app`, {
    env,
    vpc: networking.vpc,
    securityGroup: security.applicationSecurityGroup,
    environment: envName as Environment
  });
  
  // Stack dependencies
  security.addDependency(networking);
  application.addDependency(security);
});
```

#### Cross-Stack Reference Patterns

**Type-Safe Cross-Stack Communication**:
```typescript
// networking-stack.ts
export class NetworkingStack extends Stack {
  public readonly vpc: IVpc;
  public readonly privateSubnets: ISubnet[];
  public readonly publicSubnets: ISubnet[];
  
  constructor(scope: Construct, id: string, props: NetworkingStackProps) {
    super(scope, id, props);
    
    this.vpc = new Vpc(this, 'VPC', {
      maxAzs: 3,
      subnetConfiguration: [
        {
          name: 'public',
          subnetType: SubnetType.PUBLIC,
          cidrMask: 24,
        },
        {
          name: 'private',
          subnetType: SubnetType.PRIVATE_WITH_EGRESS,
          cidrMask: 24,
        }
      ]
    });
    
    this.privateSubnets = this.vpc.privateSubnets;
    this.publicSubnets = this.vpc.publicSubnets;
    
    // Export values for cross-stack reference
    new CfnOutput(this, 'VpcId', {
      value: this.vpc.vpcId,
      exportName: `${this.stackName}-vpc-id`
    });
  }
}

// security-stack.ts  
export class SecurityStack extends Stack {
  public readonly applicationSecurityGroup: SecurityGroup;
  public readonly databaseSecurityGroup: SecurityGroup;
  
  constructor(scope: Construct, id: string, props: SecurityStackProps) {
    super(scope, id, props);
    
    // Reference VPC from networking stack
    this.applicationSecurityGroup = new SecurityGroup(this, 'AppSG', {
      vpc: props.vpc, // Type-safe reference
      description: 'Security group for application tier'
    });
    
    this.databaseSecurityGroup = new SecurityGroup(this, 'DatabaseSG', {
      vpc: props.vpc,
      description: 'Security group for database tier'
    });
    
    // Allow app tier to connect to database tier
    this.databaseSecurityGroup.addIngressRule(
      this.applicationSecurityGroup,
      Port.tcp(5432),
      'Allow application access to database'
    );
  }
}
```

#### Environment-Specific Configuration

**Configuration Management Pattern**:
```typescript
// config/environment-config.ts
export interface EnvironmentConfig {
  readonly environmentName: string;
  readonly account: string;
  readonly region: string;
  readonly vpcCidr: string;
  readonly natGateways: number;
  readonly databaseConfig: {
    readonly instanceClass: string;
    readonly multiAz: boolean;
    readonly backupRetention: number;
  };
  readonly monitoringConfig: {
    readonly detailedMonitoring: boolean;
    readonly logRetention: number;
  };
}

export const ENVIRONMENT_CONFIGS: Record<string, EnvironmentConfig> = {
  dev: {
    environmentName: 'dev',
    account: '123456789012',
    region: 'us-east-1', 
    vpcCidr: '10.0.0.0/16',
    natGateways: 1,
    databaseConfig: {
      instanceClass: 'db.t3.micro',
      multiAz: false,
      backupRetention: 7
    },
    monitoringConfig: {
      detailedMonitoring: false,
      logRetention: 7
    }
  },
  prod: {
    environmentName: 'prod',
    account: '123456789013',
    region: 'us-east-1',
    vpcCidr: '10.1.0.0/16', 
    natGateways: 3,
    databaseConfig: {
      instanceClass: 'db.r5.large',
      multiAz: true,
      backupRetention: 30
    },
    monitoringConfig: {
      detailedMonitoring: true,
      logRetention: 30
    }
  }
};

// Usage in stacks
export class DatabaseStack extends Stack {
  constructor(scope: Construct, id: string, props: DatabaseStackProps) {
    super(scope, id, props);
    
    const config = ENVIRONMENT_CONFIGS[props.environment];
    
    new DatabaseInstance(this, 'Database', {
      engine: DatabaseInstanceEngine.postgres({
        version: PostgresEngineVersion.VER_13_7
      }),
      instanceType: InstanceType.of(
        InstanceClass.BURSTABLE3, 
        InstanceSize.MICRO
      ),
      multiAz: config.databaseConfig.multiAz,
      backupRetention: Duration.days(config.databaseConfig.backupRetention),
      vpc: props.vpc
    });
  }
}
```

#### 🛠️ Hands-On Lab 2.3: Multi-Stack Architecture

**Challenge**: Build a complete multi-stack application with proper dependencies

**Architecture Requirements**:
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Networking      │    │ Security        │    │ Application     │
│ Stack           │    │ Stack           │    │ Stack           │
│                 │    │                 │    │                 │
│ • VPC           │───▶│ • Security      │───▶│ • Lambda        │
│ • Subnets       │    │   Groups        │    │ • API Gateway   │
│ • NAT Gateways  │    │ • NACLs         │    │ • DynamoDB      │
│ • Route Tables  │    │ • WAF Rules     │    │ • CloudFront    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Your Mission**:
1. Create three separate stacks with proper TypeScript interfaces
2. Implement cross-stack references using CDK patterns (not CloudFormation exports)
3. Support multiple environments (dev/prod) with different configurations
4. Include proper dependency management
5. Add comprehensive tagging strategy

**Expected Structure**:
```typescript
// interfaces/stack-props.ts
export interface BaseStackProps extends StackProps {
  readonly environment: 'dev' | 'staging' | 'prod';
  readonly projectName: string;
}

export interface SecurityStackProps extends BaseStackProps {
  readonly vpc: IVpc;
}

export interface ApplicationStackProps extends BaseStackProps {
  readonly vpc: IVpc;
  readonly securityGroup: ISecurityGroup;
}

// Implementation files:
// lib/stacks/networking-stack.ts
// lib/stacks/security-stack.ts  
// lib/stacks/application-stack.ts
// bin/app.ts
```

**Success Criteria**:
- All stacks compile without TypeScript errors
- Cross-stack references work correctly
- `cdk synth` produces valid CloudFormation for all stacks
- `cdk deploy --all` deploys in correct dependency order
- Environment-specific configurations apply correctly
- `cdk destroy --all` cleans up all resources

---

### Lesson 2.4: CDK CLI Mastery and Deployment Strategies
*"Becoming one with the command line"*

#### Essential CDK CLI Commands

**Development Workflow Commands**:
```bash
# Project initialization and setup
cdk init app --language=typescript
cdk bootstrap # One-time setup per account/region

# Development commands
cdk synth                    # Generate CloudFormation
cdk synth MyStack           # Generate specific stack
cdk diff                    # Show differences
cdk diff MyStack           # Diff specific stack

# Deployment commands
cdk deploy                  # Deploy all stacks
cdk deploy MyStack         # Deploy specific stack
cdk deploy --all          # Deploy all stacks
cdk deploy --require-approval never  # Skip approval prompts

# Cleanup commands
cdk destroy                # Destroy all stacks  
cdk destroy MyStack       # Destroy specific stack
cdk destroy --force       # Skip confirmation prompts

# Utility commands
cdk ls                    # List all stacks
cdk context              # Show context values
cdk doctor              # Diagnose common issues
cdk docs                # Open CDK documentation
```

**Advanced CLI Usage**:
```bash
# Environment-specific deployments
cdk deploy --profile prod-profile
cdk deploy --context environment=prod
cdk deploy MyStack --parameters key=value

# Debugging and troubleshooting
cdk synth --verbose
cdk deploy --debug
cdk deploy --trace

# Output and formatting
cdk synth --output ./cdk.out
cdk ls --long
cdk diff --context-lines=3

# Parallel deployments
cdk deploy Stack1 Stack2 Stack3 --concurrency=3

# Rollback and recovery
cdk deploy --rollback
cdk deploy --previous-parameters
```

#### GitHub Actions Integration

**Basic CDK Deployment Workflow**:
```yaml
# .github/workflows/cdk-deploy.yml
name: CDK Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
        aws-region: us-east-1
        
    - name: Run TypeScript compilation
      run: npm run build
      
    - name: Run CDK diff
      run: npx cdk diff
      if: github.event_name == 'pull_request'
      
    - name: Deploy CDK stacks
      run: npx cdk deploy --all --require-approval never
      if: github.ref == 'refs/heads/main'
      
    - name: Run post-deployment tests
      run: npm run test:integration
      if: github.ref == 'refs/heads/main'
```

**Multi-Environment Deployment Strategy**:
```yaml
# .github/workflows/multi-env-deploy.yml
name: Multi-Environment Deploy

on:
  push:
    branches: [main, develop]

jobs:
  deploy-dev:
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: development
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Development
        run: |
          npm ci
          npm run build
          npx cdk deploy --context environment=dev --all --require-approval never
        env:
          AWS_ROLE_ARN: ${{ secrets.DEV_AWS_ROLE_ARN }}
          
  deploy-prod:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    needs: [test-and-validate]
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Production
        run: |
          npm ci
          npm run build
          npx cdk deploy --context environment=prod --all --require-approval never
        env:
          AWS_ROLE_ARN: ${{ secrets.PROD_AWS_ROLE_ARN }}
```

#### Advanced Deployment Patterns

**Blue/Green Deployment Setup**:
```typescript
// Advanced deployment configuration
export class BlueGreenDeploymentStack extends Stack {
  constructor(scope: Construct, id: string, props: BlueGreenProps) {
    super(scope, id, props);
    
    // Create both blue and green environments
    const blueEnvironment = this.createEnvironment('blue', props);
    const greenEnvironment = this.createEnvironment('green', props);
    
    // Route 53 weighted routing for traffic shifting
    new ARecord(this, 'BlueGreenRecord', {
      zone: props.hostedZone,
      recordName: props.domainName,
      target: RecordTarget.fromAlias(
        new Route53Targets.LoadBalancerTarget(
          props.activeEnvironment === 'blue' 
            ? blueEnvironment.loadBalancer 
            : greenEnvironment.loadBalancer
        )
      )
    });
  }
  
  private createEnvironment(color: string, props: BlueGreenProps) {
    // Implementation for environment creation
  }
}
```

#### 🛠️ Hands-On Lab 2.4: Complete CI/CD Pipeline

**Challenge**: Set up a production-ready CDK deployment pipeline

**Requirements**:
1. GitHub Actions workflow for CDK deployment
2. Multi-environment support (dev/staging/prod)
3. Automated testing and validation
4. Security scanning integration
5. Cost estimation and approval gates

**Your Mission**:

1. **Set up OIDC Authentication**:
```bash
# Create OIDC provider for GitHub Actions
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

2. **Create IAM Role for GitHub Actions**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USERNAME/YOUR_REPO_NAME:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

3. **Implement Workflow with Security Gates**:
```yaml
# .github/workflows/secure-cdk-deploy.yml
name: Secure CDK Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: cloudformation
          
  cost-estimation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Infracost
        uses: infracost/actions/setup@v2
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}
      - name: Generate cost estimate
        run: |
          npm ci && npm run build
          npx cdk synth
          infracost breakdown --path cdk.out/ --format json --out-file cost.json
          
  deploy:
    needs: [security-scan, cost-estimation]
    runs-on: ubuntu-latest
    steps:
      # Your deployment implementation
```

**Success Criteria**:
- GitHub Actions workflow runs without errors
- OIDC authentication works correctly
- Security scanning passes
- Cost estimation generates accurate reports
- Multi-environment deployment works
- Rollback procedures are tested and functional

---

## 📋 Module 2 Assessment

### Knowledge Check Quiz

**Question 1**: What's the main advantage of CDK constructs over CloudFormation resources?
- a) They're faster to deploy
- b) They provide intelligent defaults and best practices ✓
- c) They cost less to run
- d) They support more AWS services

**Question 2**: Which construct level provides the highest-level architectural patterns?
- a) L1 (CFN Resources)
- b) L2 (AWS Constructs) 
- c) L3 (Patterns) ✓
- d) L4 (Custom)

**Question 3**: What's the recommended way to pass data between CDK stacks?
- a) CloudFormation exports
- b) Direct property references ✓
- c) Parameter Store
- d) Environment variables

### Practical Assessment: Multi-Stack Security Platform

**Capstone Project**: Build a complete security monitoring platform using multiple CDK stacks.

**Requirements**:
- **Networking Stack**: VPC with public/private subnets
- **Security Stack**: Security groups, NACLs, WAF rules
- **Monitoring Stack**: CloudWatch dashboards, alarms, SNS notifications  
- **Application Stack**: Lambda functions, API Gateway, DynamoDB

**Architecture Diagram**:
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Networking      │    │ Security        │    │ Monitoring      │    │ Application     │
│ Stack           │    │ Stack           │    │ Stack           │    │ Stack           │
│                 │    │                 │    │                 │    │                 │
│ • VPC           │───▶│ • Security      │───▶│ • CloudWatch    │───▶│ • API Gateway   │
│ • Subnets       │    │   Groups        │    │ • Dashboards    │    │ • Lambda        │
│ • Route Tables  │    │ • WAF Rules     │    │ • Alarms        │    │ • DynamoDB      │
│ • NAT Gateways  │    │ • NACLs         │    │ • SNS Topics    │    │ • S3 Buckets    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

**TypeScript Implementation Requirements**:
```typescript
// Must demonstrate these CDK TypeScript concepts:
interface ProjectProps {
  readonly environment: 'dev' | 'staging' | 'prod';
  readonly projectName: string;
  readonly alertEmail: string;
}

// 1. Custom construct composition
export class SecurityMonitoringPlatform extends Construct {
  // Your implementation
}

// 2. Cross-stack type-safe references
export class MonitoringStack extends Stack {
  constructor(scope: Construct, id: string, props: MonitoringStackProps) {
    // Must reference security stack resources with TypeScript types
  }
}

// 3. Environment-specific configuration
export class ApplicationStack extends Stack {
  constructor(scope: Construct, id: string, props: ApplicationStackProps) {
    // Must adapt configuration based on environment
  }
}

// 4. GitHub Actions deployment
// Must include complete CI/CD workflow
```

**Validation Criteria**:
- ✅ All stacks compile without TypeScript errors
- ✅ Cross-stack references use CDK patterns (not CloudFormation exports)
- ✅ Environment-specific configuration works correctly
- ✅ GitHub Actions deployment succeeds
- ✅ Security scanning passes
- ✅ Resources deploy and function correctly
- ✅ Cleanup destroys all resources successfully

**💰 Cost Warning**: This will cost ~$2-5/day while running. Deploy → test → screenshot results → `cdk destroy --all --force` immediately!

---

## 🚀 Ready for Module 3?

**Before proceeding, ensure you can:**
- ✅ Explain the mental model shift from CloudFormation to CDK
- ✅ Use L1, L2, and L3 constructs appropriately
- ✅ Build multi-stack applications with type-safe cross-stack references
- ✅ Deploy CDK applications via GitHub Actions
- ✅ Navigate CDK CLI commands efficiently

**Next Up**: [Module 3: Advanced CDK TypeScript Patterns](/learning-plans/cdk-typescript/module-3)

---

## 💡 Reflection Prompts

1. **How has your approach to infrastructure design changed from CloudFormation to CDK?**

2. **What TypeScript features make CDK development more productive than YAML templating?**

3. **How would you explain the value of the constructs hierarchy to a fellow CloudFormation expert?**

4. **What deployment strategies would you recommend for a production CDK application?**

---

*You've successfully made the mental leap from static templates to dynamic infrastructure code! The YAML days are behind you - now you're thinking in constructs, composition, and type safety. Onward to advanced patterns! 🚀*