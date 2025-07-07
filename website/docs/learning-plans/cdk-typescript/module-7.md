# Module 7: CDK TypeScript Mastery & Enterprise Patterns
*"Advanced CDK wizardry that won't make your enterprise architecture review board break out in hives"*

> **Duration**: 2-3 weeks  
> **Cost**: ~$5-15/day while running (enterprise patterns require proper testing, but we'll be smart about it)  
> **Prerequisites**: Modules 1-6 completed, understanding that enterprise software is like a game of Jenga played by people wearing oven mitts

---

## 🎯 Module Learning Objectives

By the end of this module, you will:
- **Master CDK Construct Libraries** and publish reusable infrastructure components
- **Implement Advanced TypeScript patterns** specific to enterprise CDK development
- **Build Cross-Account and Cross-Region** deployment strategies that actually work
- **Create Custom CDK CLI tools** for your organization's specific needs
- **Optimize CDK performance** for large-scale enterprise applications
- **Design for compliance** in regulated industries without losing your sanity

---

## 📚 Core Lessons

### Lesson 7.1: Advanced CDK Construct Libraries & Distribution
*"Building infrastructure Lego blocks that your colleagues will actually want to use"*

#### The Art of Building Reusable Infrastructure

Creating construct libraries is like writing a cookbook - anyone can throw ingredients together, but making something others actually want to use requires skill, taste, and an understanding that your colleagues have different needs than you do.

**Enterprise-Grade Construct Library Architecture**

```typescript
// ❌ The "I built this for me" approach
export class MyRandomConstruct extends Construct {
  constructor(scope: Construct, id: string, config: any) {
    super(scope, id);
    
    // Hardcoded values because "it works for my use case"
    new s3.Bucket(this, 'Bucket', {
      bucketName: 'my-specific-bucket-name'
    });
    
    new lambda.Function(this, 'Function', {
      runtime: lambda.Runtime.NODEJS_14_X, // Outdated runtime
      handler: 'index.handler',
      code: lambda.Code.fromInline('exports.handler = () => "hello";')
    });
  }
}

// ✅ The "I built this for everyone" approach
export interface SecureDataProcessingPlatformProps {
  /**
   * The environment this platform is being deployed to.
   * This affects resource sizing, security settings, and cost optimization.
   */
  readonly environment: 'dev' | 'staging' | 'prod';
  
  /**
   * Name of the application using this platform.
   * Used for resource naming and tagging.
   */
  readonly applicationName: string;
  
  /**
   * VPC where the platform will be deployed.
   * If not provided, a new VPC will be created.
   */
  readonly vpc?: ec2.IVpc;
  
  /**
   * Data classification level for compliance.
   * Affects encryption, logging, and access controls.
   */
  readonly dataClassification: 'public' | 'internal' | 'confidential' | 'restricted';
  
  /**
   * Compliance standards this platform must meet.
   * Each standard enables specific security controls.
   */
  readonly complianceStandards: ('SOC2' | 'HIPAA' | 'PCI' | 'FedRAMP')[];
  
  /**
   * Processing capacity configuration.
   * Auto-calculated based on environment if not specified.
   */
  readonly processingConfig?: ProcessingCapacityConfig;
  
  /**
   * Data retention policies.
   * Defaults based on compliance standards if not specified.
   */
  readonly dataRetention?: DataRetentionConfig;
  
  /**
   * Monitoring and alerting configuration.
   * Required for production deployments.
   */
  readonly monitoringConfig: MonitoringConfig;
  
  /**
   * Cost optimization settings.
   * Balances performance with cost based on environment.
   */
  readonly costOptimization?: CostOptimizationConfig;
}

/**
 * A comprehensive data processing platform that handles enterprise requirements
 * out of the box, including compliance, security, monitoring, and cost optimization.
 * 
 * This construct abstracts away the complexity of setting up a secure,
 * scalable data processing infrastructure while providing the flexibility
 * to customize for specific use cases.
 * 
 * Features:
 * - Automatic compliance configuration based on standards
 * - Environment-appropriate resource sizing
 * - Built-in monitoring and alerting
 * - Cost optimization strategies
 * - Multi-region deployment support
 * - Zero-downtime deployment patterns
 * 
 * @example
 * ```typescript
 * const platform = new SecureDataProcessingPlatform(this, 'DataPlatform', {
 *   environment: 'prod',
 *   applicationName: 'financial-analytics',
 *   dataClassification: 'confidential',
 *   complianceStandards: ['SOC2', 'PCI'],
 *   monitoringConfig: {
 *     alertEmail: 'ops@company.com',
 *     dashboardName: 'financial-analytics-prod'
 *   }
 * });
 * ```
 */
export class SecureDataProcessingPlatform extends Construct {
  /**
   * The VPC where all platform resources are deployed
   */
  public readonly vpc: ec2.IVpc;
  
  /**
   * The primary data processing queue
   */
  public readonly processingQueue: sqs.Queue;
  
  /**
   * The dead letter queue for failed processing jobs
   */
  public readonly deadLetterQueue: sqs.Queue;
  
  /**
   * The S3 bucket for input data
   */
  public readonly inputBucket: s3.Bucket;
  
  /**
   * The S3 bucket for processed output data
   */
  public readonly outputBucket: s3.Bucket;
  
  /**
   * The Lambda function that processes data
   */
  public readonly processingFunction: lambda.Function;
  
  /**
   * The DynamoDB table for job metadata
   */
  public readonly metadataTable: dynamodb.Table;
  
  /**
   * CloudWatch dashboard for monitoring
   */
  public readonly dashboard: cloudwatch.Dashboard;
  
  /**
   * SNS topic for alerts
   */
  public readonly alertTopic: sns.Topic;
  
  private readonly props: SecureDataProcessingPlatformProps;
  private readonly config: ResolvedPlatformConfig;
  
  constructor(scope: Construct, id: string, props: SecureDataProcessingPlatformProps) {
    super(scope, id);
    
    this.props = props;
    this.config = this.resolveConfiguration(props);
    
    // Validate configuration
    this.validateConfiguration();
    
    // Set up VPC
    this.vpc = this.setupNetworking();
    
    // Create storage components
    this.inputBucket = this.createInputBucket();
    this.outputBucket = this.createOutputBucket();
    this.metadataTable = this.createMetadataTable();
    
    // Create processing components
    this.deadLetterQueue = this.createDeadLetterQueue();
    this.processingQueue = this.createProcessingQueue();
    this.processingFunction = this.createProcessingFunction();
    
    // Set up monitoring
    this.alertTopic = this.createAlertTopic();
    this.dashboard = this.createDashboard();
    
    // Apply compliance controls
    this.applyComplianceControls();
    
    // Apply cost optimization
    this.applyCostOptimization();
    
    // Apply standard tags
    this.applyTags();
    
    // Create outputs
    this.createOutputs();
  }
  
  /**
   * Resolve and validate the complete configuration for this platform
   */
  private resolveConfiguration(props: SecureDataProcessingPlatformProps): ResolvedPlatformConfig {
    const baseConfig = ConfigurationResolver.getBaseConfiguration(props.environment);
    const complianceConfig = ConfigurationResolver.getComplianceConfiguration(props.complianceStandards);
    const dataClassificationConfig = ConfigurationResolver.getDataClassificationConfiguration(props.dataClassification);
    
    return {
      ...baseConfig,
      ...complianceConfig,
      ...dataClassificationConfig,
      processingConfig: props.processingConfig || this.getDefaultProcessingConfig(props.environment),
      dataRetention: props.dataRetention || this.getDefaultDataRetention(props.complianceStandards),
      costOptimization: props.costOptimization || this.getDefaultCostOptimization(props.environment)
    };
  }
  
  private validateConfiguration(): void {
    // Validate environment-specific requirements
    if (this.props.environment === 'prod') {
      if (!this.props.monitoringConfig.alertEmail) {
        throw new Error('Production deployments require alertEmail in monitoringConfig');
      }
      
      if (this.props.dataClassification === 'restricted' && !this.props.complianceStandards.includes('FedRAMP')) {
        throw new Error('Restricted data classification requires FedRAMP compliance in production');
      }
    }
    
    // Validate compliance combinations
    if (this.props.complianceStandards.includes('HIPAA') && this.props.dataClassification === 'public') {
      throw new Error('HIPAA compliance is incompatible with public data classification');
    }
    
    // Validate cost optimization settings
    if (this.config.costOptimization?.aggressiveCostOptimization && this.props.environment === 'prod') {
      console.warn('Aggressive cost optimization enabled in production - monitor performance carefully');
    }
  }
  
  private setupNetworking(): ec2.IVpc {
    if (this.props.vpc) {
      return this.props.vpc;
    }
    
    // Create VPC with compliance-appropriate configuration
    const vpcConfig = this.config.networkingConfig;
    
    return new ec2.Vpc(this, 'PlatformVpc', {
      maxAzs: vpcConfig.maxAzs,
      natGateways: vpcConfig.natGateways,
      enableDnsHostnames: true,
      enableDnsSupport: true,
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
        },
        {
          name: 'isolated',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
          cidrMask: 24
        }
      ],
      flowLogs: vpcConfig.enableFlowLogs ? {
        trafficType: ec2.FlowLogTrafficType.ALL,
        destination: ec2.FlowLogDestination.toCloudWatchLogs(
          new logs.LogGroup(this, 'VpcFlowLogs', {
            retention: logs.RetentionDays.ONE_MONTH
          })
        )
      } : undefined
    });
  }
  
  private createInputBucket(): s3.Bucket {
    const bucketProps = this.getBucketConfiguration('input');
    
    return new s3.Bucket(this, 'InputBucket', {
      bucketName: `${this.props.applicationName}-input-${this.props.environment}-${this.account}`.toLowerCase(),
      ...bucketProps,
      
      // Input-specific configuration
      eventBridgeEnabled: true,
      notifications: [{
        type: s3.EventType.OBJECT_CREATED,
        destination: new s3n.SqsDestination(this.processingQueue)
      }],
      
      // Lifecycle rules for input data
      lifecycleRules: [{
        id: 'InputDataLifecycle',
        enabled: true,
        transitions: this.config.dataRetention.inputDataTransitions,
        expiration: this.config.dataRetention.inputDataExpiration
      }]
    });
  }
  
  private createOutputBucket(): s3.Bucket {
    const bucketProps = this.getBucketConfiguration('output');
    
    return new s3.Bucket(this, 'OutputBucket', {
      bucketName: `${this.props.applicationName}-output-${this.props.environment}-${this.account}`.toLowerCase(),
      ...bucketProps,
      
      // Output-specific configuration
      lifecycleRules: [{
        id: 'OutputDataLifecycle',
        enabled: true,
        transitions: this.config.dataRetention.outputDataTransitions,
        expiration: this.config.dataRetention.outputDataExpiration
      }]
    });
  }
  
  private getBucketConfiguration(bucketType: 'input' | 'output'): Partial<s3.BucketProps> {
    const baseConfig: Partial<s3.BucketProps> = {
      encryption: this.config.encryptionConfig.s3EncryptionType,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      versioned: this.config.complianceConfig.enableVersioning,
      enforceSSL: true
    };
    
    // Add compliance-specific configurations
    if (this.props.complianceStandards.includes('SOC2')) {
      Object.assign(baseConfig, {
        serverAccessLogsPrefix: `access-logs/${bucketType}/`,
        objectOwnership: s3.ObjectOwnership.BUCKET_OWNER_ENFORCED
      });
    }
    
    if (this.props.complianceStandards.includes('HIPAA')) {
      Object.assign(baseConfig, {
        encryption: s3.BucketEncryption.KMS_MANAGED,
        bucketKeyEnabled: true
      });
    }
    
    if (this.props.dataClassification === 'restricted') {
      Object.assign(baseConfig, {
        encryption: s3.BucketEncryption.KMS_MANAGED,
        objectLockEnabled: true,
        objectLockDefaultRetention: {
          mode: s3.ObjectLockRetentionMode.COMPLIANCE,
          duration: Duration.years(7)
        }
      });
    }
    
    return baseConfig;
  }
  
  private createProcessingFunction(): lambda.Function {
    const functionConfig = this.config.processingConfig;
    
    return new lambda.Function(this, 'ProcessingFunction', {
      functionName: `${this.props.applicationName}-processor-${this.props.environment}`,
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/data-processor')),
      
      // Resource allocation based on environment and config
      memorySize: functionConfig.memorySize,
      timeout: functionConfig.timeout,
      reservedConcurrencyExecutions: functionConfig.reservedConcurrency,
      
      // Environment variables
      environment: {
        INPUT_BUCKET: this.inputBucket.bucketName,
        OUTPUT_BUCKET: this.outputBucket.bucketName,
        METADATA_TABLE: this.metadataTable.tableName,
        ENVIRONMENT: this.props.environment,
        DATA_CLASSIFICATION: this.props.dataClassification,
        LOG_LEVEL: this.config.loggingConfig.level
      },
      
      // VPC configuration for compliance
      vpc: this.config.complianceConfig.requireVpcIsolation ? this.vpc : undefined,
      vpcSubnets: this.config.complianceConfig.requireVpcIsolation ? {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED
      } : undefined,
      
      // Security configuration
      tracing: lambda.Tracing.ACTIVE,
      logRetention: this.config.loggingConfig.retention,
      
      // Dead letter queue
      deadLetterQueue: this.deadLetterQueue,
      
      // Error handling
      retryAttempts: 2
    });
  }
  
  private applyComplianceControls(): void {
    // Apply CDK Aspects for compliance
    if (this.props.complianceStandards.includes('SOC2')) {
      Aspects.of(this).add(new SOC2ComplianceAspect());
    }
    
    if (this.props.complianceStandards.includes('HIPAA')) {
      Aspects.of(this).add(new HIPAAComplianceAspect());
    }
    
    if (this.props.complianceStandards.includes('PCI')) {
      Aspects.of(this).add(new PCIComplianceAspect());
    }
    
    if (this.props.complianceStandards.includes('FedRAMP')) {
      Aspects.of(this).add(new FedRAMPComplianceAspect());
    }
  }
  
  private applyCostOptimization(): void {
    if (this.config.costOptimization?.enableCostOptimization) {
      Aspects.of(this).add(new CostOptimizationAspect(this.config.costOptimization));
    }
  }
  
  private applyTags(): void {
    const tags = {
      Application: this.props.applicationName,
      Environment: this.props.environment,
      DataClassification: this.props.dataClassification,
      ComplianceStandards: this.props.complianceStandards.join(','),
      ManagedBy: 'SecureDataProcessingPlatform',
      CostCenter: this.config.costOptimization?.costCenter || 'unknown',
      Owner: this.config.organizationConfig?.owner || 'unknown'
    };
    
    Object.entries(tags).forEach(([key, value]) => {
      Tags.of(this).add(key, value);
    });
  }
  
  // ... Additional methods for monitoring, outputs, etc.
}

/**
 * Configuration resolver that handles complex enterprise configuration logic
 */
export class ConfigurationResolver {
  static getBaseConfiguration(environment: string): BaseConfiguration {
    const configs: Record<string, BaseConfiguration> = {
      dev: {
        networkingConfig: {
          maxAzs: 2,
          natGateways: 1,
          enableFlowLogs: false
        },
        loggingConfig: {
          level: 'DEBUG',
          retention: logs.RetentionDays.ONE_WEEK
        },
        encryptionConfig: {
          s3EncryptionType: s3.BucketEncryption.S3_MANAGED
        }
      },
      staging: {
        networkingConfig: {
          maxAzs: 2,
          natGateways: 2,
          enableFlowLogs: true
        },
        loggingConfig: {
          level: 'INFO',
          retention: logs.RetentionDays.TWO_WEEKS
        },
        encryptionConfig: {
          s3EncryptionType: s3.BucketEncryption.KMS_MANAGED
        }
      },
      prod: {
        networkingConfig: {
          maxAzs: 3,
          natGateways: 3,
          enableFlowLogs: true
        },
        loggingConfig: {
          level: 'WARN',
          retention: logs.RetentionDays.ONE_MONTH
        },
        encryptionConfig: {
          s3EncryptionType: s3.BucketEncryption.KMS_MANAGED
        }
      }
    };
    
    return configs[environment] || configs.dev;
  }
  
  static getComplianceConfiguration(standards: string[]): ComplianceConfiguration {
    const config: ComplianceConfiguration = {
      enableVersioning: false,
      requireVpcIsolation: false,
      enableAuditLogging: false,
      enableEncryptionAtRest: false,
      enableEncryptionInTransit: false
    };
    
    // SOC2 requirements
    if (standards.includes('SOC2')) {
      config.enableVersioning = true;
      config.enableAuditLogging = true;
      config.enableEncryptionAtRest = true;
    }
    
    // HIPAA requirements
    if (standards.includes('HIPAA')) {
      config.enableVersioning = true;
      config.requireVpcIsolation = true;
      config.enableAuditLogging = true;
      config.enableEncryptionAtRest = true;
      config.enableEncryptionInTransit = true;
    }
    
    // PCI requirements
    if (standards.includes('PCI')) {
      config.enableVersioning = true;
      config.requireVpcIsolation = true;
      config.enableAuditLogging = true;
      config.enableEncryptionAtRest = true;
      config.enableEncryptionInTransit = true;
    }
    
    // FedRAMP requirements (most stringent)
    if (standards.includes('FedRAMP')) {
      config.enableVersioning = true;
      config.requireVpcIsolation = true;
      config.enableAuditLogging = true;
      config.enableEncryptionAtRest = true;
      config.enableEncryptionInTransit = true;
      config.requireDedicatedTenancy = true;
    }
    
    return config;
  }
  
  static getDataClassificationConfiguration(classification: string): DataClassificationConfiguration {
    const configs: Record<string, DataClassificationConfiguration> = {
      public: {
        encryptionRequired: false,
        accessLoggingRequired: false,
        auditTrailRequired: false
      },
      internal: {
        encryptionRequired: true,
        accessLoggingRequired: true,
        auditTrailRequired: false
      },
      confidential: {
        encryptionRequired: true,
        accessLoggingRequired: true,
        auditTrailRequired: true
      },
      restricted: {
        encryptionRequired: true,
        accessLoggingRequired: true,
        auditTrailRequired: true,
        immutableStorageRequired: true,
        dedicatedInfrastructureRequired: true
      }
    };
    
    return configs[classification] || configs.internal;
  }
}
```

**Publishing and Versioning Strategy**

```typescript
// Package.json for construct library
{
  "name": "@yourorg/secure-data-processing-platform",
  "version": "1.0.0",
  "description": "Enterprise-grade secure data processing platform for AWS CDK",
  "main": "lib/index.js",
  "types": "lib/index.d.ts",
  "scripts": {
    "build": "tsc",
    "watch": "tsc -w",
    "test": "jest",
    "test:update": "jest -u",
    "package": "jsii-pacmak",
    "eslint": "eslint . --ext .ts --max-warnings 0",
    "bump": "standard-version",
    "release": "npm run build && npm run test && npm run package && npm publish"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/yourorg/secure-data-processing-platform.git"
  },
  "keywords": [
    "aws",
    "cdk",
    "constructs",
    "data-processing",
    "security",
    "compliance",
    "enterprise"
  ],
  "author": "Your Organization",
  "license": "Apache-2.0",
  "peerDependencies": {
    "aws-cdk-lib": "^2.80.0",
    "constructs": "^10.0.0"
  },
  "devDependencies": {
    "@types/jest": "^29.5.0",
    "@types/node": "^18.15.0",
    "@typescript-eslint/eslint-plugin": "^5.57.0",
    "@typescript-eslint/parser": "^5.57.0",
    "aws-cdk-lib": "^2.80.0",
    "constructs": "^10.0.0",
    "eslint": "^8.37.0",
    "jest": "^29.5.0",
    "jsii": "^5.0.0",
    "jsii-pacmak": "^1.80.0",
    "standard-version": "^9.5.0",
    "ts-jest": "^29.1.0",
    "typescript": "^5.0.0"
  },
  "jsii": {
    "outdir": "dist",
    "targets": {
      "python": {
        "distName": "yourorg.secure-data-processing-platform",
        "module": "yourorg_secure_data_processing_platform"
      },
      "java": {
        "package": "com.yourorg.securedataprocessingplatform",
        "maven": {
          "groupId": "com.yourorg",
          "artifactId": "secure-data-processing-platform"
        }
      },
      "dotnet": {
        "namespace": "YourOrg.SecureDataProcessingPlatform",
        "packageId": "YourOrg.SecureDataProcessingPlatform"
      }
    }
  },
  "stability": "stable"
}

// .projenrc.js for advanced project management
const { awscdk } = require('projen');

const project = new awscdk.AwsCdkConstructLibrary({
  author: 'Your Organization',
  authorAddress: 'engineering@yourorg.com',
  cdkVersion: '2.80.0',
  defaultReleaseBranch: 'main',
  name: '@yourorg/secure-data-processing-platform',
  repositoryUrl: 'https://github.com/yourorg/secure-data-processing-platform.git',
  
  // TypeScript configuration
  tsconfig: {
    compilerOptions: {
      strict: true,
      noImplicitAny: true,
      strictNullChecks: true,
      noImplicitThis: true,
      alwaysStrict: true,
      noUnusedLocals: true,
      noUnusedParameters: true,
      noImplicitReturns: true,
      noFallthroughCasesInSwitch: true
    }
  },
  
  // Testing configuration
  jestOptions: {
    jestConfig: {
      testEnvironment: 'node',
      collectCoverageFrom: [
        'src/**/*.ts',
        '!src/**/*.d.ts'
      ],
      coverageThreshold: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80
        }
      }
    }
  },
  
  // Publishing configuration
  publishToPypi: {
    distName: 'yourorg-secure-data-processing-platform',
    module: 'yourorg_secure_data_processing_platform'
  },
  publishToMaven: {
    javaPackage: 'com.yourorg.securedataprocessingplatform',
    mavenGroupId: 'com.yourorg',
    mavenArtifactId: 'secure-data-processing-platform'
  },
  publishToNuget: {
    dotNetNamespace: 'YourOrg.SecureDataProcessingPlatform',
    packageId: 'YourOrg.SecureDataProcessingPlatform'
  },
  
  // Dependencies
  deps: [
    'aws-cdk-lib@^2.80.0',
    'constructs@^10.0.0'
  ],
  devDeps: [
    '@types/jest',
    'aws-cdk-lib',
    'constructs'
  ],
  
  // Release configuration
  releaseToNpm: true,
  npmAccess: 'restricted', // For private org packages
  
  // Documentation
  docgen: true,
  docsDirectory: 'docs',
  
  // Code quality
  eslint: true,
  prettier: true,
  
  // GitHub workflows
  buildWorkflow: true,
  releaseWorkflow: true,
  
  // Additional files
  gitignore: [
    '*.log',
    '.env',
    '.vscode/',
    'cdk.out/',
    'dist/',
    'temp/'
  ]
});

// Add custom tasks
project.addTask('docs:generate', {
  description: 'Generate API documentation',
  exec: 'typedoc --out docs src/index.ts'
});

project.addTask('security:audit', {
  description: 'Run security audit',
  exec: 'npm audit && npm run eslint'
});

project.addTask('validate:constructs', {
  description: 'Validate construct implementations',
  exec: 'npm run build && npm run test && npm run package'
});

project.synth();
```

#### 🛠️ Hands-On Lab 7.1: Build and Publish an Enterprise Construct Library

**Challenge**: Create a complete, publishable construct library for your organization

**Your Mission**: Build a construct library that includes:
1. **Multi-tier Web Application** construct with configurable environments
2. **Compliance-ready Data Platform** with built-in security controls
3. **Monitoring and Alerting** constructs with organization-specific defaults
4. **Cost Optimization** aspects that apply across all constructs
5. **Custom CDK CLI commands** for common organizational tasks

**Enterprise Requirements**:
- Support multiple compliance standards (SOC2, HIPAA, PCI)
- Environment-specific configurations (dev/staging/prod)
- Comprehensive TypeScript documentation with examples
- Unit and integration test suite with >90% coverage
- Multi-language support (TypeScript, Python, Java)
- Semantic versioning with automated releases

**Success Criteria**:
- Library compiles and publishes to multiple package managers
- All constructs have comprehensive documentation and examples
- Test suite covers edge cases and error conditions
- Constructs work correctly in real AWS deployments
- Breaking changes are properly versioned and documented
- Performance meets enterprise-scale requirements

**💰 Cost Warning**: Testing enterprise constructs costs ~$5-10/day. Use integration test environments efficiently!

---

### Lesson 7.2: Advanced TypeScript Patterns for Large-Scale CDK
*"TypeScript patterns that scale from 'my little hobby project' to 'enterprise behemoth'"*

#### Generic Constructs and Advanced Type Safety

When you're building infrastructure for an organization with hundreds of developers, type safety isn't just nice to have - it's the difference between smooth deployments and emergency meetings with very angry people.

**Advanced Generic Patterns for CDK**

```typescript
// Type-safe resource factory pattern
export interface ResourceFactory<TResource, TProps> {
  create(scope: Construct, id: string, props: TProps): TResource;
  validate(props: TProps): ValidationResult;
  getDefaultProps(environment: Environment): Partial<TProps>;
}

export class TypeSafeResourceManager<TResource extends Construct, TProps> {
  private factories = new Map<string, ResourceFactory<TResource, TProps>>();
  private validators = new Map<string, PropsValidator<TProps>>();
  
  registerFactory(resourceType: string, factory: ResourceFactory<TResource, TProps>): void {
    this.factories.set(resourceType, factory);
  }
  
  registerValidator(resourceType: string, validator: PropsValidator<TProps>): void {
    this.validators.set(resourceType, validator);
  }
  
  createResource(
    scope: Construct,
    id: string,
    resourceType: string,
    props: TProps
  ): TResource {
    const factory = this.factories.get(resourceType);
    if (!factory) {
      throw new Error(`No factory registered for resource type: ${resourceType}`);
    }
    
    // Validate props before creation
    const validator = this.validators.get(resourceType);
    if (validator) {
      const validationResult = validator.validate(props);
      if (!validationResult.isValid) {
        throw new Error(`Invalid props for ${resourceType}: ${validationResult.errors.join(', ')}`);
      }
    }
    
    // Create resource with factory
    return factory.create(scope, id, props);
  }
}

// Advanced conditional type patterns
export type EnvironmentSpecificProps<TEnvironment extends Environment> = 
  TEnvironment extends 'prod' 
    ? ProductionRequiredProps
    : TEnvironment extends 'staging'
    ? StagingRequiredProps  
    : DevelopmentRequiredProps;

export type ComplianceRequiredProps<TCompliance extends ComplianceStandard[]> = {
  [K in TCompliance[number]]: K extends 'HIPAA'
    ? HIPAARequiredProps
    : K extends 'SOC2'
    ? SOC2RequiredProps
    : K extends 'PCI'
    ? PCIRequiredProps
    : never;
};

// Utility types for better developer experience
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type RequiredKeys<T, K extends keyof T> = T & Required<Pick<T, K>>;

export type ConditionalProps<TCondition extends boolean, TTrueProps, TFalseProps = {}> =
  TCondition extends true ? TTrueProps : TFalseProps;

// Advanced construct with conditional typing
export interface SmartInfrastructureProps<
  TEnvironment extends Environment = Environment,
  TCompliance extends ComplianceStandard[] = ComplianceStandard[],
  TEnableAdvancedFeatures extends boolean = false
> {
  readonly environment: TEnvironment;
  readonly complianceStandards: TCompliance;
  readonly applicationName: string;
  readonly enableAdvancedFeatures?: TEnableAdvancedFeatures;
  
  // Environment-specific props
  readonly environmentConfig: EnvironmentSpecificProps<TEnvironment>;
  
  // Compliance-specific props
  readonly complianceConfig: ComplianceRequiredProps<TCompliance>;
  
  // Conditional advanced features
  readonly advancedFeatures?: ConditionalProps<
    TEnableAdvancedFeatures,
    AdvancedFeaturesConfig,
    never
  >;
}

export class SmartInfrastructure<
  TEnvironment extends Environment = Environment,
  TCompliance extends ComplianceStandard[] = ComplianceStandard[],
  TEnableAdvancedFeatures extends boolean = false
> extends Construct {
  
  constructor(
    scope: Construct,
    id: string,
    props: SmartInfrastructureProps<TEnvironment, TCompliance, TEnableAdvancedFeatures>
  ) {
    super(scope, id);
    
    // Type-safe environment handling
    this.setupEnvironmentSpecificResources(props.environmentConfig);
    
    // Type-safe compliance handling
    this.setupComplianceResources(props.complianceConfig);
    
    // Conditional advanced features with type safety
    if (props.enableAdvancedFeatures && props.advancedFeatures) {
      this.setupAdvancedFeatures(props.advancedFeatures);
    }
  }
  
  private setupEnvironmentSpecificResources(config: EnvironmentSpecificProps<TEnvironment>): void {
    // TypeScript knows the exact type of config based on TEnvironment
    // This enables IntelliSense and compile-time validation
  }
  
  private setupComplianceResources(config: ComplianceRequiredProps<TCompliance>): void {
    // TypeScript enforces that all required compliance props are present
  }
  
  private setupAdvancedFeatures(config: AdvancedFeaturesConfig): void {
    // Only called when enableAdvancedFeatures is true
  }
}

// Usage examples with full type safety
const prodInfra = new SmartInfrastructure(this, 'ProdInfra', {
  environment: 'prod', // TypeScript knows this is specifically 'prod'
  complianceStandards: ['SOC2', 'HIPAA'],
  applicationName: 'secure-app',
  enableAdvancedFeatures: true,
  
  environmentConfig: {
    // TypeScript requires ProductionRequiredProps here
    instanceClass: 'r5.large',
    multiAz: true, // Required for prod
    backupRetention: 30 // Required for prod
  },
  
  complianceConfig: {
    SOC2: {
      enableAuditLogging: true,
      enableEncryption: true
    },
    HIPAA: {
      enableVpcIsolation: true,
      enableEncryption: true,
      enableAccessLogging: true
    }
  },
  
  advancedFeatures: {
    // TypeScript knows this is available because enableAdvancedFeatures is true
    enableAIOptimization: true,
    enablePredictiveScaling: true
  }
});
```

**Plugin Architecture for Extensibility**

```typescript
// Plugin interface for extensible CDK constructs
export interface CDKPlugin<TConfig = any> {
  readonly name: string;
  readonly version: string;
  readonly dependencies?: string[];
  
  initialize(construct: Construct, config: TConfig): void;
  validate(config: TConfig): ValidationResult;
  getDefaultConfig(): TConfig;
}

export class PluginManager {
  private plugins = new Map<string, CDKPlugin>();
  private loadedPlugins = new Set<string>();
  
  registerPlugin<TConfig>(plugin: CDKPlugin<TConfig>): void {
    // Validate plugin dependencies
    if (plugin.dependencies) {
      for (const dep of plugin.dependencies) {
        if (!this.plugins.has(dep)) {
          throw new Error(`Plugin ${plugin.name} requires dependency ${dep} which is not registered`);
        }
      }
    }
    
    this.plugins.set(plugin.name, plugin);
  }
  
  loadPlugin<TConfig>(
    construct: Construct,
    pluginName: string,
    config: TConfig
  ): void {
    const plugin = this.plugins.get(pluginName);
    if (!plugin) {
      throw new Error(`Plugin ${pluginName} is not registered`);
    }
    
    // Load dependencies first
    if (plugin.dependencies) {
      for (const dep of plugin.dependencies) {
        if (!this.loadedPlugins.has(dep)) {
          this.loadPlugin(construct, dep, this.plugins.get(dep)!.getDefaultConfig());
        }
      }
    }
    
    // Validate configuration
    const validation = plugin.validate(config);
    if (!validation.isValid) {
      throw new Error(`Invalid configuration for plugin ${pluginName}: ${validation.errors.join(', ')}`);
    }
    
    // Initialize plugin
    plugin.initialize(construct, config);
    this.loadedPlugins.add(pluginName);
  }
  
  getLoadedPlugins(): string[] {
    return Array.from(this.loadedPlugins);
  }
}

// Example plugin implementations
export class MonitoringPlugin implements CDKPlugin<MonitoringConfig> {
  readonly name = 'monitoring';
  readonly version = '1.0.0';
  
  initialize(construct: Construct, config: MonitoringConfig): void {
    // Create CloudWatch dashboards
    new cloudwatch.Dashboard(construct, 'MonitoringDashboard', {
      dashboardName: config.dashboardName,
      widgets: this.createWidgets(config)
    });
    
    // Create alarms
    config.alarms?.forEach((alarmConfig, index) => {
      new cloudwatch.Alarm(construct, `Alarm${index}`, {
        metric: new cloudwatch.Metric(alarmConfig.metric),
        threshold: alarmConfig.threshold,
        evaluationPeriods: alarmConfig.evaluationPeriods
      });
    });
  }
  
  validate(config: MonitoringConfig): ValidationResult {
    const errors: string[] = [];
    
    if (!config.dashboardName) {
      errors.push('dashboardName is required');
    }
    
    if (config.alarms) {
      config.alarms.forEach((alarm, index) => {
        if (!alarm.metric.metricName) {
          errors.push(`Alarm ${index} is missing metricName`);
        }
      });
    }
    
    return {
      isValid: errors.length === 0,
      errors
    };
  }
  
  getDefaultConfig(): MonitoringConfig {
    return {
      dashboardName: 'default-dashboard',
      alarms: []
    };
  }
  
  private createWidgets(config: MonitoringConfig): cloudwatch.IWidget[] {
    // Implementation for creating widgets
    return [];
  }
}

export class SecurityPlugin implements CDKPlugin<SecurityConfig> {
  readonly name = 'security';
  readonly version = '1.0.0';
  readonly dependencies = ['monitoring']; // Requires monitoring plugin
  
  initialize(construct: Construct, config: SecurityConfig): void {
    // Apply security policies
    Aspects.of(construct).add(new SecurityAspect(config));
    
    // Create security monitoring
    if (config.enableSecurityMonitoring) {
      this.setupSecurityMonitoring(construct, config);
    }
  }
  
  validate(config: SecurityConfig): ValidationResult {
    const errors: string[] = [];
    
    if (config.complianceStandards.length === 0) {
      errors.push('At least one compliance standard must be specified');
    }
    
    if (config.dataClassification === 'restricted' && !config.enableEncryption) {
      errors.push('Encryption must be enabled for restricted data classification');
    }
    
    return {
      isValid: errors.length === 0,
      errors
    };
  }
  
  getDefaultConfig(): SecurityConfig {
    return {
      complianceStandards: ['SOC2'],
      dataClassification: 'internal',
      enableEncryption: true,
      enableSecurityMonitoring: true
    };
  }
  
  private setupSecurityMonitoring(construct: Construct, config: SecurityConfig): void {
    // Implementation for security monitoring
  }
}

// Extensible construct using plugin architecture
export class ExtensiblePlatform extends Construct {
  private pluginManager = new PluginManager();
  
  constructor(scope: Construct, id: string, props: ExtensiblePlatformProps) {
    super(scope, id);
    
    // Register built-in plugins
    this.pluginManager.registerPlugin(new MonitoringPlugin());
    this.pluginManager.registerPlugin(new SecurityPlugin());
    
    // Register custom plugins
    props.customPlugins?.forEach(plugin => {
      this.pluginManager.registerPlugin(plugin);
    });
    
    // Load enabled plugins
    props.enabledPlugins.forEach(pluginConfig => {
      this.pluginManager.loadPlugin(this, pluginConfig.name, pluginConfig.config);
    });
    
    // Create core infrastructure
    this.createCoreInfrastructure(props);
  }
  
  private createCoreInfrastructure(props: ExtensiblePlatformProps): void {
    // Base infrastructure that plugins can extend
  }
}
```

#### 🛠️ Hands-On Lab 7.2: Advanced TypeScript Patterns

**Challenge**: Implement a type-safe, extensible infrastructure platform using advanced TypeScript patterns

**Your Mission**: Create a platform that demonstrates:
1. **Generic type constraints** for environment-specific configurations
2. **Conditional types** for feature flags and compliance requirements
3. **Plugin architecture** with dependency management
4. **Type-safe factories** for resource creation
5. **Advanced validation** with comprehensive error handling

**TypeScript Features to Master**:
- Mapped types and conditional types
- Template literal types for string manipulation
- Utility types for prop transformation
- Generic constraints and inference
- Advanced module patterns

**Success Criteria**:
- All TypeScript code compiles with strict mode enabled
- IntelliSense provides accurate autocompletion and error detection
- Type safety prevents runtime errors from configuration mistakes
- Plugin system supports third-party extensions
- Code is maintainable and self-documenting through types

**💰 Cost Warning**: Advanced TypeScript testing is mostly compile-time, so costs are minimal!

---

### Lesson 7.3: Cross-Account and Cross-Region Deployment Strategies
*"Because sometimes your infrastructure needs to travel more than a gap year backpacker"*

#### Multi-Account Architecture Patterns

Managing infrastructure across multiple AWS accounts is like herding cats, except the cats are in different countries and some of them don't speak the same language.

**Cross-Account CDK Pipeline Architecture**

```typescript
// Organization-wide account strategy
export interface OrganizationAccounts {
  readonly management: string;      // 111111111111 - Central management account
  readonly security: string;        // 222222222222 - Security tooling and monitoring
  readonly sharedServices: string;  // 333333333333 - Shared infrastructure
  readonly development: string;     // 444444444444 - Development workloads
  readonly staging: string;         // 555555555555 - Staging environment
  readonly production: string;      // 666666666666 - Production workloads
  readonly sandbox: string;         // 777777777777 - Experimentation
}

export class CrossAccountInfrastructure extends Construct {
  private readonly accounts: OrganizationAccounts;
  private readonly regions: string[];
  
  constructor(scope: Construct, id: string, props: CrossAccountProps) {
    super(scope, id);
    
    this.accounts = props.organizationAccounts;
    this.regions = props.deploymentRegions;
    
    // Deploy central management infrastructure
    this.deployCentralManagement();
    
    // Deploy shared services
    this.deploySharedServices();
    
    // Deploy environment-specific infrastructure
    this.deployEnvironmentInfrastructure();
    
    // Set up cross-account access and monitoring
    this.setupCrossAccountAccess();
  }
  
  private deployCentralManagement(): void {
    // Deploy to management account in primary region
    const managementStage = new ManagementAccountStage(this, 'Management', {
      env: {
        account: this.accounts.management,
        region: this.regions[0] // Primary region
      },
      organizationAccounts: this.accounts
    });
    
    // Cross-region replication for management infrastructure
    this.regions.slice(1).forEach((region, index) => {
      new ManagementAccountStage(this, `ManagementDR${index}`, {
        env: {
          account: this.accounts.management,
          region
        },
        organizationAccounts: this.accounts,
        isPrimaryRegion: false
      });
    });
  }
  
  private deploySharedServices(): void {
    // Deploy shared services to dedicated account
    const sharedServicesStage = new SharedServicesStage(this, 'SharedServices', {
      env: {
        account: this.accounts.sharedServices,
        region: this.regions[0]
      },
      organizationAccounts: this.accounts
    });
    
    // Cross-region shared services for DR
    this.regions.slice(1).forEach((region, index) => {
      new SharedServicesStage(this, `SharedServicesDR${index}`, {
        env: {
          account: this.accounts.sharedServices,
          region
        },
        organizationAccounts: this.accounts,
        isPrimaryRegion: false
      });
    });
  }
  
  private deployEnvironmentInfrastructure(): void {
    // Development environment
    new EnvironmentStage(this, 'Development', {
      env: {
        account: this.accounts.development,
        region: this.regions[0]
      },
      environment: 'dev',
      organizationAccounts: this.accounts
    });
    
    // Staging environment with multi-region
    this.regions.forEach((region, index) => {
      new EnvironmentStage(this, `Staging${index}`, {
        env: {
          account: this.accounts.staging,
          region
        },
        environment: 'staging',
        organizationAccounts: this.accounts,
        isPrimaryRegion: index === 0
      });
    });
    
    // Production environment with full multi-region
    this.regions.forEach((region, index) => {
      new EnvironmentStage(this, `Production${index}`, {
        env: {
          account: this.accounts.production,
          region
        },
        environment: 'prod',
        organizationAccounts: this.accounts,
        isPrimaryRegion: index === 0
      });
    });
  }
  
  private setupCrossAccountAccess(): void {
    // Create cross-account roles for CDK deployments
    this.createCrossAccountRoles();
    
    // Set up centralized monitoring
    this.setupCentralizedMonitoring();
    
    // Configure cross-account networking
    this.setupCrossAccountNetworking();
  }
  
  private createCrossAccountRoles(): void {
    // Create standardized cross-account roles
    const crossAccountRoleProps = {
      roleName: 'CDKDeploymentRole',
      trustedAccount: this.accounts.management,
      managedPolicies: [
        'arn:aws:iam::aws:policy/PowerUserAccess',
        'arn:aws:iam::aws:policy/IAMReadOnlyAccess'
      ],
      inlinePolicies: {
        CDKDeploymentPolicy: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              effect: iam.Effect.ALLOW,
              actions: [
                'iam:CreateRole',
                'iam:DeleteRole',
                'iam:AttachRolePolicy',
                'iam:DetachRolePolicy',
                'iam:PutRolePolicy',
                'iam:DeleteRolePolicy'
              ],
              resources: ['arn:aws:iam::*:role/cdk-*']
            })
          ]
        })
      }
    };
    
    // Deploy role to each target account
    Object.entries(this.accounts).forEach(([accountType, accountId]) => {
      if (accountType !== 'management') {
        new CrossAccountRole(this, `${accountType}DeploymentRole`, {
          ...crossAccountRoleProps,
          targetAccount: accountId
        });
      }
    });
  }
  
  private setupCentralizedMonitoring(): void {
    // Deploy centralized monitoring to security account
    new CentralizedMonitoringStack(this, 'CentralizedMonitoring', {
      env: {
        account: this.accounts.security,
        region: this.regions[0]
      },
      monitoredAccounts: Object.values(this.accounts),
      organizationId: 'o-xxxxxxxxxx' // Your organization ID
    });
  }
  
  private setupCrossAccountNetworking(): void {
    // Set up VPC peering and Transit Gateway across accounts
    new CrossAccountNetworkingStack(this, 'CrossAccountNetworking', {
      env: {
        account: this.accounts.sharedServices,
        region: this.regions[0]
      },
      organizationAccounts: this.accounts,
      networkingStrategy: 'transit-gateway' // or 'vpc-peering'
    });
  }
}

// Management account stage
export class ManagementAccountStage extends Stage {
  constructor(scope: Construct, id: string, props: ManagementAccountStageProps) {
    super(scope, id, props);
    
    // CDK Pipelines for cross-account deployment
    new CDKPipelineStack(this, 'CDKPipeline', {
      organizationAccounts: props.organizationAccounts,
      sourceRepo: 'your-org/infrastructure-repo',
      isPrimaryRegion: props.isPrimaryRegion ?? true
    });
    
    // Organization management
    new OrganizationManagementStack(this, 'OrganizationManagement', {
      organizationAccounts: props.organizationAccounts
    });
    
    // Billing and cost management
    new BillingManagementStack(this, 'BillingManagement', {
      organizationAccounts: props.organizationAccounts
    });
  }
}

// Shared services stage
export class SharedServicesStage extends Stage {
  constructor(scope: Construct, id: string, props: SharedServicesStageProps) {
    super(scope, id, props);
    
    // DNS management
    new DNSManagementStack(this, 'DNSManagement', {
      organizationAccounts: props.organizationAccounts,
      domainName: 'yourorg.com'
    });
    
    // Certificate management
    new CertificateManagementStack(this, 'CertificateManagement', {
      organizationAccounts: props.organizationAccounts
    });
    
    // Shared databases and services
    new SharedDatabaseStack(this, 'SharedDatabase', {
      organizationAccounts: props.organizationAccounts,
      isPrimaryRegion: props.isPrimaryRegion ?? true
    });
  }
}

// Cross-account role creation
export class CrossAccountRole extends Construct {
  constructor(scope: Construct, id: string, props: CrossAccountRoleProps) {
    super(scope, id);
    
    // Use custom resource to create role in target account
    const roleCreator = new lambda.Function(this, 'RoleCreator', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
        const { STSClient, AssumeRoleCommand } = require('@aws-sdk/client-sts');
        const { IAMClient, CreateRoleCommand, AttachRolePolicyCommand } = require('@aws-sdk/client-iam');
        
        exports.handler = async (event) => {
          const { targetAccount, roleName, trustedAccount, managedPolicies } = event.ResourceProperties;
          
          if (event.RequestType === 'Create') {
            // Assume role in target account
            const sts = new STSClient();
            const assumeRoleResult = await sts.send(new AssumeRoleCommand({
              RoleArn: \`arn:aws:iam::\${targetAccount}:role/OrganizationAccountAccessRole\`,
              RoleSessionName: 'CDKRoleCreation'
            }));
            
            // Create IAM client with assumed role credentials
            const iam = new IAMClient({
              credentials: {
                accessKeyId: assumeRoleResult.Credentials.AccessKeyId,
                secretAccessKey: assumeRoleResult.Credentials.SecretAccessKey,
                sessionToken: assumeRoleResult.Credentials.SessionToken
              }
            });
            
            // Create role
            await iam.send(new CreateRoleCommand({
              RoleName: roleName,
              AssumeRolePolicyDocument: JSON.stringify({
                Version: '2012-10-17',
                Statement: [{
                  Effect: 'Allow',
                  Principal: {
                    AWS: \`arn:aws:iam::\${trustedAccount}:root\`
                  },
                  Action: 'sts:AssumeRole'
                }]
              })
            }));
            
            // Attach managed policies
            for (const policyArn of managedPolicies) {
              await iam.send(new AttachRolePolicyCommand({
                RoleName: roleName,
                PolicyArn: policyArn
              }));
            }
          }
          
          return {
            PhysicalResourceId: \`\${targetAccount}-\${roleName}\`,
            Data: {
              RoleArn: \`arn:aws:iam::\${targetAccount}:role/\${roleName}\`
            }
          };
        };
      `),
      timeout: Duration.minutes(5)
    });
    
    // Grant permissions to assume organization roles
    roleCreator.addToRolePolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: ['sts:AssumeRole'],
      resources: [`arn:aws:iam::${props.targetAccount}:role/OrganizationAccountAccessRole`]
    }));
    
    // Custom resource
    new CustomResource(this, 'CrossAccountRoleResource', {
      serviceToken: roleCreator.functionArn,
      properties: {
        targetAccount: props.targetAccount,
        roleName: props.roleName,
        trustedAccount: props.trustedAccount,
        managedPolicies: props.managedPolicies
      }
    });
  }
}
```

**Multi-Region Deployment Patterns**

```typescript
// Global infrastructure with regional failover
export class GlobalInfrastructureStack extends Stack {
  public readonly primaryRegion: string;
  public readonly secondaryRegions: string[];
  public readonly globalTable: dynamodb.Table;
  public readonly route53Record: route53.ARecord;
  
  constructor(scope: Construct, id: string, props: GlobalInfrastructureProps) {
    super(scope, id, props);
    
    this.primaryRegion = props.primaryRegion;
    this.secondaryRegions = props.secondaryRegions;
    
    // Deploy primary region infrastructure
    const primaryInfra = this.deployRegionalInfrastructure(this.primaryRegion, true);
    
    // Deploy secondary region infrastructure
    const secondaryInfras = this.secondaryRegions.map((region, index) => 
      this.deployRegionalInfrastructure(region, false, `Secondary${index}`)
    );
    
    // Set up global DynamoDB table
    this.globalTable = this.createGlobalTable([this.primaryRegion, ...this.secondaryRegions]);
    
    // Configure Route 53 health checks and failover
    this.route53Record = this.setupGlobalDNS(primaryInfra, secondaryInfras);
    
    // Set up cross-region monitoring
    this.setupCrossRegionMonitoring();
  }
  
  private deployRegionalInfrastructure(
    region: string, 
    isPrimary: boolean, 
    suffix: string = ''
  ): RegionalInfrastructure {
    
    const regionalStack = new RegionalInfrastructureStack(this, `Regional${suffix || 'Primary'}`, {
      env: { region, account: this.account },
      isPrimaryRegion: isPrimary,
      applicationName: this.props.applicationName,
      globalConfiguration: this.props.globalConfiguration
    });
    
    return {
      stack: regionalStack,
      loadBalancer: regionalStack.loadBalancer,
      api: regionalStack.api,
      region
    };
  }
  
  private createGlobalTable(regions: string[]): dynamodb.Table {
    // Create global table that replicates across all regions
    return new dynamodb.Table(this, 'GlobalTable', {
      tableName: `${this.props.applicationName}-global-table`,
      partitionKey: { name: 'pk', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'sk', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      replicationRegions: regions.filter(r => r !== this.primaryRegion),
      stream: dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
      pointInTimeRecovery: true,
      encryption: dynamodb.TableEncryption.AWS_MANAGED
    });
  }
  
  private setupGlobalDNS(
    primary: RegionalInfrastructure, 
    secondaries: RegionalInfrastructure[]
  ): route53.ARecord {
    
    // Hosted zone for the application
    const hostedZone = route53.HostedZone.fromLookup(this, 'HostedZone', {
      domainName: this.props.domainName
    });
    
    // Health checks for each region
    const primaryHealthCheck = new route53.CfnHealthCheck(this, 'PrimaryHealthCheck', {
      type: 'HTTPS',
      resourcePath: '/health',
      fullyQualifiedDomainName: primary.loadBalancer.loadBalancerDnsName,
      port: 443,
      requestInterval: 30,
      failureThreshold: 3
    });
    
    const secondaryHealthChecks = secondaries.map((secondary, index) => 
      new route53.CfnHealthCheck(this, `SecondaryHealthCheck${index}`, {
        type: 'HTTPS',
        resourcePath: '/health',
        fullyQualifiedDomainName: secondary.loadBalancer.loadBalancerDnsName,
        port: 443,
        requestInterval: 30,
        failureThreshold: 3
      })
    );
    
    // Primary record with health check
    new route53.ARecord(this, 'PrimaryRecord', {
      zone: hostedZone,
      recordName: `api.${this.props.domainName}`,
      target: route53.RecordTarget.fromAlias(
        new route53targets.LoadBalancerTarget(primary.loadBalancer)
      ),
      setIdentifier: 'primary',
      healthCheckId: primaryHealthCheck.attrHealthCheckId,
      failover: route53.FailoverPolicy.PRIMARY
    });
    
    // Secondary records for failover
    secondaries.forEach((secondary, index) => {
      new route53.ARecord(this, `SecondaryRecord${index}`, {
        zone: hostedZone,
        recordName: `api.${this.props.domainName}`,
        target: route53.RecordTarget.fromAlias(
          new route53targets.LoadBalancerTarget(secondary.loadBalancer)
        ),
        setIdentifier: `secondary-${index}`,
        healthCheckId: secondaryHealthChecks[index].attrHealthCheckId,
        failover: route53.FailoverPolicy.SECONDARY
      });
    });
    
    // Return the primary record for reference
    return new route53.ARecord(this, 'GlobalRecord', {
      zone: hostedZone,
      recordName: `api.${this.props.domainName}`,
      target: route53.RecordTarget.fromAlias(
        new route53targets.LoadBalancerTarget(primary.loadBalancer)
      )
    });
  }
  
  private setupCrossRegionMonitoring(): void {
    // CloudWatch Synthetics for global monitoring
    const syntheticCanary = new synthetics.Canary(this, 'GlobalSynthetic', {
      canaryName: `${this.props.applicationName}-global-health`,
      schedule: synthetics.Schedule.rate(Duration.minutes(5)),
      test: synthetics.Test.custom({
        code: synthetics.Code.fromInline(`
          const synthetics = require('Synthetics');
          const log = require('SyntheticsLogger');
          
          const checkEndpoint = async function () {
            const regions = ['${this.primaryRegion}', '${this.secondaryRegions.join("', '")}'];
            
            for (const region of regions) {
              try {
                const response = await synthetics.executeHttpStep('check-' + region, {
                  hostname: 'api.${this.props.domainName}',
                  method: 'GET',
                  path: '/health',
                  headers: {
                    'User-Agent': 'CloudWatch-Synthetics',
                    'Region': region
                  }
                });
                
                if (response.statusCode !== 200) {
                  throw new Error(\`Health check failed for \${region}: \${response.statusCode}\`);
                }
                
                log.info(\`Health check passed for \${region}\`);
              } catch (error) {
                log.error(\`Health check failed for \${region}: \${error.message}\`);
                throw error;
              }
            }
          };
          
          exports.handler = async () => {
            return await synthetics.executeStep('checkEndpoint', checkEndpoint);
          };
        `),
        handler: 'index.handler'
      }),
      runtime: synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_9,
      environmentVariables: {
        PRIMARY_REGION: this.primaryRegion,
        SECONDARY_REGIONS: this.secondaryRegions.join(',')
      }
    });
    
    // Alarms for cross-region failures
    const globalFailureAlarm = new cloudwatch.Alarm(this, 'GlobalFailureAlarm', {
      metric: syntheticCanary.metricFailed(),
      threshold: 1,
      evaluationPeriods: 2,
      alarmDescription: 'Global endpoint health check is failing'
    });
    
    // SNS topic for global alerts
    const globalAlertTopic = new sns.Topic(this, 'GlobalAlerts');
    globalFailureAlarm.addAlarmAction(new cloudwatchActions.SnsAction(globalAlertTopic));
  }
}
```

#### 🛠️ Hands-On Lab 7.3: Multi-Account, Multi-Region Deployment

**Challenge**: Build a complete cross-account and cross-region infrastructure deployment

**Your Mission**: Create a realistic enterprise deployment that spans:
1. **Management Account**: Central CDK pipelines and organization management
2. **Security Account**: Centralized monitoring and compliance tools
3. **Shared Services Account**: DNS, certificates, and shared infrastructure
4. **Environment Accounts**: Separate accounts for dev/staging/prod
5. **Multi-Region**: Primary region (us-east-1) and DR region (us-west-2)

**Architecture Requirements**:
- Cross-account IAM roles for CDK deployment
- Centralized monitoring across all accounts
- Global DynamoDB table with cross-region replication
- Route 53 health checks with automatic failover
- Cross-account VPC peering or Transit Gateway
- Centralized logging and audit trail

**Enterprise Constraints**:
- All deployments must go through central pipeline
- Security account must have read-only access to all other accounts
- Cross-region failover must be automatic and transparent
- Compliance monitoring must be organization-wide
- Cost allocation tags must work across all accounts and regions

**Success Criteria**:
- Infrastructure deploys successfully across all accounts and regions
- Cross-account access works correctly with proper permissions
- Multi-region failover functions automatically during testing
- Centralized monitoring provides unified view across organization
- Cost allocation tags enable accurate billing per account/region
- Disaster recovery procedures work within defined RTO/RPO

**💰 Cost Warning**: Multi-account, multi-region deployment costs ~$10-25/day while running. Plan testing carefully and use automation for teardown!

---

## 📋 Module 7 Final Assessment

### Knowledge Check Quiz

**Question 1**: What's the most important consideration when building CDK construct libraries for enterprise use?
- a) Performance optimization
- b) Type safety and developer experience ✓
- c) Minimizing bundle size
- d) Supporting only TypeScript

**Question 2**: Which pattern is most effective for managing configuration across multiple environments and compliance standards?
- a) Environment variables
- b) Configuration files
- c) Type-safe configuration with conditional types ✓
- d) Hard-coded values

**Question 3**: What's the primary challenge in cross-account CDK deployments?
- a) Network connectivity
- b) IAM permissions and role assumption ✓
- c) Cost management
- d) Performance differences

### The Ultimate Enterprise CDK Challenge

**The Final Boss**: Build a complete enterprise-grade, multi-account, multi-region CDK platform that demonstrates mastery of all advanced patterns.

**System Requirements**:

Your platform must demonstrate:

1. **Advanced TypeScript Mastery**
   - Generic constructs with complex type constraints
   - Plugin architecture with dependency management
   - Type-safe configuration management
   - Advanced validation and error handling

2. **Enterprise Construct Library**
   - Published to multiple package managers
   - Comprehensive documentation and examples
   - Multi-language support (TypeScript, Python, Java)
   - Semantic versioning with automated releases

3. **Cross-Account Architecture**
   - Management account with central CDK pipelines
   - Security account with organization-wide monitoring
   - Shared services account with common infrastructure
   - Environment-specific accounts with proper isolation

4. **Multi-Region Deployment**
   - Primary region with full functionality
   - Secondary region with disaster recovery capabilities
   - Global services with automatic failover
   - Cross-region data replication and consistency

5. **Production-Grade Operations**
   - Comprehensive monitoring and alerting
   - Automated deployment pipelines with gates
   - Security scanning and compliance validation
   - Cost optimization and governance controls

**The Scenarios That Will Test Your Skills**:

1. **New Application Onboarding**: A new team wants to deploy their microservices using your platform
2. **Compliance Audit**: Auditors need to verify SOC2 and HIPAA compliance across all accounts
3. **Disaster Recovery Test**: Primary region goes offline and systems must failover automatically
4. **Security Incident**: Suspicious activity detected that requires immediate response across organization
5. **Cost Optimization**: CFO demands 30% cost reduction without impacting performance
6. **Regulatory Change**: New compliance requirement needs to be implemented across all environments

**Success Criteria**:

- ✅ **Platform Completeness**: All components work together seamlessly
- ✅ **Type Safety**: No runtime errors due to configuration issues
- ✅ **Documentation**: Comprehensive docs enable team self-service
- ✅ **Testing**: >95% code coverage with integration tests
- ✅ **Performance**: Platform handles enterprise-scale workloads
- ✅ **Security**: All security scans pass with no critical issues
- ✅ **Compliance**: Automated compliance validation across all standards
- ✅ **Operations**: Platform is maintainable and observable
- ✅ **Cost Efficiency**: Resource utilization is optimized
- ✅ **Disaster Recovery**: RTO < 30 minutes, RPO < 5 minutes

**Evaluation Process**:

1. **Architecture Review**: Technical design review with enterprise architects
2. **Code Quality Assessment**: TypeScript best practices and maintainability
3. **Security Audit**: Comprehensive security review and penetration testing
4. **Performance Testing**: Load testing under realistic enterprise conditions
5. **Disaster Recovery Drill**: Full failover testing with time measurements
6. **Compliance Validation**: Audit against all supported compliance standards
7. **Operational Readiness**: Documentation, runbooks, and knowledge transfer

**Timeline**: 3-4 weeks for complete implementation and validation

**💰 Investment**: $100-200 total for comprehensive testing across all accounts and regions

---

## 🎓 Congratulations - You Are Now a CDK TypeScript Master!

**What You've Accomplished**:

- ✅ **Mastered TypeScript** for enterprise infrastructure development
- ✅ **Built production-ready** CDK applications that won't embarrass you at 3 AM
- ✅ **Created reusable construct libraries** that your colleagues actually want to use
- ✅ **Implemented enterprise patterns** for compliance, security, and scalability
- ✅ **Deployed across accounts and regions** like a seasoned enterprise architect
- ✅ **Handled real-world complexity** with grace, humor, and proper error handling

**Your CDK TypeScript Journey**:
From CloudFormation YAML archaeology → Type-safe infrastructure poetry
From manual deployments → Automated, tested, reliable pipelines  
From "it works on my machine" → "it works everywhere, all the time"
From infrastructure nightmares → Infrastructure dreams

**What Makes You Special**:
You now understand that CDK TypeScript isn't just about deploying resources - it's about building maintainable, scalable, secure infrastructure that grows with your organization. You've learned to write infrastructure code that is not just functional, but elegant, testable, and actually enjoyable to work with.

**Your Superpower**:
You can now walk into any organization and build infrastructure platforms that developers love, operations teams trust, security teams approve, and finance teams don't complain about. That's a rare and valuable combination.

**The CDK TypeScript Mastery Achievement Unlocked**:
- 🏆 Enterprise-Grade Architecture Patterns
- 🎯 Type-Safe Infrastructure Development  
- 🚀 Production-Ready Deployment Pipelines
- 🛡️ Security-First Design Principles
- 💰 Cost-Optimized Resource Management
- 🔍 Comprehensive Monitoring & Observability
- 📚 Reusable Construct Library Creation
- 🌍 Multi-Account, Multi-Region Deployment
- 🎭 The Ability to Make Infrastructure Fun

**What's Next**:
Go forth and build amazing things. The AWS cloud is your oyster, TypeScript is your knife, and CDK is your shucking technique. Make infrastructure that doesn't just work, but works beautifully.

*Remember: You're not just a developer anymore - you're an infrastructure artist. Now paint us something beautiful! 🎨*

---

## 💡 Final Reflection Prompts

1. **How has your understanding of infrastructure-as-code evolved from CloudFormation templates to CDK TypeScript applications?**

2. **What enterprise patterns do you think will be most valuable in your organization?**

3. **How would you introduce CDK TypeScript to a team that's comfortable with CloudFormation?**

4. **What aspects of type safety in infrastructure code do you find most compelling?**

5. **How will you continue to grow your CDK TypeScript skills beyond this curriculum?**

---

*The journey from CloudFormation veteran to CDK TypeScript master is complete. You've learned not just to deploy infrastructure, but to craft it with precision, scale it with confidence, and maintain it with sanity intact. Go build the future! 🚀*