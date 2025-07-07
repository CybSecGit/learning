# CDK TypeScript Debugging Guide
*"When your infrastructure code fights back: A survival guide for the digitally wounded"*

> **Essential Reading**: For when your CDK deployment fails spectacularly and you need to figure out why without having a mental breakdown

---

## 🚨 Emergency Triage: "My CDK Is On Fire"

### The 5-Minute Emergency Response Protocol

When everything is broken and people are asking questions you can't answer:

```bash
# 1. Stop the bleeding - check what's actually deployed
cdk list --long
aws cloudformation list-stacks --stack-status-filter CREATE_FAILED UPDATE_FAILED ROLLBACK_FAILED

# 2. Get the failure details
cdk deploy --verbose --debug MyStack 2>&1 | tee debug-output.log

# 3. Check CloudFormation events for the real story
aws cloudformation describe-stack-events --stack-name MyStack --query 'StackEvents[?ResourceStatus==`CREATE_FAILED` || ResourceStatus==`UPDATE_FAILED`]'

# 4. Emergency rollback if needed
cdk destroy MyStack --force  # Nuclear option
```

**The CDK Debugging Hierarchy of Needs:**
1. Can you breathe? (Is your AWS account working?)
2. Can you deploy anything? (Basic CDK functionality)
3. Can you deploy your specific stack? (Stack-specific issues)
4. Does your deployed infrastructure work? (Runtime issues)
5. Is it performant and cost-effective? (Optimization issues)

---

## 🔍 Systematic Debugging Approach

### Phase 1: Pre-Flight Checks
*"Before you blame CDK, make sure you're not the problem"*

```typescript
// Create this debug helper - it's saved me countless hours
export class CDKDebugHelper {
  static validateEnvironment(): void {
    console.log('🔍 CDK Environment Debug Check');
    console.log('Node Version:', process.version);
    console.log('CDK Version:', require('@aws-cdk/core/package.json').version);
    console.log('AWS Region:', process.env.CDK_DEFAULT_REGION || 'Not set');
    console.log('AWS Account:', process.env.CDK_DEFAULT_ACCOUNT || 'Not set');
    
    // Check for common gotchas
    if (!process.env.CDK_DEFAULT_REGION) {
      console.warn('⚠️  CDK_DEFAULT_REGION not set - this causes mysterious failures');
    }
    
    if (!process.env.CDK_DEFAULT_ACCOUNT) {
      console.warn('⚠️  CDK_DEFAULT_ACCOUNT not set - cross-account stuff will break');
    }
  }
  
  static async validateAWSCredentials(): Promise<void> {
    try {
      const sts = new AWS.STS();
      const identity = await sts.getCallerIdentity().promise();
      console.log('✅ AWS Credentials valid for:', identity.Arn);
    } catch (error) {
      console.error('❌ AWS Credentials invalid:', error.message);
      throw new Error('Fix your AWS credentials first');
    }
  }
  
  static validateStack(stack: Stack): void {
    console.log(`🔍 Validating stack: ${stack.stackName}`);
    
    // Check for common anti-patterns
    const templateJson = JSON.stringify(stack.toCloudFormation());
    
    if (templateJson.includes('"Ref":"AWS::NoValue"')) {
      console.warn('⚠️  Found AWS::NoValue references - conditional logic might be broken');
    }
    
    if (templateJson.length > 460800) { // 450KB limit
      console.error('❌ Template too large for CloudFormation');
    }
    
    // Check for hardcoded values that will cause conflicts
    const hardcodedPatterns = [
      /"BucketName":"[^{]/,
      /"FunctionName":"[^{]/,
      /"QueueName":"[^{]/
    ];
    
    hardcodedPatterns.forEach(pattern => {
      if (pattern.test(templateJson)) {
        console.warn('⚠️  Found hardcoded resource names - will conflict across environments');
      }
    });
  }
}
```

### Phase 2: Compilation Issues
*"When TypeScript and CDK have relationship problems"*

#### Common TypeScript + CDK Compilation Errors

**Error: "Cannot find module '@aws-cdk/...'"**
```bash
# The nuclear option that actually works
rm -rf node_modules package-lock.json
npm install

# If that doesn't work, check version compatibility
npm ls @aws-cdk/core
npm ls aws-cdk-lib

# For CDK v2 (recommended), use aws-cdk-lib
npm install aws-cdk-lib@latest constructs@latest
```

**Error: "Property 'X' does not exist on type 'Y'"**
```typescript
// ❌ This breaks because of version mismatches
import { Function } from '@aws-cdk/aws-lambda';  // CDK v1
import { Function } from 'aws-cdk-lib/aws-lambda';  // CDK v2

// ✅ Always check your imports match your CDK version
import { aws_lambda as lambda } from 'aws-cdk-lib';  // CDK v2 way
```

**Error: "jsii.errors.JSIIError: Expected object reference, got [object]"**
```typescript
// ❌ This JSII serialization error is usually caused by:
const props = {
  vpc: vpc,
  subnet: subnet.subnets[0],  // Array access in props
  config: someComplexObject   // Non-serializable object
};

// ✅ Fix by ensuring clean object structure
const props: MyConstructProps = {
  vpc: vpc,
  subnetId: subnet.subnets[0].subnetId,  // Use IDs, not objects
  configParam: someComplexObject.simpleProperty
};
```

### Phase 3: Synthesis Issues
*"When CDK can compile but can't create CloudFormation"*

#### The `cdk synth` Debug Workflow

```bash
# Enable all debug output
export CDK_DEBUG=true
cdk synth --verbose --debug MyStack > synth-output.json 2> synth-errors.log

# Check the generated CloudFormation
cat cdk.out/MyStack.template.json | jq .

# Look for circular dependencies
cdk synth --verbose 2>&1 | grep -i "circular\|dependency"

# Check asset bundling issues
ls -la cdk.out/asset.*
```

#### Common Synthesis Errors and Solutions

**Circular Dependency Errors:**
```typescript
// ❌ This creates circular dependency hell
export class DatabaseStack extends Stack {
  public readonly database: rds.Database;
  
  constructor(scope: Construct, id: string, props: { vpc: ec2.IVpc }) {
    super(scope, id);
    this.database = new rds.Database(this, 'DB', { vpc: props.vpc });
  }
}

export class LambdaStack extends Stack {
  constructor(scope: Construct, id: string, props: { database: rds.IDatabase, vpc: ec2.IVpc }) {
    super(scope, id);
    
    const fn = new lambda.Function(this, 'Function', {
      // This creates a circular dependency if the database references the lambda
      environment: {
        DB_ENDPOINT: props.database.instanceEndpoint.hostname
      }
    });
    
    // Don't do this - creates circular dependency
    props.database.connections.allowDefaultPortFrom(fn);
  }
}

// ✅ Break circular dependencies with proper layering
export class DatabaseStack extends Stack {
  public readonly database: rds.Database;
  public readonly securityGroup: ec2.SecurityGroup;
  
  constructor(scope: Construct, id: string, props: { vpc: ec2.IVpc }) {
    super(scope, id);
    
    // Create security group that lambda can reference
    this.securityGroup = new ec2.SecurityGroup(this, 'DatabaseSG', {
      vpc: props.vpc,
      allowAllOutbound: false
    });
    
    this.database = new rds.Database(this, 'DB', {
      vpc: props.vpc,
      securityGroups: [this.securityGroup]
    });
  }
}

export class LambdaStack extends Stack {
  constructor(scope: Construct, id: string, props: { 
    database: rds.IDatabase, 
    databaseSG: ec2.ISecurityGroup,
    vpc: ec2.IVpc 
  }) {
    super(scope, id);
    
    const fn = new lambda.Function(this, 'Function', {
      environment: {
        DB_ENDPOINT: props.database.instanceEndpoint.hostname
      }
    });
    
    // Allow lambda to connect to database
    props.databaseSG.addIngressRule(
      ec2.Peer.securityGroupId(fn.connections.securityGroups[0].securityGroupId),
      ec2.Port.tcp(5432)
    );
  }
}
```

**Asset Bundling Failures:**
```typescript
// ❌ Common asset issues
const fn = new lambda.Function(this, 'Function', {
  code: lambda.Code.fromAsset('src/lambda'),  // Directory doesn't exist
  handler: 'index.handler'
});

// ✅ Debug asset bundling
const fn = new lambda.Function(this, 'Function', {
  code: lambda.Code.fromAsset('src/lambda', {
    bundling: {
      image: lambda.Runtime.NODEJS_18_X.bundlingImage,
      command: [
        'bash', '-c', [
          'echo "=== Debug: Listing source directory ==="',
          'ls -la /asset-input',
          'echo "=== Debug: Installing dependencies ==="',
          'cd /asset-input && npm install',
          'echo "=== Debug: Building ==="',
          'npm run build',
          'echo "=== Debug: Listing output ==="',
          'ls -la /asset-output',
          'cp -r . /asset-output'
        ].join(' && ')
      ]
    }
  }),
  handler: 'index.handler'
});
```

### Phase 4: Deployment Issues
*"When CloudFormation decides to have opinions"*

#### The Deployment Debug Arsenal

```bash
# Enable CloudFormation debug mode
export AWS_CLI_FILE_ENCODING=UTF-8
aws configure set cli_follow_urlparam false

# Deploy with maximum verbosity
cdk deploy --verbose --debug --require-approval never MyStack 2>&1 | tee deploy-debug.log

# Watch CloudFormation events in real-time
aws cloudformation describe-stack-events --stack-name MyStack \
  --query 'StackEvents[0:10].[Timestamp,ResourceStatus,ResourceType,LogicalResourceId,ResourceStatusReason]' \
  --output table

# For failed deployments, get the real error
aws logs filter-log-events --log-group-name /aws/lambda/MyFunction --start-time $(date -d '1 hour ago' +%s)000
```

#### Common Deployment Failures

**IAM Permission Issues:**
```typescript
// ❌ The "it works on my machine" IAM setup
const fn = new lambda.Function(this, 'Function', {
  // Uses default execution role - often insufficient
});

fn.addToRolePolicy(new iam.PolicyStatement({
  effect: iam.Effect.ALLOW,
  actions: ['*'],  // Security team will hunt you down
  resources: ['*']
}));

// ✅ Proper IAM debugging and setup
const role = new iam.Role(this, 'FunctionRole', {
  assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
  managedPolicies: [
    iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole')
  ]
});

// Add specific permissions with debug logging
role.addToPolicy(new iam.PolicyStatement({
  effect: iam.Effect.ALLOW,
  actions: [
    's3:GetObject',
    's3:PutObject'
  ],
  resources: [`${bucket.bucketArn}/*`]
}));

const fn = new lambda.Function(this, 'Function', {
  role: role,
  environment: {
    DEBUG_IAM: 'true'  // Enable debug logging in your function
  }
});

// Debug helper: Test IAM permissions
new lambda.Function(this, 'IAMTester', {
  runtime: lambda.Runtime.PYTHON_3_9,
  handler: 'index.handler',
  code: lambda.Code.fromInline(`
import boto3
import json

def handler(event, context):
    try:
        # Test each permission your function needs
        s3 = boto3.client('s3')
        s3.head_bucket(Bucket='${bucket.bucketName}')
        return {'statusCode': 200, 'body': 'IAM permissions OK'}
    except Exception as e:
        print(f"IAM Error: {str(e)}")
        return {'statusCode': 500, 'body': str(e)}
  `)
});
```

**Resource Limit Issues:**
```typescript
// Common AWS limits that will ruin your day
export class LimitAwareConstruct extends Construct {
  constructor(scope: Construct, id: string, props: { functionCount: number }) {
    super(scope, id);
    
    // Lambda concurrent executions limit: 1000 (default)
    if (props.functionCount > 50) {
      console.warn(`⚠️  Creating ${props.functionCount} functions - may hit concurrency limits`);
    }
    
    // VPC elastic network interfaces limit: 350 per AZ
    const vpc = new ec2.Vpc(this, 'VPC', {
      maxAzs: 3,
      // Don't create too many subnets
      subnetConfiguration: [
        { name: 'public', subnetType: ec2.SubnetType.PUBLIC, cidrMask: 24 },
        { name: 'private', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, cidrMask: 24 }
      ]
    });
    
    // CloudFormation template size limit: 460,800 bytes
    const templateSize = JSON.stringify(Stack.of(this).toCloudFormation()).length;
    if (templateSize > 400000) {
      console.warn(`⚠️  Template size: ${templateSize} bytes - approaching CloudFormation limit`);
    }
  }
}
```

### Phase 5: Runtime Issues
*"When your infrastructure deploys but doesn't work"*

#### Runtime Debugging Patterns

```typescript
// ✅ Build observability into your constructs
export class ObservableLambdaFunction extends lambda.Function {
  public readonly logGroup: logs.LogGroup;
  public readonly errorAlarm: cloudwatch.Alarm;
  
  constructor(scope: Construct, id: string, props: lambda.FunctionProps) {
    super(scope, id, {
      ...props,
      environment: {
        ...props.environment,
        LOG_LEVEL: 'DEBUG',
        AWS_LAMBDA_LOG_LEVEL: 'DEBUG'
      }
    });
    
    // Explicit log group with retention
    this.logGroup = new logs.LogGroup(this, 'LogGroup', {
      logGroupName: `/aws/lambda/${this.functionName}`,
      retention: logs.RetentionDays.ONE_WEEK,
      removalPolicy: RemovalPolicy.DESTROY
    });
    
    // Error alarm that actually tells you something useful
    this.errorAlarm = new cloudwatch.Alarm(this, 'ErrorAlarm', {
      metric: this.metricErrors({
        period: Duration.minutes(1)
      }),
      threshold: 1,
      evaluationPeriods: 1,
      alarmDescription: `Errors in ${this.functionName} - check CloudWatch logs`
    });
    
    // Dashboard for debugging
    new cloudwatch.Dashboard(this, 'Debug Dashboard', {
      widgets: [
        [
          new cloudwatch.GraphWidget({
            title: 'Function Metrics',
            left: [
              this.metricInvocations(),
              this.metricErrors(),
              this.metricDuration()
            ]
          })
        ],
        [
          new cloudwatch.LogQueryWidget({
            title: 'Recent Errors',
            logGroups: [this.logGroup],
            queryLines: [
              'fields @timestamp, @message',
              'filter @message like /ERROR/',
              'sort @timestamp desc',
              'limit 20'
            ]
          })
        ]
      ]
    });
  }
}
```

### Phase 6: Advanced Debugging Techniques

#### The CDK Debugging Toolkit

```typescript
// Create this in your shared utilities
export class CDKDebugToolkit {
  /**
   * Dump all stack information for debugging
   */
  static dumpStackInfo(stack: Stack): void {
    console.log(`\n🔍 Stack Debug Info: ${stack.stackName}`);
    console.log('Account:', stack.account);
    console.log('Region:', stack.region);
    console.log('Availability Zones:', stack.availabilityZones);
    
    // Check for common issues
    const template = stack.toCloudFormation();
    console.log('Template size:', JSON.stringify(template).length, 'bytes');
    console.log('Resource count:', Object.keys(template.Resources || {}).length);
    
    // List all constructs in the stack
    console.log('\nConstructs in stack:');
    stack.node.findAll().forEach(construct => {
      console.log(`  - ${construct.node.path} (${construct.constructor.name})`);
    });
  }
  
  /**
   * Validate cross-stack references
   */
  static validateCrossStackRefs(stacks: Stack[]): void {
    console.log('\n🔍 Validating cross-stack references...');
    
    stacks.forEach(stack => {
      const deps = stack.dependencies;
      if (deps.length > 0) {
        console.log(`${stack.stackName} depends on:`, deps.map(d => d.stackName));
        
        // Check for circular dependencies
        const checkCircular = (current: Stack, visited: Set<string>): boolean => {
          if (visited.has(current.stackName)) {
            console.error(`❌ Circular dependency detected: ${Array.from(visited).join(' -> ')} -> ${current.stackName}`);
            return true;
          }
          
          visited.add(current.stackName);
          return current.dependencies.some(dep => checkCircular(dep, new Set(visited)));
        };
        
        checkCircular(stack, new Set());
      }
    });
  }
  
  /**
   * Check for common CDK anti-patterns
   */
  static validateBestPractices(stack: Stack): void {
    console.log(`\n🔍 Checking best practices for ${stack.stackName}...`);
    
    const template = stack.toCloudFormation();
    const resources = template.Resources || {};
    
    // Check for hardcoded resource names
    Object.entries(resources).forEach(([logicalId, resource]: [string, any]) => {
      const resourceProps = resource.Properties || {};
      
      // Common properties that shouldn't be hardcoded
      const hardcodedChecks = [
        'BucketName', 'FunctionName', 'QueueName', 'TopicName', 'RoleName'
      ];
      
      hardcodedChecks.forEach(prop => {
        if (resourceProps[prop] && typeof resourceProps[prop] === 'string' && !resourceProps[prop].includes('Ref')) {
          console.warn(`⚠️  ${logicalId} has hardcoded ${prop}: ${resourceProps[prop]}`);
        }
      });
    });
    
    // Check for missing tags
    if (!template.Parameters?.['BootstrapVersion']) {
      console.warn('⚠️  Stack not using CDK bootstrap - may have deployment issues');
    }
  }
}
```

---

## 🚨 Common CDK TypeScript Error Patterns

### The "Greatest Hits" of CDK Failures

#### 1. The "It Works in Dev" Syndrome
```typescript
// ❌ Environment-specific hardcoding
const bucket = new s3.Bucket(this, 'MyBucket', {
  bucketName: 'my-app-bucket'  // Will conflict across environments
});

// ✅ Environment-aware naming
const bucket = new s3.Bucket(this, 'MyBucket', {
  bucketName: `my-app-bucket-${this.node.tryGetContext('environment') || 'dev'}-${this.account}`
});
```

#### 2. The "Import Hell" Problem
```typescript
// ❌ Version mismatch imports
import { Bucket } from '@aws-cdk/aws-s3';  // CDK v1
import { Function } from 'aws-cdk-lib/aws-lambda';  // CDK v2

// ✅ Consistent imports
import { aws_s3 as s3, aws_lambda as lambda } from 'aws-cdk-lib';
```

#### 3. The "Magic String" Disaster
```typescript
// ❌ Magic strings everywhere
lambda.addToRolePolicy(new iam.PolicyStatement({
  actions: ['s3:GetObject'],
  resources: ['arn:aws:s3:::my-bucket/*']  // Will break when bucket name changes
}));

// ✅ Proper resource references
lambda.addToRolePolicy(new iam.PolicyStatement({
  actions: ['s3:GetObject'],
  resources: [bucket.arnForObjects('*')]
}));
```

#### 4. The "Async Await Trap"
```typescript
// ❌ Async in construct constructor (doesn't work)
export class BadConstruct extends Construct {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    
    // This will fail silently
    this.setupResources();
  }
  
  private async setupResources() {
    const data = await someAsyncCall();
    new s3.Bucket(this, 'Bucket', { bucketName: data.name });
  }
}

// ✅ Use CDK custom resources for async operations
export class GoodConstruct extends Construct {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    
    const provider = new cr.Provider(this, 'Provider', {
      onEventHandler: new lambda.Function(this, 'OnEvent', {
        runtime: lambda.Runtime.NODEJS_18_X,
        handler: 'index.onEvent',
        code: lambda.Code.fromInline(`
          exports.onEvent = async (event) => {
            const data = await someAsyncCall();
            return { PhysicalResourceId: data.id, Data: { bucketName: data.name } };
          };
        `)
      })
    });
    
    const customResource = new CustomResource(this, 'CustomResource', {
      serviceToken: provider.serviceToken
    });
    
    new s3.Bucket(this, 'Bucket', {
      bucketName: customResource.getAttString('bucketName')
    });
  }
}
```

---

## 🔧 Emergency Debugging Commands

### When Everything Is Broken

```bash
#!/bin/bash
# Save this as "cdk-emergency-debug.sh"

echo "🚨 CDK Emergency Debugging Protocol"
echo "=================================="

# Check CDK version and environment
echo "📋 Environment Check:"
cdk --version
node --version
npm list aws-cdk-lib 2>/dev/null || npm list @aws-cdk/core 2>/dev/null

# Check AWS credentials
echo -e "\n🔐 AWS Credentials:"
aws sts get-caller-identity 2>/dev/null || echo "❌ AWS credentials not configured"

# List existing stacks
echo -e "\n📚 Existing Stacks:"
cdk list 2>/dev/null || echo "❌ No CDK app found"

# Check for common issues
echo -e "\n🔍 Common Issues Check:"
if [ ! -f "cdk.json" ]; then
  echo "❌ No cdk.json found - not in CDK project root?"
fi

if [ ! -f "package.json" ]; then
  echo "❌ No package.json found"
fi

if [ ! -d "node_modules" ]; then
  echo "❌ No node_modules - run 'npm install'"
fi

# Try to synthesize
echo -e "\n🧪 Synthesis Test:"
cdk synth --dry-run 2>&1 | head -20

echo -e "\n💡 Next Steps:"
echo "1. Fix any red ❌ issues above"
echo "2. Run 'cdk synth MyStackName --verbose' for detailed errors"
echo "3. Check CloudWatch logs if deployment succeeded but runtime fails"
echo "4. Use 'cdk diff MyStackName' to see what would change"
```

### Performance Debugging

```bash
#!/bin/bash
# CDK Performance Debugging

echo "⚡ CDK Performance Analysis"
echo "========================="

# Time synthesis
echo "📊 Synthesis Performance:"
time cdk synth --quiet

# Check template size
echo -e "\n📏 Template Sizes:"
for template in cdk.out/*.template.json; do
  if [ -f "$template" ]; then
    size=$(wc -c < "$template")
    echo "$(basename $template): ${size} bytes"
    if [ $size -gt 460800 ]; then
      echo "  ⚠️  Template too large for CloudFormation!"
    fi
  fi
done

# Check for large constructs
echo -e "\n🏗️  Resource Analysis:"
for template in cdk.out/*.template.json; do
  if [ -f "$template" ]; then
    resources=$(jq '.Resources | length' "$template")
    echo "$(basename $template): ${resources} resources"
    if [ $resources -gt 200 ]; then
      echo "  ⚠️  Large number of resources - consider splitting stack"
    fi
  fi
done
```

---

## 🎯 Debugging Checklist

### Before You Deploy
- [ ] Run `cdk synth` successfully
- [ ] Check generated CloudFormation template size < 450KB
- [ ] Validate no hardcoded resource names
- [ ] Check for circular dependencies
- [ ] Verify IAM permissions are minimal
- [ ] Test with `cdk diff` against existing stack

### When Deployment Fails
- [ ] Check CloudFormation events for real error message
- [ ] Verify AWS service limits haven't been hit
- [ ] Check IAM permissions for deployment role
- [ ] Look for resource naming conflicts
- [ ] Validate all referenced resources exist

### When Runtime Fails
- [ ] Check CloudWatch logs for application errors
- [ ] Verify environment variables are set correctly
- [ ] Test IAM permissions at runtime
- [ ] Check VPC/security group configurations
- [ ] Validate external service connectivity

### Performance Issues
- [ ] Monitor CloudWatch metrics
- [ ] Check for cold starts in Lambda functions
- [ ] Verify database connection pooling
- [ ] Review API Gateway timeout settings
- [ ] Check for unnecessary resource provisioning

---

## 💊 Pain Relief: Quick Fixes for Common Issues

### The "Nothing Works" Troubleshooting

```bash
# The nuclear option (use with caution)
rm -rf node_modules package-lock.json cdk.out
npm install
cdk bootstrap  # If using a new account/region
cdk synth      # Should work now

# If still broken, check your CDK app entry point
cat cdk.json | jq .app
```

### The "It Deployed But Doesn't Work" Fix

```typescript
// Add this to every Lambda function during debugging
const debugLambda = new lambda.Function(this, 'DebugFunction', {
  runtime: lambda.Runtime.NODEJS_18_X,
  handler: 'index.handler',
  code: lambda.Code.fromInline(`
    exports.handler = async (event, context) => {
      console.log('Event:', JSON.stringify(event, null, 2));
      console.log('Context:', JSON.stringify(context, null, 2));
      console.log('Environment:', JSON.stringify(process.env, null, 2));
      
      // Test AWS SDK connectivity
      const AWS = require('aws-sdk');
      const sts = new AWS.STS();
      try {
        const identity = await sts.getCallerIdentity().promise();
        console.log('AWS Identity:', identity);
      } catch (error) {
        console.error('AWS SDK Error:', error);
      }
      
      return { statusCode: 200, body: 'Debug info logged' };
    };
  `),
  environment: {
    DEBUG: 'true'
  }
});
```

---

## 🏆 Advanced Debugging Mastery

### Custom CDK Debugging Aspects

```typescript
/**
 * Custom aspect that adds debugging metadata to all constructs
 */
export class DebuggingAspect implements IAspect {
  visit(node: IConstruct): void {
    // Add debugging tags to all taggable resources
    if (cdk.TagManager.isTaggable(node)) {
      cdk.Tags.of(node).add('Debug:ConstructPath', node.node.path);
      cdk.Tags.of(node).add('Debug:ConstructType', node.constructor.name);
      cdk.Tags.of(node).add('Debug:CDKVersion', cdk.VERSION);
    }
    
    // Add debug outputs for key resources
    if (node instanceof s3.Bucket) {
      new cdk.CfnOutput(Stack.of(node), `${node.node.id}BucketName`, {
        value: node.bucketName,
        description: `Debug: ${node.node.path} bucket name`
      });
    }
    
    if (node instanceof lambda.Function) {
      new cdk.CfnOutput(Stack.of(node), `${node.node.id}FunctionName`, {
        value: node.functionName,
        description: `Debug: ${node.node.path} function name`
      });
    }
  }
}

// Apply to your app
const app = new cdk.App();
const stack = new MyStack(app, 'MyStack');
cdk.Aspects.of(app).add(new DebuggingAspect());
```

Remember: Debugging CDK TypeScript is like being a detective, a therapist, and a fortune teller all at once. The key is systematic investigation, proper tooling, and the wisdom to know when to just delete everything and start over. 

*May your deployments be swift and your rollbacks unnecessary.*