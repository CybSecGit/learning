# Module 3: Advanced CDK TypeScript Patterns
*"Mastering the art of programmatic infrastructure"*

> **Duration**: 1-2 weeks  
> **Cost**: ~$2-5/day while running (deploy → test → destroy same day!)  
> **Prerequisites**: Modules 1-2 completed, comfortable with basic CDK constructs

---

## 🎯 Module Learning Objectives

By the end of this module, you will:
- **Master advanced CDK construct composition** patterns in TypeScript
- **Create custom reusable constructs** with proper TypeScript typing
- **Implement CDK Aspects** for cross-cutting infrastructure concerns
- **Build construct libraries** that can be published and shared
- **Apply advanced TypeScript patterns** specific to infrastructure code
- **Test CDK constructs** comprehensively with Jest and CDK assertions

---

## 📚 Core Lessons

### Lesson 3.1: Advanced Construct Composition Patterns
*"Building infrastructure with composition over inheritance"*

#### The Philosophy of CDK Composition

**Traditional Infrastructure Thinking** → **CDK Composition Thinking**

```typescript
// ❌ Monolithic approach (like huge CloudFormation templates)
export class MonolithicApplicationStack extends Stack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    
    // Everything in one giant class - hard to reuse, test, or maintain
    const vpc = new ec2.Vpc(this, 'VPC', { /* 50 lines of config */ });
    const securityGroup = new ec2.SecurityGroup(this, 'SG', { /* config */ });
    const database = new rds.DatabaseInstance(this, 'DB', { /* config */ });
    const lambda1 = new lambda.Function(this, 'Function1', { /* config */ });
    const lambda2 = new lambda.Function(this, 'Function2', { /* config */ });
    const api = new apigateway.RestApi(this, 'API', { /* config */ });
    // ... 200 more lines
  }
}

// ✅ Composition approach (the CDK way)
export class ApplicationStack extends Stack {
  constructor(scope: Construct, id: string, props: ApplicationStackProps) {
    super(scope, id, props);
    
    // Compose from reusable, testable constructs
    const networking = new NetworkingConstruct(this, 'Networking', {
      cidr: props.networkConfig.cidr,
      maxAzs: props.networkConfig.maxAzs
    });
    
    const dataLayer = new DataLayerConstruct(this, 'DataLayer', {
      vpc: networking.vpc,
      databaseConfig: props.databaseConfig
    });
    
    const computeLayer = new ComputeLayerConstruct(this, 'ComputeLayer', {
      vpc: networking.vpc,
      database: dataLayer.database
    });
    
    const apiLayer = new ApiLayerConstruct(this, 'ApiLayer', {
      lambdaFunctions: computeLayer.functions,
      domainConfig: props.domainConfig
    });
  }
}
```

#### Advanced Construct Patterns

**1. The Builder Pattern for Complex Infrastructure**

```typescript
export interface WebApplicationConfig {
  readonly domainName: string;
  readonly certificateArn: string;
  readonly databaseConfig: DatabaseConfig;
  readonly cacheConfig?: CacheConfig;
  readonly monitoringConfig?: MonitoringConfig;
}

export class WebApplicationBuilder {
  private config: Partial<WebApplicationConfig> = {};
  
  public withDomain(domainName: string, certificateArn: string): this {
    this.config.domainName = domainName;
    this.config.certificateArn = certificateArn;
    return this;
  }
  
  public withDatabase(config: DatabaseConfig): this {
    this.config.databaseConfig = config;
    return this;
  }
  
  public withCaching(config: CacheConfig): this {
    this.config.cacheConfig = config;
    return this;
  }
  
  public withMonitoring(config: MonitoringConfig): this {
    this.config.monitoringConfig = config;
    return this;
  }
  
  public build(scope: Construct, id: string): WebApplication {
    if (!this.config.domainName || !this.config.databaseConfig) {
      throw new Error('Domain and database configuration are required');
    }
    
    return new WebApplication(scope, id, this.config as WebApplicationConfig);
  }
}

// Usage
const webApp = new WebApplicationBuilder()
  .withDomain('api.example.com', 'arn:aws:acm:...')
  .withDatabase({ instanceClass: 'db.t3.micro', engine: 'postgres' })
  .withCaching({ nodeType: 'cache.t3.micro', numNodes: 2 })
  .withMonitoring({ detailedMonitoring: true, alertEmail: 'ops@example.com' })
  .build(this, 'WebApplication');
```

**2. The Factory Pattern for Environment-Specific Infrastructure**

```typescript
export abstract class InfrastructureFactory {
  abstract createCompute(scope: Construct, id: string): ICompute;
  abstract createDatabase(scope: Construct, id: string): IDatabase;
  abstract createMonitoring(scope: Construct, id: string): IMonitoring;
}

export class DevelopmentInfrastructureFactory extends InfrastructureFactory {
  createCompute(scope: Construct, id: string): ICompute {
    return new lambda.Function(scope, id, {
      runtime: lambda.Runtime.NODEJS_18_X,
      memorySize: 128, // Minimal for dev
      timeout: Duration.seconds(30)
    });
  }
  
  createDatabase(scope: Construct, id: string): IDatabase {
    return new rds.DatabaseInstance(scope, id, {
      engine: rds.DatabaseInstanceEngine.postgres({ version: rds.PostgresEngineVersion.VER_13_7 }),
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
      multiAz: false,
      deletionProtection: false
    });
  }
  
  createMonitoring(scope: Construct, id: string): IMonitoring {
    // Minimal monitoring for dev
    return new BasicMonitoring(scope, id);
  }
}

export class ProductionInfrastructureFactory extends InfrastructureFactory {
  createCompute(scope: Construct, id: string): ICompute {
    return new lambda.Function(scope, id, {
      runtime: lambda.Runtime.NODEJS_18_X,
      memorySize: 1024, // More memory for prod
      timeout: Duration.minutes(15),
      reservedConcurrentExecutions: 100
    });
  }
  
  createDatabase(scope: Construct, id: string): IDatabase {
    return new rds.DatabaseInstance(scope, id, {
      engine: rds.DatabaseInstanceEngine.postgres({ version: rds.PostgresEngineVersion.VER_13_7 }),
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.MEMORY5, ec2.InstanceSize.LARGE),
      multiAz: true,
      deletionProtection: true,
      backupRetention: Duration.days(30)
    });
  }
  
  createMonitoring(scope: Construct, id: string): IMonitoring {
    return new ComprehensiveMonitoring(scope, id, {
      detailedMetrics: true,
      alerting: true,
      dashboard: true
    });
  }
}

// Usage in stack
export class ApplicationStack extends Stack {
  constructor(scope: Construct, id: string, props: ApplicationStackProps) {
    super(scope, id, props);
    
    const factory = props.environment === 'prod' 
      ? new ProductionInfrastructureFactory()
      : new DevelopmentInfrastructureFactory();
    
    const compute = factory.createCompute(this, 'Compute');
    const database = factory.createDatabase(this, 'Database');
    const monitoring = factory.createMonitoring(this, 'Monitoring');
  }
}
```

**3. The Strategy Pattern for Deployment Strategies**

```typescript
export interface DeploymentStrategy {
  deploy(construct: Construct, application: ApplicationConfig): IDeployment;
}

export class BlueGreenDeploymentStrategy implements DeploymentStrategy {
  deploy(construct: Construct, application: ApplicationConfig): IDeployment {
    const blueEnvironment = this.createEnvironment(construct, 'Blue', application);
    const greenEnvironment = this.createEnvironment(construct, 'Green', application);
    
    return new BlueGreenDeployment(construct, 'BlueGreenDeployment', {
      blueEnvironment,
      greenEnvironment,
      trafficShiftingConfig: {
        type: 'linear',
        percentage: 10,
        interval: Duration.minutes(1)
      }
    });
  }
  
  private createEnvironment(construct: Construct, color: string, config: ApplicationConfig) {
    return new ApplicationEnvironment(construct, `${color}Environment`, {
      applicationConfig: config,
      color: color.toLowerCase()
    });
  }
}

export class CanaryDeploymentStrategy implements DeploymentStrategy {
  constructor(private canaryPercentage: number = 5) {}
  
  deploy(construct: Construct, application: ApplicationConfig): IDeployment {
    const productionEnvironment = this.createEnvironment(construct, 'Production', application);
    const canaryEnvironment = this.createEnvironment(construct, 'Canary', application);
    
    return new CanaryDeployment(construct, 'CanaryDeployment', {
      productionEnvironment,
      canaryEnvironment,
      canaryPercentage: this.canaryPercentage,
      autoRollbackConfig: {
        enableAutoRollback: true,
        errorThreshold: 5.0,
        duration: Duration.minutes(5)
      }
    });
  }
  
  private createEnvironment(construct: Construct, type: string, config: ApplicationConfig) {
    return new ApplicationEnvironment(construct, `${type}Environment`, {
      applicationConfig: config,
      type: type.toLowerCase()
    });
  }
}

// Usage
export class WebApplicationStack extends Stack {
  constructor(scope: Construct, id: string, props: WebApplicationStackProps) {
    super(scope, id, props);
    
    const deploymentStrategy = props.environment === 'prod'
      ? new BlueGreenDeploymentStrategy()
      : new CanaryDeploymentStrategy(10); // 10% canary for staging
    
    const deployment = deploymentStrategy.deploy(this, props.applicationConfig);
  }
}
```

#### 🛠️ Hands-On Lab 3.1: Build a Composable Infrastructure Library

**Challenge**: Create a reusable infrastructure library for web applications

**Your Mission**: Build a library that can deploy different types of web applications using composition patterns.

**Requirements**:
1. **Base Components**: VPC, Security Groups, Load Balancer, Database
2. **Compute Options**: Lambda, ECS Fargate, or EC2
3. **Storage Options**: S3, DynamoDB, RDS
4. **Deployment Strategies**: Rolling, Blue/Green, Canary
5. **TypeScript Interfaces**: Proper typing for all configurations

**Expected Structure**:
```typescript
// lib/constructs/base/networking.ts
export interface NetworkingProps {
  readonly cidr: string;
  readonly maxAzs: number;
  readonly natGateways?: number;
}

export class NetworkingConstruct extends Construct {
  public readonly vpc: ec2.IVpc;
  public readonly privateSubnets: ec2.ISubnet[];
  public readonly publicSubnets: ec2.ISubnet[];
  
  constructor(scope: Construct, id: string, props: NetworkingProps) {
    super(scope, id);
    
    this.vpc = new ec2.Vpc(this, 'VPC', {
      cidr: props.cidr,
      maxAzs: props.maxAzs,
      natGateways: props.natGateways ?? 1,
      subnetConfiguration: [
        {
          name: 'public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24
        },
        {
          name: 'private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
          cidrMask: 24
        }
      ]
    });
    
    this.privateSubnets = this.vpc.privateSubnets;
    this.publicSubnets = this.vpc.publicSubnets;
  }
}

// lib/constructs/compute/lambda-compute.ts
export interface LambdaComputeProps {
  readonly vpc: ec2.IVpc;
  readonly functionConfigs: LambdaFunctionConfig[];
  readonly environment?: Record<string, string>;
}

export class LambdaComputeConstruct extends Construct implements IComputeConstruct {
  public readonly functions: lambda.IFunction[];
  
  constructor(scope: Construct, id: string, props: LambdaComputeProps) {
    super(scope, id);
    
    this.functions = props.functionConfigs.map((config, index) => {
      return new lambda.Function(this, `Function${index}`, {
        runtime: lambda.Runtime.NODEJS_18_X,
        handler: config.handler,
        code: lambda.Code.fromAsset(config.codePath),
        vpc: props.vpc,
        environment: {
          ...props.environment,
          ...config.environment
        },
        timeout: config.timeout ?? Duration.seconds(30),
        memorySize: config.memorySize ?? 256
      });
    });
  }
  
  public getFunction(index: number): lambda.IFunction {
    return this.functions[index];
  }
}

// lib/constructs/web-application.ts
export interface WebApplicationProps {
  readonly networkingConfig: NetworkingProps;
  readonly computeConfig: ComputeConfig;
  readonly databaseConfig?: DatabaseConfig;
  readonly domainConfig?: DomainConfig;
  readonly deploymentStrategy?: DeploymentStrategy;
}

export class WebApplication extends Construct {
  public readonly networking: NetworkingConstruct;
  public readonly compute: IComputeConstruct;
  public readonly database?: IDatabaseConstruct;
  public readonly api: ApiGatewayConstruct;
  
  constructor(scope: Construct, id: string, props: WebApplicationProps) {
    super(scope, id);
    
    // Compose infrastructure from smaller constructs
    this.networking = new NetworkingConstruct(this, 'Networking', props.networkingConfig);
    
    this.compute = this.createComputeLayer(props.computeConfig);
    
    if (props.databaseConfig) {
      this.database = this.createDatabaseLayer(props.databaseConfig);
    }
    
    this.api = new ApiGatewayConstruct(this, 'API', {
      functions: this.compute.getFunctions(),
      domainConfig: props.domainConfig
    });
    
    // Apply deployment strategy if specified
    if (props.deploymentStrategy) {
      props.deploymentStrategy.apply(this);
    }
  }
  
  private createComputeLayer(config: ComputeConfig): IComputeConstruct {
    switch (config.type) {
      case 'lambda':
        return new LambdaComputeConstruct(this, 'LambdaCompute', {
          vpc: this.networking.vpc,
          functionConfigs: config.lambdaConfigs!
        });
      case 'ecs':
        return new EcsComputeConstruct(this, 'EcsCompute', {
          vpc: this.networking.vpc,
          serviceConfigs: config.ecsConfigs!
        });
      default:
        throw new Error(`Unsupported compute type: ${config.type}`);
    }
  }
  
  private createDatabaseLayer(config: DatabaseConfig): IDatabaseConstruct {
    switch (config.type) {
      case 'rds':
        return new RdsDatabaseConstruct(this, 'RdsDatabase', {
          vpc: this.networking.vpc,
          rdsConfig: config.rdsConfig!
        });
      case 'dynamodb':
        return new DynamoDbConstruct(this, 'DynamoDb', {
          tables: config.dynamoConfig!
        });
      default:
        throw new Error(`Unsupported database type: ${config.type}`);
    }
  }
}
```

**Success Criteria**:
- Can deploy different application types using composition
- TypeScript interfaces provide type safety for all configurations
- Components are reusable across different applications
- Proper separation of concerns between constructs
- `cdk synth` produces valid CloudFormation
- Unit tests pass for all constructs

---

### Lesson 3.2: Creating Custom CDK Constructs in TypeScript
*"Building your own infrastructure building blocks"*

#### The Anatomy of a CDK Construct

**Understanding Construct Levels in Your Custom Library**:

```typescript
// Level 1: Basic construct wrapping AWS resources
export class BasicS3Bucket extends Construct {
  public readonly bucket: s3.Bucket;
  
  constructor(scope: Construct, id: string, props: BasicS3BucketProps) {
    super(scope, id);
    
    this.bucket = new s3.Bucket(this, 'Bucket', {
      bucketName: props.bucketName,
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL
    });
  }
}

// Level 2: Opinionated construct with best practices
export class SecureS3Bucket extends Construct {
  public readonly bucket: s3.Bucket;
  public readonly cloudfront: cloudfront.Distribution;
  
  constructor(scope: Construct, id: string, props: SecureS3BucketProps) {
    super(scope, id);
    
    // Create bucket with security best practices
    this.bucket = new s3.Bucket(this, 'Bucket', {
      encryption: s3.BucketEncryption.KMS_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      versioned: true,
      lifecycleRules: [{
        id: 'OptimizeStorage',
        transitions: [{
          storageClass: s3.StorageClass.INTELLIGENT_TIERING,
          transitionAfter: Duration.days(30)
        }]
      }],
      serverAccessLogsPrefix: 'access-logs/',
      enforceSSL: true
    });
    
    // Origin Access Identity for CloudFront
    const oai = new cloudfront.OriginAccessIdentity(this, 'OAI');
    this.bucket.grantRead(oai);
    
    // CloudFront distribution with security headers
    this.cloudfront = new cloudfront.Distribution(this, 'Distribution', {
      defaultBehavior: {
        origin: new origins.S3Origin(this.bucket, { originAccessIdentity: oai }),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        responseHeadersPolicy: new cloudfront.ResponseHeadersPolicy(this, 'SecurityHeaders', {
          securityHeadersBehavior: {
            contentTypeOptions: { override: true },
            frameOptions: { frameOption: cloudfront.HeadersFrameOption.DENY, override: true },
            referrerPolicy: { 
              referrerPolicy: cloudfront.HeadersReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN, 
              override: true 
            }
          }
        })
      },
      priceClass: cloudfront.PriceClass.PRICE_CLASS_100
    });
  }
}

// Level 3: Complete architectural pattern
export class StaticWebsite extends Construct {
  public readonly bucket: s3.Bucket;
  public readonly distribution: cloudfront.Distribution;
  public readonly certificate: acm.Certificate;
  public readonly domain: route53.ARecord;
  
  constructor(scope: Construct, id: string, props: StaticWebsiteProps) {
    super(scope, id);
    
    // Certificate for HTTPS
    this.certificate = new acm.Certificate(this, 'Certificate', {
      domainName: props.domainName,
      validation: acm.CertificateValidation.fromDns(props.hostedZone)
    });
    
    // Secure S3 bucket
    const secureStorage = new SecureS3Bucket(this, 'Storage', {
      // Configuration for the secure bucket
    });
    
    this.bucket = secureStorage.bucket;
    this.distribution = secureStorage.cloudfront;
    
    // Custom domain
    this.domain = new route53.ARecord(this, 'Domain', {
      zone: props.hostedZone,
      recordName: props.domainName,
      target: route53.RecordTarget.fromAlias(
        new route53targets.CloudFrontTarget(this.distribution)
      )
    });
    
    // Deployment pipeline (if specified)
    if (props.deploymentConfig) {
      new StaticWebsiteDeployment(this, 'Deployment', {
        bucket: this.bucket,
        distribution: this.distribution,
        source: props.deploymentConfig.source,
        buildCommand: props.deploymentConfig.buildCommand
      });
    }
  }
}
```

#### Advanced TypeScript Patterns for CDK Constructs

**1. Generic Constructs with Type Safety**

```typescript
// Generic construct for monitored resources
export interface MonitoredResourceProps<T> {
  readonly resourceConfig: T;
  readonly monitoringConfig: MonitoringConfig;
  readonly alertingConfig: AlertingConfig;
}

export class MonitoredResource<T> extends Construct {
  public readonly resource: T;
  public readonly alarms: cloudwatch.Alarm[];
  public readonly dashboard: cloudwatch.Dashboard;
  
  constructor(
    scope: Construct, 
    id: string, 
    props: MonitoredResourceProps<T>,
    resourceFactory: (scope: Construct, id: string, config: T) => T
  ) {
    super(scope, id);
    
    // Create the resource using the factory function
    this.resource = resourceFactory(this, 'Resource', props.resourceConfig);
    
    // Create monitoring based on resource type
    this.alarms = this.createAlarms(props.monitoringConfig);
    this.dashboard = this.createDashboard(props.monitoringConfig);
  }
  
  private createAlarms(config: MonitoringConfig): cloudwatch.Alarm[] {
    // Implementation depends on resource type
    return config.metrics.map((metric, index) => {
      return new cloudwatch.Alarm(this, `Alarm${index}`, {
        metric: new cloudwatch.Metric({
          namespace: metric.namespace,
          metricName: metric.name,
          dimensionsMap: metric.dimensions
        }),
        threshold: metric.threshold,
        evaluationPeriods: metric.evaluationPeriods
      });
    });
  }
  
  private createDashboard(config: MonitoringConfig): cloudwatch.Dashboard {
    return new cloudwatch.Dashboard(this, 'Dashboard', {
      dashboardName: `${this.node.id}-dashboard`,
      widgets: [
        // Widget creation based on monitoring config
      ]
    });
  }
}

// Usage with type safety
const monitoredLambda = new MonitoredResource(this, 'MonitoredLambda', {
  resourceConfig: {
    runtime: lambda.Runtime.NODEJS_18_X,
    handler: 'index.handler',
    code: lambda.Code.fromAsset('lambda')
  },
  monitoringConfig: {
    metrics: [
      { namespace: 'AWS/Lambda', name: 'Duration', dimensions: { FunctionName: 'my-function' } },
      { namespace: 'AWS/Lambda', name: 'Errors', dimensions: { FunctionName: 'my-function' } }
    ]
  },
  alertingConfig: {
    email: 'alerts@example.com'
  }
}, (scope, id, config) => new lambda.Function(scope, id, config));
```

**2. Fluent Interface Pattern for Construct Configuration**

```typescript
export class ApiGatewayBuilder {
  private config: Partial<ApiGatewayConfig> = {};
  
  public withCors(allowOrigins: string[] = ['*']): this {
    this.config.corsConfiguration = {
      allowOrigins,
      allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
      allowHeaders: ['Content-Type', 'Authorization']
    };
    return this;
  }
  
  public withAuthorizer(type: 'lambda' | 'cognito', config: AuthorizerConfig): this {
    this.config.authorizer = { type, ...config };
    return this;
  }
  
  public withCustomDomain(domainName: string, certificateArn: string): this {
    this.config.customDomain = { domainName, certificateArn };
    return this;
  }
  
  public withRequestValidation(validateRequestBody: boolean = true, validateParameters: boolean = true): this {
    this.config.requestValidation = { validateRequestBody, validateParameters };
    return this;
  }
  
  public withThrottling(rateLimit: number, burstLimit: number): this {
    this.config.throttling = { rateLimit, burstLimit };
    return this;
  }
  
  public addRoute(path: string, method: string, handler: lambda.IFunction): this {
    if (!this.config.routes) {
      this.config.routes = [];
    }
    this.config.routes.push({ path, method, handler });
    return this;
  }
  
  public build(scope: Construct, id: string): ApiGatewayConstruct {
    return new ApiGatewayConstruct(scope, id, this.config as ApiGatewayConfig);
  }
}

// Usage with fluent interface
const api = new ApiGatewayBuilder()
  .withCors(['https://example.com'])
  .withAuthorizer('lambda', { functionArn: authorizerFunction.functionArn })
  .withCustomDomain('api.example.com', certificateArn)
  .withRequestValidation(true, true)
  .withThrottling(1000, 2000)
  .addRoute('/users', 'GET', getUsersFunction)
  .addRoute('/users', 'POST', createUserFunction)
  .addRoute('/users/{id}', 'GET', getUserFunction)
  .addRoute('/users/{id}', 'PUT', updateUserFunction)
  .addRoute('/users/{id}', 'DELETE', deleteUserFunction)
  .build(this, 'UserAPI');
```

**3. Decorator Pattern for Adding Capabilities**

```typescript
// Base construct interface
export interface EnhanceableConstruct {
  addCapability(capability: ConstructCapability): void;
}

// Capability interface
export interface ConstructCapability {
  apply(construct: Construct): void;
}

// Monitoring capability
export class MonitoringCapability implements ConstructCapability {
  constructor(private config: MonitoringConfig) {}
  
  apply(construct: Construct): void {
    // Add CloudWatch alarms and dashboards
    const alarms = this.config.metrics.map((metric, index) => {
      return new cloudwatch.Alarm(construct, `Alarm${index}`, {
        metric: new cloudwatch.Metric(metric),
        threshold: metric.threshold
      });
    });
    
    new cloudwatch.Dashboard(construct, 'Dashboard', {
      widgets: [
        new cloudwatch.GraphWidget({
          title: 'Metrics',
          left: alarms.map(alarm => alarm.metric)
        })
      ]
    });
  }
}

// Logging capability
export class LoggingCapability implements ConstructCapability {
  constructor(private config: LoggingConfig) {}
  
  apply(construct: Construct): void {
    // Add centralized logging
    const logGroup = new logs.LogGroup(construct, 'LogGroup', {
      retention: logs.RetentionDays.ONE_MONTH,
      logGroupName: `/aws/${construct.node.id.toLowerCase()}`
    });
    
    // Add log stream for the construct
    new logs.LogStream(construct, 'LogStream', {
      logGroup,
      logStreamName: `${construct.node.id}-stream`
    });
  }
}

// Base construct that can be enhanced
export class EnhanceableFunction extends Construct implements EnhanceableConstruct {
  public readonly function: lambda.Function;
  private capabilities: ConstructCapability[] = [];
  
  constructor(scope: Construct, id: string, props: lambda.FunctionProps) {
    super(scope, id);
    
    this.function = new lambda.Function(this, 'Function', props);
  }
  
  public addCapability(capability: ConstructCapability): void {
    this.capabilities.push(capability);
    capability.apply(this);
  }
  
  public addMonitoring(config: MonitoringConfig): this {
    this.addCapability(new MonitoringCapability(config));
    return this;
  }
  
  public addLogging(config: LoggingConfig): this {
    this.addCapability(new LoggingCapability(config));
    return this;
  }
}

// Usage
const enhancedFunction = new EnhanceableFunction(this, 'MyFunction', {
  runtime: lambda.Runtime.NODEJS_18_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('lambda')
})
.addMonitoring({
  metrics: [
    { namespace: 'AWS/Lambda', metricName: 'Duration', threshold: 5000 },
    { namespace: 'AWS/Lambda', metricName: 'Errors', threshold: 1 }
  ]
})
.addLogging({
  level: 'INFO',
  format: 'JSON'
});
```

#### 🛠️ Hands-On Lab 3.2: Build a Custom Construct Library

**Challenge**: Create a publishable NPM package with custom CDK constructs

**Your Mission**: Build a construct library for serverless applications with these features:

1. **Core Constructs**: API Gateway, Lambda Functions, DynamoDB Tables
2. **High-Level Patterns**: Complete REST API, CRUD Operations, Event Processing
3. **TypeScript Features**: Generic types, fluent interfaces, decorators
4. **Testing**: Unit tests with CDK assertions
5. **Documentation**: TypeDoc comments and README

**Project Structure**:
```
my-cdk-constructs/
├── src/
│   ├── constructs/
│   │   ├── api-gateway-construct.ts
│   │   ├── lambda-construct.ts
│   │   ├── dynamodb-construct.ts
│   │   └── index.ts
│   ├── patterns/
│   │   ├── rest-api-pattern.ts
│   │   ├── crud-pattern.ts
│   │   ├── event-processing-pattern.ts
│   │   └── index.ts
│   └── index.ts
├── test/
│   ├── constructs/
│   └── patterns/
├── package.json
├── tsconfig.json
├── jest.config.js
└── README.md
```

**Implementation Requirements**:

```typescript
// src/patterns/rest-api-pattern.ts
export interface RestApiPatternProps {
  readonly apiName: string;
  readonly corsConfig?: CorsConfiguration;
  readonly authConfig?: AuthConfiguration;
  readonly tableConfig: DynamoTableConfiguration;
  readonly lambdaConfig: LambdaConfiguration;
}

export class RestApiPattern extends Construct {
  public readonly api: apigateway.RestApi;
  public readonly table: dynamodb.Table;
  public readonly functions: { [key: string]: lambda.Function };
  
  constructor(scope: Construct, id: string, props: RestApiPatternProps) {
    super(scope, id);
    
    // Create DynamoDB table
    this.table = new dynamodb.Table(this, 'Table', {
      tableName: props.tableConfig.tableName,
      partitionKey: props.tableConfig.partitionKey,
      sortKey: props.tableConfig.sortKey,
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: RemovalPolicy.DESTROY // For learning
    });
    
    // Create Lambda functions for CRUD operations
    this.functions = this.createCrudFunctions(props.lambdaConfig);
    
    // Create API Gateway
    this.api = new apigateway.RestApi(this, 'Api', {
      restApiName: props.apiName,
      defaultCorsPreflightOptions: props.corsConfig
    });
    
    // Set up API routes
    this.setupApiRoutes();
  }
  
  private createCrudFunctions(config: LambdaConfiguration): { [key: string]: lambda.Function } {
    const operations = ['create', 'read', 'update', 'delete', 'list'];
    const functions: { [key: string]: lambda.Function } = {};
    
    operations.forEach(operation => {
      functions[operation] = new lambda.Function(this, `${operation}Function`, {
        runtime: lambda.Runtime.NODEJS_18_X,
        handler: `${operation}.handler`,
        code: lambda.Code.fromAsset(config.codeAssetPath),
        environment: {
          TABLE_NAME: this.table.tableName,
          ...config.environment
        },
        timeout: Duration.seconds(30)
      });
      
      // Grant appropriate permissions
      if (operation === 'read' || operation === 'list') {
        this.table.grantReadData(functions[operation]);
      } else {
        this.table.grantReadWriteData(functions[operation]);
      }
    });
    
    return functions;
  }
  
  private setupApiRoutes(): void {
    const items = this.api.root.addResource('items');
    const item = items.addResource('{id}');
    
    // POST /items - create
    items.addMethod('POST', new apigateway.LambdaIntegration(this.functions.create));
    
    // GET /items - list
    items.addMethod('GET', new apigateway.LambdaIntegration(this.functions.list));
    
    // GET /items/{id} - read
    item.addMethod('GET', new apigateway.LambdaIntegration(this.functions.read));
    
    // PUT /items/{id} - update
    item.addMethod('PUT', new apigateway.LambdaIntegration(this.functions.update));
    
    // DELETE /items/{id} - delete
    item.addMethod('DELETE', new apigateway.LambdaIntegration(this.functions.delete));
  }
}

// Usage
const restApi = new RestApiPattern(this, 'UserAPI', {
  apiName: 'user-management-api',
  corsConfig: {
    allowOrigins: ['*'],
    allowMethods: ['GET', 'POST', 'PUT', 'DELETE']
  },
  tableConfig: {
    tableName: 'users',
    partitionKey: { name: 'userId', type: dynamodb.AttributeType.STRING },
    sortKey: { name: 'timestamp', type: dynamodb.AttributeType.NUMBER }
  },
  lambdaConfig: {
    codeAssetPath: './lambda',
    environment: {
      LOG_LEVEL: 'INFO'
    }
  }
});
```

**Testing Requirements**:
```typescript
// test/patterns/rest-api-pattern.test.ts
import { Template } from 'aws-cdk-lib/assertions';
import { Stack } from 'aws-cdk-lib';
import { RestApiPattern } from '../../src/patterns/rest-api-pattern';

describe('RestApiPattern', () => {
  test('creates all required resources', () => {
    const stack = new Stack();
    
    new RestApiPattern(stack, 'TestRestApi', {
      apiName: 'test-api',
      tableConfig: {
        tableName: 'test-table',
        partitionKey: { name: 'id', type: 'S' }
      },
      lambdaConfig: {
        codeAssetPath: './test-lambda'
      }
    });
    
    const template = Template.fromStack(stack);
    
    // Assert DynamoDB table exists
    template.hasResourceProperties('AWS::DynamoDB::Table', {
      TableName: 'test-table',
      BillingMode: 'PAY_PER_REQUEST'
    });
    
    // Assert API Gateway exists
    template.hasResourceProperties('AWS::ApiGateway::RestApi', {
      Name: 'test-api'
    });
    
    // Assert Lambda functions exist
    template.resourceCountIs('AWS::Lambda::Function', 5); // CRUD + List
    
    // Assert proper IAM permissions
    template.hasResourceProperties('AWS::IAM::Policy', {
      PolicyDocument: {
        Statement: [
          {
            Effect: 'Allow',
            Action: ['dynamodb:GetItem', 'dynamodb:PutItem', 'dynamodb:UpdateItem', 'dynamodb:DeleteItem', 'dynamodb:Scan'],
            Resource: { 'Fn::GetAtt': ['TestRestApiTable', 'Arn'] }
          }
        ]
      }
    });
  });
});
```

**Success Criteria**:
- Custom constructs compile without TypeScript errors
- All unit tests pass
- `npm run build` creates distributable package
- Generated CloudFormation is valid and deployable
- TypeDoc generates proper documentation
- Package can be imported and used in other CDK projects

---

### Lesson 3.3: CDK Aspects for Cross-Cutting Concerns
*"Applying consistent patterns across your entire infrastructure"*

#### Understanding CDK Aspects

CDK Aspects are a powerful way to apply cross-cutting concerns (like tagging, security policies, compliance checks) across your entire CDK application. They follow the Visitor pattern and can modify constructs after they're created.

#### Built-in Aspects and Custom Implementations

**1. Tagging Aspect (Built-in)**

```typescript
import { Aspects, Tags } from 'aws-cdk-lib';

export class ApplicationStack extends Stack {
  constructor(scope: Construct, id: string, props: ApplicationStackProps) {
    super(scope, id, props);
    
    // Create your infrastructure
    const vpc = new ec2.Vpc(this, 'VPC');
    const lambda = new lambda.Function(this, 'Function', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline('exports.handler = async () => ({ statusCode: 200 });')
    });
    
    // Apply tags to all taggable resources in this stack
    Tags.of(this).add('Environment', props.environment);
    Tags.of(this).add('Project', props.projectName);
    Tags.of(this).add('Owner', props.owner);
    Tags.of(this).add('CostCenter', props.costCenter);
    Tags.of(this).add('ManagedBy', 'CDK');
  }
}
```

**2. Custom Security Aspect**

```typescript
import { IAspect, IConstruct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as rds from 'aws-cdk-lib/aws-rds';

export class SecurityComplianceAspect implements IAspect {
  visit(node: IConstruct): void {
    // Apply security policies to S3 buckets
    if (node instanceof s3.Bucket) {
      this.enforceS3Security(node);
    }
    
    // Apply security policies to Lambda functions
    if (node instanceof lambda.Function) {
      this.enforceLambdaSecurity(node);
    }
    
    // Apply security policies to RDS instances
    if (node instanceof rds.DatabaseInstance) {
      this.enforceRDSecurity(node);
    }
  }
  
  private enforceS3Security(bucket: s3.Bucket): void {
    // Enforce encryption
    const cfnBucket = bucket.node.defaultChild as s3.CfnBucket;
    if (!cfnBucket.bucketEncryption) {
      cfnBucket.bucketEncryption = {
        serverSideEncryptionConfiguration: [{
          serverSideEncryptionByDefault: {
            sseAlgorithm: 'AES256'
          }
        }]
      };
    }
    
    // Enforce versioning
    if (!cfnBucket.versioningConfiguration) {
      cfnBucket.versioningConfiguration = {
        status: 'Enabled'
      };
    }
    
    // Block public access
    if (!cfnBucket.publicAccessBlockConfiguration) {
      cfnBucket.publicAccessBlockConfiguration = {
        blockPublicAcls: true,
        blockPublicPolicy: true,
        ignorePublicAcls: true,
        restrictPublicBuckets: true
      };
    }
  }
  
  private enforceLambdaSecurity(func: lambda.Function): void {
    const cfnFunction = func.node.defaultChild as lambda.CfnFunction;
    
    // Enforce environment variable encryption
    if (cfnFunction.environment && !cfnFunction.kmsKeyArn) {
      // Add warning or create KMS key
      console.warn(`Lambda function ${func.node.id} should use KMS encryption for environment variables`);
    }
    
    // Enforce reserved concurrency (prevent runaway costs)
    if (!cfnFunction.reservedConcurrencyExecutions) {
      cfnFunction.reservedConcurrencyExecutions = 100; // Default limit
    }
    
    // Add security-related environment variables
    if (cfnFunction.environment) {
      cfnFunction.environment.variables = {
        ...cfnFunction.environment.variables,
        NODE_OPTIONS: '--enable-source-maps',
        AWS_NODEJS_CONNECTION_REUSE_ENABLED: '1'
      };
    }
  }
  
  private enforceRDSecurity(db: rds.DatabaseInstance): void {
    const cfnDb = db.node.defaultChild as rds.CfnDBInstance;
    
    // Enforce encryption at rest
    if (cfnDb.storageEncrypted === undefined) {
      cfnDb.storageEncrypted = true;
    }
    
    // Enforce backup retention
    if (!cfnDb.backupRetentionPeriod || cfnDb.backupRetentionPeriod < 7) {
      cfnDb.backupRetentionPeriod = 7; // Minimum 7 days
    }
    
    // Enforce deletion protection for production
    if (cfnDb.deletionProtection === undefined) {
      cfnDb.deletionProtection = true;
    }
  }
}

// Apply the aspect to your app
export class MyApp extends App {
  constructor() {
    super();
    
    const stack = new ApplicationStack(this, 'MyAppStack', {
      environment: 'production',
      projectName: 'my-project',
      owner: 'team-alpha',
      costCenter: 'engineering'
    });
    
    // Apply security compliance to all constructs
    Aspects.of(this).add(new SecurityComplianceAspect());
  }
}
```

**3. Cost Optimization Aspect**

```typescript
export class CostOptimizationAspect implements IAspect {
  constructor(private environment: string) {}
  
  visit(node: IConstruct): void {
    // Optimize EC2 instances for non-production
    if (node instanceof ec2.Instance && this.environment !== 'production') {
      this.optimizeEC2Instance(node);
    }
    
    // Optimize RDS instances for non-production
    if (node instanceof rds.DatabaseInstance && this.environment !== 'production') {
      this.optimizeRDSInstance(node);
    }
    
    // Add lifecycle policies to S3 buckets
    if (node instanceof s3.Bucket) {
      this.addS3LifecyclePolicies(node);
    }
    
    // Optimize Lambda memory allocation
    if (node instanceof lambda.Function) {
      this.optimizeLambdaMemory(node);
    }
  }
  
  private optimizeEC2Instance(instance: ec2.Instance): void {
    const cfnInstance = instance.node.defaultChild as ec2.CfnInstance;
    
    // Use burstable instances for development
    if (cfnInstance.instanceType?.includes('m5') || cfnInstance.instanceType?.includes('c5')) {
      cfnInstance.instanceType = cfnInstance.instanceType
        .replace('m5', 't3')
        .replace('c5', 't3');
    }
  }
  
  private optimizeRDSInstance(db: rds.DatabaseInstance): void {
    const cfnDb = db.node.defaultChild as rds.CfnDBInstance;
    
    // Disable multi-AZ for development
    cfnDb.multiAz = false;
    
    // Use smaller instance types
    if (cfnDb.dbInstanceClass?.includes('r5') || cfnDb.dbInstanceClass?.includes('m5')) {
      cfnDb.dbInstanceClass = cfnDb.dbInstanceClass
        .replace('r5', 't3')
        .replace('m5', 't3');
    }
    
    // Reduce backup retention for development
    cfnDb.backupRetentionPeriod = 1;
  }
  
  private addS3LifecyclePolicies(bucket: s3.Bucket): void {
    const cfnBucket = bucket.node.defaultChild as s3.CfnBucket;
    
    if (!cfnBucket.lifecycleConfiguration) {
      cfnBucket.lifecycleConfiguration = {
        rules: [{
          id: 'CostOptimization',
          status: 'Enabled',
          transitions: [
            {
              storageClass: 'INTELLIGENT_TIERING',
              transitionInDays: 0
            },
            {
              storageClass: 'GLACIER',
              transitionInDays: 30
            },
            {
              storageClass: 'DEEP_ARCHIVE',
              transitionInDays: 90
            }
          ],
          noncurrentVersionTransitions: [
            {
              storageClass: 'GLACIER',
              transitionInDays: 30
            }
          ],
          noncurrentVersionExpirationInDays: 365
        }]
      };
    }
  }
  
  private optimizeLambdaMemory(func: lambda.Function): void {
    const cfnFunction = func.node.defaultChild as lambda.CfnFunction;
    
    // Set reasonable defaults if not specified
    if (!cfnFunction.memorySize) {
      cfnFunction.memorySize = 256; // Good balance of cost vs performance
    }
    
    // Warn about potentially over-provisioned functions
    if (cfnFunction.memorySize && cfnFunction.memorySize > 1024) {
      console.warn(`Lambda function ${func.node.id} has high memory allocation (${cfnFunction.memorySize}MB). Consider optimizing.`);
    }
  }
}
```

**4. Compliance Validation Aspect**

```typescript
export interface ComplianceRule {
  name: string;
  check: (node: IConstruct) => boolean;
  fix?: (node: IConstruct) => void;
  severity: 'error' | 'warning' | 'info';
}

export class ComplianceValidationAspect implements IAspect {
  private violations: Array<{ rule: string, resource: string, severity: string }> = [];
  
  constructor(private rules: ComplianceRule[]) {}
  
  visit(node: IConstruct): void {
    this.rules.forEach(rule => {
      if (!rule.check(node)) {
        this.violations.push({
          rule: rule.name,
          resource: node.node.path,
          severity: rule.severity
        });
        
        // Apply automatic fix if available
        if (rule.fix) {
          rule.fix(node);
          console.log(`Auto-fixed compliance violation: ${rule.name} on ${node.node.path}`);
        } else {
          console.log(`Compliance violation: ${rule.name} on ${node.node.path} (${rule.severity})`);
        }
      }
    });
  }
  
  public getViolations(): Array<{ rule: string, resource: string, severity: string }> {
    return this.violations;
  }
  
  public hasErrors(): boolean {
    return this.violations.some(v => v.severity === 'error');
  }
}

// Define compliance rules
const securityRules: ComplianceRule[] = [
  {
    name: 'S3-ENCRYPTION-REQUIRED',
    check: (node) => {
      if (!(node instanceof s3.Bucket)) return true;
      const cfnBucket = node.node.defaultChild as s3.CfnBucket;
      return !!cfnBucket.bucketEncryption;
    },
    fix: (node) => {
      if (node instanceof s3.Bucket) {
        const cfnBucket = node.node.defaultChild as s3.CfnBucket;
        cfnBucket.bucketEncryption = {
          serverSideEncryptionConfiguration: [{
            serverSideEncryptionByDefault: {
              sseAlgorithm: 'AES256'
            }
          }]
        };
      }
    },
    severity: 'error'
  },
  {
    name: 'RDS-ENCRYPTION-REQUIRED',
    check: (node) => {
      if (!(node instanceof rds.DatabaseInstance)) return true;
      const cfnDb = node.node.defaultChild as rds.CfnDBInstance;
      return cfnDb.storageEncrypted === true;
    },
    fix: (node) => {
      if (node instanceof rds.DatabaseInstance) {
        const cfnDb = node.node.defaultChild as rds.CfnDBInstance;
        cfnDb.storageEncrypted = true;
      }
    },
    severity: 'error'
  },
  {
    name: 'LAMBDA-TIMEOUT-REASONABLE',
    check: (node) => {
      if (!(node instanceof lambda.Function)) return true;
      const cfnFunction = node.node.defaultChild as lambda.CfnFunction;
      return !cfnFunction.timeout || cfnFunction.timeout <= 300; // 5 minutes max
    },
    severity: 'warning'
  }
];

// Usage
const complianceAspect = new ComplianceValidationAspect(securityRules);
Aspects.of(app).add(complianceAspect);

// Check violations after synthesis
app.synth();
if (complianceAspect.hasErrors()) {
  throw new Error('Compliance violations found that must be fixed before deployment');
}
```

#### 🛠️ Hands-On Lab 3.3: Build Multi-Environment Compliance System

**Challenge**: Create a comprehensive aspect system that enforces different policies based on environment

**Your Mission**: Build aspects that automatically configure resources for dev/staging/prod environments with appropriate compliance rules.

**Requirements**:
1. **Environment Detection**: Automatically detect environment from stack name or context
2. **Policy Enforcement**: Different rules for different environments
3. **Cost Optimization**: Automatically optimize resources for non-production
4. **Security Baseline**: Ensure all resources meet security standards
5. **Reporting**: Generate compliance report after synthesis

**Implementation**:

```typescript
// aspects/environment-aware-aspect.ts
export interface EnvironmentConfig {
  readonly costOptimization: boolean;
  readonly securityLevel: 'basic' | 'enhanced' | 'strict';
  readonly complianceStandards: string[];
  readonly monitoringLevel: 'minimal' | 'standard' | 'comprehensive';
}

export class EnvironmentAwareAspect implements IAspect {
  private readonly environmentConfigs: Record<string, EnvironmentConfig> = {
    dev: {
      costOptimization: true,
      securityLevel: 'basic',
      complianceStandards: ['basic-security'],
      monitoringLevel: 'minimal'
    },
    staging: {
      costOptimization: true,
      securityLevel: 'enhanced',
      complianceStandards: ['basic-security', 'data-protection'],
      monitoringLevel: 'standard'
    },
    prod: {
      costOptimization: false,
      securityLevel: 'strict',
      complianceStandards: ['basic-security', 'data-protection', 'industry-specific'],
      monitoringLevel: 'comprehensive'
    }
  };
  
  constructor(private environment: string) {}
  
  visit(node: IConstruct): void {
    const config = this.environmentConfigs[this.environment];
    if (!config) {
      throw new Error(`Unknown environment: ${this.environment}`);
    }
    
    // Apply cost optimization
    if (config.costOptimization) {
      this.applyCostOptimization(node);
    }
    
    // Apply security policies
    this.applySecurityPolicies(node, config.securityLevel);
    
    // Apply monitoring
    this.applyMonitoring(node, config.monitoringLevel);
    
    // Apply compliance standards
    config.complianceStandards.forEach(standard => {
      this.applyComplianceStandard(node, standard);
    });
  }
  
  private applyCostOptimization(node: IConstruct): void {
    // Implementation for cost optimization
    if (node instanceof rds.DatabaseInstance) {
      const cfnDb = node.node.defaultChild as rds.CfnDBInstance;
      cfnDb.multiAz = false;
      cfnDb.backupRetentionPeriod = 1;
    }
    
    if (node instanceof ec2.Instance) {
      const cfnInstance = node.node.defaultChild as ec2.CfnInstance;
      // Switch to burstable instances
      if (cfnInstance.instanceType?.includes('m5')) {
        cfnInstance.instanceType = cfnInstance.instanceType.replace('m5', 't3');
      }
    }
  }
  
  private applySecurityPolicies(node: IConstruct, level: 'basic' | 'enhanced' | 'strict'): void {
    if (node instanceof s3.Bucket) {
      const cfnBucket = node.node.defaultChild as s3.CfnBucket;
      
      // Basic: Encryption
      if (level === 'basic' || level === 'enhanced' || level === 'strict') {
        cfnBucket.bucketEncryption = {
          serverSideEncryptionConfiguration: [{
            serverSideEncryptionByDefault: {
              sseAlgorithm: level === 'strict' ? 'aws:kms' : 'AES256'
            }
          }]
        };
      }
      
      // Enhanced: Versioning + Access Logging
      if (level === 'enhanced' || level === 'strict') {
        cfnBucket.versioningConfiguration = { status: 'Enabled' };
        cfnBucket.loggingConfiguration = {
          destinationBucketName: `access-logs-${node.node.addr}`,
          logFilePrefix: 'access-logs/'
        };
      }
      
      // Strict: MFA Delete + Notification
      if (level === 'strict') {
        cfnBucket.versioningConfiguration = { 
          status: 'Enabled',
          mfaDelete: 'Enabled'
        };
        cfnBucket.notificationConfiguration = {
          cloudWatchConfigurations: [{
            event: 's3:ObjectCreated:*',
            cloudWatchConfiguration: {
              logGroupName: `/aws/s3/${cfnBucket.bucketName || 'unknown'}`
            }
          }]
        };
      }
    }
  }
  
  private applyMonitoring(node: IConstruct, level: 'minimal' | 'standard' | 'comprehensive'): void {
    // Add CloudWatch alarms based on monitoring level
    if (node instanceof lambda.Function) {
      if (level === 'standard' || level === 'comprehensive') {
        new cloudwatch.Alarm(node, 'ErrorAlarm', {
          metric: node.metricErrors(),
          threshold: level === 'comprehensive' ? 1 : 5,
          evaluationPeriods: 2
        });
      }
      
      if (level === 'comprehensive') {
        new cloudwatch.Alarm(node, 'DurationAlarm', {
          metric: node.metricDuration(),
          threshold: 5000, // 5 seconds
          evaluationPeriods: 3
        });
        
        new cloudwatch.Alarm(node, 'ThrottleAlarm', {
          metric: node.metricThrottles(),
          threshold: 1,
          evaluationPeriods: 1
        });
      }
    }
  }
  
  private applyComplianceStandard(node: IConstruct, standard: string): void {
    // Implement specific compliance standards
    switch (standard) {
      case 'basic-security':
        this.applyBasicSecurityCompliance(node);
        break;
      case 'data-protection':
        this.applyDataProtectionCompliance(node);
        break;
      case 'industry-specific':
        this.applyIndustrySpecificCompliance(node);
        break;
    }
  }
  
  private applyBasicSecurityCompliance(node: IConstruct): void {
    // Implement basic security compliance
    if (node instanceof ec2.SecurityGroup) {
      const cfnSg = node.node.defaultChild as ec2.CfnSecurityGroup;
      
      // Check for overly permissive rules
      if (cfnSg.securityGroupIngress) {
        cfnSg.securityGroupIngress.forEach((rule: any) => {
          if (rule.cidrIp === '0.0.0.0/0' && rule.ipProtocol !== 'tcp') {
            console.warn(`Security Group ${node.node.id} has overly permissive rule`);
          }
        });
      }
    }
  }
  
  private applyDataProtectionCompliance(node: IConstruct): void {
    // Implement data protection compliance (GDPR, etc.)
    if (node instanceof dynamodb.Table) {
      const cfnTable = node.node.defaultChild as dynamodb.CfnTable;
      
      // Enforce encryption at rest
      if (!cfnTable.sseSpecification) {
        cfnTable.sseSpecification = {
          sseEnabled: true
        };
      }
      
      // Enable point-in-time recovery
      cfnTable.pointInTimeRecoveryEnabled = true;
    }
  }
  
  private applyIndustrySpecificCompliance(node: IConstruct): void {
    // Implement industry-specific compliance (PCI DSS, HIPAA, etc.)
    if (node instanceof rds.DatabaseInstance) {
      const cfnDb = node.node.defaultChild as rds.CfnDBInstance;
      
      // Enhanced backup and monitoring
      cfnDb.backupRetentionPeriod = 35; // Longer retention for compliance
      cfnDb.monitoringInterval = 60; // Enhanced monitoring
      cfnDb.performanceInsightsEnabled = true;
      cfnDb.deletionProtection = true;
    }
  }
}

// Usage in your CDK app
export class ComplianceApp extends App {
  constructor() {
    super();
    
    const environment = this.node.tryGetContext('environment') || 'dev';
    
    const stack = new ApplicationStack(this, `MyApp-${environment}`, {
      environment,
      // other props
    });
    
    // Apply environment-aware policies
    Aspects.of(this).add(new EnvironmentAwareAspect(environment));
    
    // Generate compliance report after synthesis
    this.generateComplianceReport();
  }
  
  private generateComplianceReport(): void {
    const originalSynth = this.synth;
    this.synth = (options?) => {
      const assembly = originalSynth.call(this, options);
      
      // Generate compliance report
      console.log('\n=== COMPLIANCE REPORT ===');
      console.log(`Environment: ${this.node.tryGetContext('environment')}`);
      console.log(`Timestamp: ${new Date().toISOString()}`);
      console.log('Resources reviewed for compliance');
      console.log('========================\n');
      
      return assembly;
    };
  }
}
```

**Success Criteria**:
- Aspects correctly detect and modify resources based on environment
- Cost optimizations apply only to non-production environments
- Security policies scale appropriately with environment criticality
- Compliance report generates with actionable information
- All tests pass and resources deploy successfully

---

## 📋 Module 3 Assessment

### Knowledge Check Quiz

**Question 1**: What's the primary benefit of construct composition over inheritance in CDK?
- a) Better performance
- b) Easier testing and reusability ✓
- c) Smaller bundle sizes
- d) Faster deployment

**Question 2**: When should you use CDK Aspects?
- a) Only for tagging resources
- b) For cross-cutting concerns across multiple constructs ✓
- c) Only for security policies
- d) Never, they're deprecated

**Question 3**: What TypeScript pattern is most useful for building configurable CDK constructs?
- a) Singleton pattern
- b) Observer pattern
- c) Builder pattern ✓
- d) Adapter pattern

### Practical Assessment: Advanced Infrastructure Library

**Capstone Project**: Build a complete, production-ready CDK construct library

**Requirements**:

1. **Multi-Tier Web Application Pattern**
   - Frontend (S3 + CloudFront)
   - API Layer (API Gateway + Lambda)
   - Data Layer (DynamoDB or RDS)
   - Monitoring (CloudWatch + Alarms)

2. **Advanced TypeScript Features**
   - Generic constructs with type safety
   - Fluent interface for configuration
   - Decorator pattern for capabilities
   - Factory pattern for environment-specific resources

3. **CDK Aspects Integration**
   - Security compliance aspect
   - Cost optimization aspect
   - Monitoring aspect
   - Custom validation aspect

4. **Testing Suite**
   - Unit tests for all constructs
   - Integration tests with CDK assertions
   - Snapshot tests for CloudFormation templates
   - Performance tests for synthesis time

5. **Documentation and Distribution**
   - TypeDoc documentation
   - README with examples
   - NPM package configuration
   - Semantic versioning

**Example Implementation Structure**:

```typescript
// lib/patterns/web-application-pattern.ts
export class WebApplicationPattern extends Construct {
  public readonly frontend: StaticWebsite;
  public readonly api: RestApiConstruct;
  public readonly database: IDatabaseConstruct;
  public readonly monitoring: MonitoringConstruct;
  
  constructor(scope: Construct, id: string, props: WebApplicationPatternProps) {
    super(scope, id);
    
    // Build application using composition
    this.frontend = new StaticWebsite(this, 'Frontend', props.frontendConfig);
    this.api = new RestApiConstruct(this, 'API', props.apiConfig);
    this.database = this.createDatabase(props.databaseConfig);
    this.monitoring = new MonitoringConstruct(this, 'Monitoring', {
      targets: [this.frontend, this.api, this.database]
    });
    
    // Wire components together
    this.wireComponents();
  }
  
  private createDatabase(config: DatabaseConfig): IDatabaseConstruct {
    const factory = new DatabaseFactory();
    return factory.create(this, 'Database', config);
  }
  
  private wireComponents(): void {
    // Connect API to database
    this.database.grantReadWriteData(this.api.executionRole);
    
    // Configure CORS for frontend
    this.api.addCorsConfiguration({
      allowOrigins: [this.frontend.distributionDomainName]
    });
  }
}

// Usage with fluent interface and aspects
const app = new App();

const webApp = new WebApplicationPatternBuilder()
  .withFrontend({
    domainName: 'example.com',
    sources: ['./dist']
  })
  .withApi({
    routes: [
      { path: '/users', methods: ['GET', 'POST'], handler: userHandler },
      { path: '/users/{id}', methods: ['GET', 'PUT', 'DELETE'], handler: userDetailHandler }
    ]
  })
  .withDatabase({
    type: 'dynamodb',
    tables: [
      { name: 'users', partitionKey: 'userId' }
    ]
  })
  .withMonitoring({
    level: 'comprehensive',
    alertEmail: 'ops@example.com'
  })
  .build(stack, 'WebApp');

// Apply aspects
Aspects.of(app).add(new SecurityComplianceAspect());
Aspects.of(app).add(new CostOptimizationAspect('production'));
Aspects.of(app).add(new MonitoringAspect('comprehensive'));
```

**Validation Criteria**:
- ✅ Library compiles without TypeScript errors
- ✅ All unit tests pass with >80% coverage
- ✅ Integration tests deploy and tear down successfully
- ✅ Aspects correctly modify resources
- ✅ Documentation is comprehensive and accurate
- ✅ Package can be published to NPM registry
- ✅ Performance meets benchmarks (synthesis < 30 seconds)
- ✅ Real deployment works in AWS account

**💰 Cost Warning**: Full deployment ~$2-5/day. Deploy → validate → destroy within same day!

---

## 🚀 Ready for Module 4?

**Before proceeding, ensure you can:**
- ✅ Compose complex infrastructure from smaller, reusable constructs
- ✅ Create custom CDK constructs with proper TypeScript typing
- ✅ Implement and apply CDK Aspects for cross-cutting concerns
- ✅ Use advanced TypeScript patterns in infrastructure code
- ✅ Build testable, maintainable construct libraries

**Next Up**: [Module 4: CDK TypeScript Data Flow & Event-Driven Patterns](/learning-plans/cdk-typescript/module-4)

---

## 💡 Reflection Prompts

1. **How do composition patterns change your approach to infrastructure design compared to monolithic CloudFormation templates?**

2. **What are the key TypeScript features that make CDK constructs more powerful than traditional infrastructure tools?**

3. **How would you architect a construct library for a team of 10+ developers working on microservices?**

4. **What's the most valuable use case for CDK Aspects in your organization?**

---

*You've now mastered the advanced patterns that separate CDK beginners from CDK experts! Your constructs are composable, your TypeScript is sophisticated, and your aspects ensure consistency across your entire infrastructure. Time to tackle complex data flows and event-driven architectures! 🏗️*