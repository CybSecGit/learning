# Module 6: CDK TypeScript for Container Orchestration
*"When Lambda isn't enough, but Kubernetes is too much like assembling IKEA furniture blindfolded"*

> **Duration**: 2-3 weeks  
> **Cost**: ~$2-4/day while running (because containers are more predictable than your relatives at Christmas dinner)  
> **Prerequisites**: Modules 1-5 completed, basic understanding that containers are not just fancy zip files, and the emotional resilience to deal with ECS service discovery

---

## 🎯 Module Learning Objectives

By the end of this module, you will:
- **Deploy containerized applications** with ECS that don't randomly stop working
- **Orchestrate multi-service architectures** without losing your sanity
- **Implement service discovery** that actually discovers services (revolutionary concept)
- **Design for scalability** because your application might actually become popular
- **Manage container security** like someone who reads the news
- **Handle persistent storage** for containers that need to remember things

---

## 📚 Core Lessons

### Lesson 6.1: ECS Fundamentals with CDK TypeScript
*"Container orchestration: Like conducting an orchestra, except half the musicians are drunk and the other half are playing different songs"*

#### Why ECS Instead of Just Running Everything on Lambda

Lambda is great, but sometimes you need to run applications that take longer than 15 minutes, use more than 10GB of memory, or just generally need to exist as more than a glorified function call. That's where containers come in - they're like Lambda's older, more responsible sibling who can hold down a proper job.

**The Container Hierarchy That Actually Makes Sense**

```typescript
// ❌ The "I have no idea what I'm doing" approach
export class ContainerChaosStack extends Stack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    
    // Throwing containers at ECS and hoping for the best
    const cluster = new ecs.Cluster(this, 'Cluster');
    
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'Task', {
      memoryLimitMiB: 512, // Probably not enough
      cpu: 256 // Definitely not enough
    });
    
    taskDefinition.addContainer('Container', {
      image: ecs.ContainerImage.fromRegistry('nginx'), // Random image from the internet
      portMappings: [{ containerPort: 80 }],
      environment: {
        SECRET_KEY: 'definitely-not-secret' // Security audit incoming
      }
    });
    
    new ecs.FargateService(this, 'Service', {
      cluster,
      taskDefinition,
      desiredCount: 1 // Because redundancy is for cowards
    });
    
    // No load balancer, no service discovery, no monitoring
    // What could possibly go wrong?
  }
}

// ✅ The "I know what I'm doing and my containers won't embarrass me" approach
export class ProductionContainerStack extends Stack {
  public readonly cluster: ecs.Cluster;
  public readonly service: ecs.FargateService;
  public readonly loadBalancer: elbv2.ApplicationLoadBalancer;
  
  constructor(scope: Construct, id: string, props: ContainerStackProps) {
    super(scope, id, props);
    
    // VPC because containers need somewhere to live
    const vpc = props.vpc || new ec2.Vpc(this, 'ContainerVpc', {
      maxAzs: 3, // Because availability zones are like backups - you need more than one
      natGateways: props.environment === 'prod' ? 3 : 1,
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
    
    // ECS Cluster with proper configuration
    this.cluster = new ecs.Cluster(this, 'ContainerCluster', {
      clusterName: `${props.applicationName}-${props.environment}`,
      vpc,
      containerInsights: true, // Because flying blind is for pilots, not engineers
      enableFargateCapacityProviders: true
    });
    
    // Application Load Balancer - the traffic cop that actually knows what it's doing
    this.loadBalancer = new elbv2.ApplicationLoadBalancer(this, 'LoadBalancer', {
      vpc,
      internetFacing: true,
      loadBalancerName: `${props.applicationName}-alb-${props.environment}`,
      securityGroup: this.createLoadBalancerSecurityGroup(vpc, props)
    });
    
    // Target group for health checks that won't lie to you
    const targetGroup = new elbv2.ApplicationTargetGroup(this, 'TargetGroup', {
      port: 80,
      protocol: elbv2.ApplicationProtocol.HTTP,
      vpc,
      targetType: elbv2.TargetType.IP,
      healthCheck: {
        enabled: true,
        healthyHttpCodes: '200',
        path: '/health',
        interval: Duration.seconds(30),
        timeout: Duration.seconds(5),
        healthyThresholdCount: 2,
        unhealthyThresholdCount: 5
      },
      deregistrationDelay: Duration.seconds(60) // Don't keep hitting dead containers
    });
    
    // Listener that actually listens
    const listener = this.loadBalancer.addListener('HttpListener', {
      port: 80,
      protocol: elbv2.ApplicationProtocol.HTTP,
      defaultTargetGroups: [targetGroup]
    });
    
    // HTTPS listener because security isn't optional
    if (props.certificateArn) {
      const httpsListener = this.loadBalancer.addListener('HttpsListener', {
        port: 443,
        protocol: elbv2.ApplicationProtocol.HTTPS,
        certificates: [
          elbv2.ListenerCertificate.fromArn(props.certificateArn)
        ],
        defaultTargetGroups: [targetGroup]
      });
      
      // Redirect HTTP to HTTPS because we're not animals
      listener.addAction('RedirectToHttps', {
        action: elbv2.ListenerAction.redirect({
          protocol: 'HTTPS',
          port: '443',
          permanent: true
        })
      });
    }
    
    // Task definition with proper resource allocation
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDefinition', {
      family: `${props.applicationName}-task-${props.environment}`,
      memoryLimitMiB: this.getTaskMemory(props.environment),
      cpu: this.getTaskCpu(props.environment),
      
      // Execution role for ECS agent
      executionRole: this.createExecutionRole(props),
      
      // Task role for application permissions
      taskRole: this.createTaskRole(props)
    });
    
    // Log group because logs are like breadcrumbs, but for debugging
    const logGroup = new logs.LogGroup(this, 'ContainerLogGroup', {
      logGroupName: `/ecs/${props.applicationName}-${props.environment}`,
      retention: logs.RetentionDays.ONE_MONTH,
      removalPolicy: RemovalPolicy.DESTROY
    });
    
    // Container definition with everything properly configured
    const container = taskDefinition.addContainer('ApplicationContainer', {
      containerName: props.applicationName,
      image: ecs.ContainerImage.fromAsset(props.dockerfilePath || './docker', {
        buildArgs: {
          ENVIRONMENT: props.environment
        }
      }),
      
      // Port mapping that makes sense
      portMappings: [{
        containerPort: 8080,
        protocol: ecs.Protocol.TCP,
        name: 'http'
      }],
      
      // Environment variables without secrets (we're not idiots)
      environment: {
        NODE_ENV: props.environment,
        PORT: '8080',
        LOG_LEVEL: props.environment === 'prod' ? 'info' : 'debug'
      },
      
      // Secrets from Parameter Store/Secrets Manager like adults
      secrets: {
        DATABASE_URL: ecs.Secret.fromSecretsManager(
          secretsmanager.Secret.fromSecretNameV2(this, 'DatabaseSecret', 
            `${props.applicationName}/${props.environment}/database-url`
          )
        ),
        API_KEY: ecs.Secret.fromSsmParameter(
          ssm.StringParameter.fromStringParameterName(this, 'ApiKeyParam',
            `/${props.applicationName}/${props.environment}/api-key`
          )
        )
      },
      
      // Logging configuration
      logging: ecs.LogDrivers.awsLogs({
        logGroup,
        streamPrefix: 'ecs'
      }),
      
      // Health check because containers lie about their health
      healthCheck: {
        command: ['CMD-SHELL', 'curl -f http://localhost:8080/health || exit 1'],
        interval: Duration.seconds(30),
        timeout: Duration.seconds(5),
        retries: 3,
        startPeriod: Duration.seconds(60) // Give the app time to start
      },
      
      // Resource limits because containers are greedy
      memoryReservationMiB: Math.floor(this.getTaskMemory(props.environment) * 0.8),
      
      // Essential because if this container dies, the whole task should die
      essential: true
    });
    
    // ECS Service with auto-scaling that actually works
    this.service = new ecs.FargateService(this, 'ContainerService', {
      serviceName: `${props.applicationName}-service-${props.environment}`,
      cluster: this.cluster,
      taskDefinition,
      
      // Desired count based on environment
      desiredCount: this.getDesiredCount(props.environment),
      
      // Placement in private subnets because security
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
      },
      
      // Security group that's actually secure
      securityGroups: [this.createServiceSecurityGroup(vpc, props)],
      
      // Platform version because latest isn't always greatest
      platformVersion: ecs.FargatePlatformVersion.LATEST,
      
      // Health check grace period
      healthCheckGracePeriod: Duration.seconds(120),
      
      // Enable service discovery
      cloudMapOptions: {
        cloudMapNamespace: this.cluster.addDefaultCloudMapNamespace({
          name: `${props.applicationName}-${props.environment}.local`,
          type: servicediscovery.NamespaceType.DNS_PRIVATE
        }),
        name: props.applicationName
      },
      
      // Circuit breaker to prevent bad deployments
      circuitBreaker: { rollback: true },
      
      // Enable logging
      enableLogging: true
    });
    
    // Attach service to load balancer
    this.service.attachToApplicationTargetGroup(targetGroup);
    
    // Auto-scaling because traffic is unpredictable
    const scalableTarget = this.service.autoScaleTaskCount({
      minCapacity: this.getMinCapacity(props.environment),
      maxCapacity: this.getMaxCapacity(props.environment)
    });
    
    // Scale on CPU utilization
    scalableTarget.scaleOnCpuUtilization('CpuScaling', {
      targetUtilizationPercent: 70, // Scale before things get spicy
      scaleInCooldown: Duration.seconds(300),
      scaleOutCooldown: Duration.seconds(60)
    });
    
    // Scale on memory utilization
    scalableTarget.scaleOnMemoryUtilization('MemoryScaling', {
      targetUtilizationPercent: 80,
      scaleInCooldown: Duration.seconds(300),
      scaleOutCooldown: Duration.seconds(60)
    });
    
    // Custom metric scaling for application-specific metrics
    scalableTarget.scaleOnMetric('RequestCountScaling', {
      metric: new cloudwatch.Metric({
        namespace: 'AWS/ApplicationELB',
        metricName: 'RequestCount',
        dimensionsMap: {
          LoadBalancer: this.loadBalancer.loadBalancerFullName
        },
        statistic: 'Sum'
      }),
      scalingSteps: [
        { upper: 1000, change: -1 },
        { lower: 2000, change: +1 },
        { lower: 5000, change: +2 }
      ],
      adjustmentType: autoscaling.AdjustmentType.CHANGE_IN_CAPACITY
    });
    
    // CloudWatch alarms because problems don't announce themselves
    this.addMonitoringAndAlerts(props);
    
    // Output important information
    new CfnOutput(this, 'LoadBalancerDNS', {
      value: this.loadBalancer.loadBalancerDnsName,
      description: 'Load Balancer DNS Name'
    });
    
    new CfnOutput(this, 'ServiceName', {
      value: this.service.serviceName,
      description: 'ECS Service Name'
    });
  }
  
  private getTaskMemory(environment: string): number {
    const memoryMap: Record<string, number> = {
      dev: 1024,      // 1GB for development
      staging: 2048,  // 2GB for staging
      prod: 4096      // 4GB for production
    };
    return memoryMap[environment] || memoryMap.dev;
  }
  
  private getTaskCpu(environment: string): number {
    const cpuMap: Record<string, number> = {
      dev: 512,       // 0.5 vCPU for development
      staging: 1024,  // 1 vCPU for staging
      prod: 2048      // 2 vCPU for production
    };
    return cpuMap[environment] || cpuMap.dev;
  }
  
  private getDesiredCount(environment: string): number {
    const countMap: Record<string, number> = {
      dev: 1,         // Single instance for development
      staging: 2,     // Two instances for staging
      prod: 3         // Three instances for production
    };
    return countMap[environment] || countMap.dev;
  }
  
  private getMinCapacity(environment: string): number {
    return Math.max(1, this.getDesiredCount(environment) - 1);
  }
  
  private getMaxCapacity(environment: string): number {
    const maxMap: Record<string, number> = {
      dev: 3,         // Max 3 for development
      staging: 5,     // Max 5 for staging  
      prod: 10        // Max 10 for production
    };
    return maxMap[environment] || maxMap.dev;
  }
  
  private createExecutionRole(props: ContainerStackProps): iam.Role {
    const role = new iam.Role(this, 'ExecutionRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      description: 'ECS Execution Role for pulling images and writing logs'
    });
    
    // Managed policy for ECS task execution
    role.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonECSTaskExecutionRolePolicy')
    );
    
    // Additional permissions for secrets access
    role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'secretsmanager:GetSecretValue',
        'ssm:GetParameters',
        'ssm:GetParameter'
      ],
      resources: [
        `arn:aws:secretsmanager:${this.region}:${this.account}:secret:${props.applicationName}/${props.environment}/*`,
        `arn:aws:ssm:${this.region}:${this.account}:parameter/${props.applicationName}/${props.environment}/*`
      ]
    }));
    
    return role;
  }
  
  private createTaskRole(props: ContainerStackProps): iam.Role {
    const role = new iam.Role(this, 'TaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      description: 'ECS Task Role for application permissions'
    });
    
    // Add application-specific permissions here
    // For example, S3 access, DynamoDB access, etc.
    
    return role;
  }
  
  private createLoadBalancerSecurityGroup(vpc: ec2.IVpc, props: ContainerStackProps): ec2.SecurityGroup {
    const sg = new ec2.SecurityGroup(this, 'LoadBalancerSecurityGroup', {
      vpc,
      description: 'Security group for Application Load Balancer',
      allowAllOutbound: false
    });
    
    // Allow HTTP traffic from internet
    sg.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(80),
      'Allow HTTP traffic from internet'
    );
    
    // Allow HTTPS traffic from internet
    if (props.certificateArn) {
      sg.addIngressRule(
        ec2.Peer.anyIpv4(),
        ec2.Port.tcp(443),
        'Allow HTTPS traffic from internet'
      );
    }
    
    return sg;
  }
  
  private createServiceSecurityGroup(vpc: ec2.IVpc, props: ContainerStackProps): ec2.SecurityGroup {
    const sg = new ec2.SecurityGroup(this, 'ServiceSecurityGroup', {
      vpc,
      description: 'Security group for ECS service',
      allowAllOutbound: true // Containers need internet access
    });
    
    // Allow traffic from load balancer only
    sg.addIngressRule(
      ec2.Peer.securityGroupId(this.loadBalancer.connections.securityGroups[0].securityGroupId),
      ec2.Port.tcp(8080),
      'Allow traffic from load balancer'
    );
    
    return sg;
  }
  
  private addMonitoringAndAlerts(props: ContainerStackProps): void {
    // CloudWatch dashboard
    const dashboard = new cloudwatch.Dashboard(this, 'ContainerDashboard', {
      dashboardName: `${props.applicationName}-containers-${props.environment}`
    });
    
    // Service metrics
    const serviceMetrics = {
      cpuUtilization: this.service.metricCpuUtilization(),
      memoryUtilization: this.service.metricMemoryUtilization(),
      runningTaskCount: new cloudwatch.Metric({
        namespace: 'AWS/ECS',
        metricName: 'RunningTaskCount',
        dimensionsMap: {
          ServiceName: this.service.serviceName,
          ClusterName: this.cluster.clusterName
        }
      })
    };
    
    // Load balancer metrics
    const albMetrics = {
      requestCount: this.loadBalancer.metricRequestCount(),
      targetResponseTime: this.loadBalancer.metricTargetResponseTime(),
      httpCodeELB5XX: this.loadBalancer.metricHttpCodeElb(elbv2.HttpCodeElb.ELB_5XX_COUNT),
      httpCodeTarget5XX: this.loadBalancer.metricHttpCodeTarget(elbv2.HttpCodeTarget.TARGET_5XX_COUNT)
    };
    
    // Add widgets to dashboard
    dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'ECS Service Metrics',
        left: [serviceMetrics.cpuUtilization, serviceMetrics.memoryUtilization],
        right: [serviceMetrics.runningTaskCount],
        width: 12
      }),
      new cloudwatch.GraphWidget({
        title: 'Load Balancer Metrics',
        left: [albMetrics.requestCount],
        right: [albMetrics.targetResponseTime],
        width: 12
      }),
      new cloudwatch.GraphWidget({
        title: 'Error Rates',
        left: [albMetrics.httpCodeELB5XX, albMetrics.httpCodeTarget5XX],
        width: 12
      })
    );
    
    // Alarms for high CPU utilization
    const highCpuAlarm = new cloudwatch.Alarm(this, 'HighCpuAlarm', {
      metric: serviceMetrics.cpuUtilization,
      threshold: 85,
      evaluationPeriods: 2,
      alarmDescription: 'ECS service CPU utilization is too high'
    });
    
    // Alarms for high memory utilization
    const highMemoryAlarm = new cloudwatch.Alarm(this, 'HighMemoryAlarm', {
      metric: serviceMetrics.memoryUtilization,
      threshold: 90,
      evaluationPeriods: 2,
      alarmDescription: 'ECS service memory utilization is too high'
    });
    
    // Alarms for 5XX errors
    const errorAlarm = new cloudwatch.Alarm(this, 'ErrorAlarm', {
      metric: albMetrics.httpCodeTarget5XX,
      threshold: 10,
      evaluationPeriods: 2,
      alarmDescription: 'Too many 5XX errors from application'
    });
    
    // SNS topic for alerts
    const alertTopic = new sns.Topic(this, 'ContainerAlerts');
    
    [highCpuAlarm, highMemoryAlarm, errorAlarm].forEach(alarm => {
      alarm.addAlarmAction(new cloudwatchActions.SnsAction(alertTopic));
    });
    
    // Email subscription for production alerts
    if (props.environment === 'prod' && props.alertEmail) {
      alertTopic.addSubscription(
        new snsSubscriptions.EmailSubscription(props.alertEmail)
      );
    }
  }
}
```

#### Multi-Service Architecture Patterns

**Service Mesh (Without the Kubernetes Complexity)**

```typescript
// Because sometimes services need to talk to each other without screaming across the data center
export class MicroservicesArchitecture extends Construct {
  public readonly cluster: ecs.Cluster;
  public readonly services: Map<string, ecs.FargateService> = new Map();
  public readonly loadBalancers: Map<string, elbv2.ApplicationLoadBalancer> = new Map();
  
  constructor(scope: Construct, id: string, props: MicroservicesProps) {
    super(scope, id);
    
    // Shared VPC for all services
    const vpc = new ec2.Vpc(this, 'MicroservicesVpc', {
      maxAzs: 3,
      natGateways: props.environment === 'prod' ? 3 : 1,
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
    
    // Shared ECS cluster
    this.cluster = new ecs.Cluster(this, 'MicroservicesCluster', {
      clusterName: `${props.applicationName}-cluster-${props.environment}`,
      vpc,
      containerInsights: true,
      enableFargateCapacityProviders: true
    });
    
    // Service discovery namespace
    const namespace = this.cluster.addDefaultCloudMapNamespace({
      name: `${props.applicationName}-${props.environment}.local`,
      type: servicediscovery.NamespaceType.DNS_PRIVATE
    });
    
    // Shared database for microservices (because sometimes you need to share)
    const database = new rds.DatabaseInstance(this, 'SharedDatabase', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13_7
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE3, 
        props.environment === 'prod' ? ec2.InstanceSize.LARGE : ec2.InstanceSize.MICRO
      ),
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
      },
      multiAz: props.environment === 'prod',
      deletionProtection: props.environment === 'prod',
      backupRetention: Duration.days(props.environment === 'prod' ? 30 : 7),
      storageEncrypted: true
    });
    
    // Deploy multiple services
    const serviceConfigs = [
      {
        name: 'user-service',
        port: 8080,
        healthPath: '/health',
        image: './services/user-service',
        environment: {
          SERVICE_NAME: 'user-service',
          DATABASE_TYPE: 'postgres'
        }
      },
      {
        name: 'order-service', 
        port: 8081,
        healthPath: '/health',
        image: './services/order-service',
        environment: {
          SERVICE_NAME: 'order-service',
          USER_SERVICE_URL: 'http://user-service.${props.applicationName}-${props.environment}.local:8080'
        }
      },
      {
        name: 'payment-service',
        port: 8082,
        healthPath: '/health', 
        image: './services/payment-service',
        environment: {
          SERVICE_NAME: 'payment-service',
          ORDER_SERVICE_URL: 'http://order-service.${props.applicationName}-${props.environment}.local:8081'
        }
      }
    ];
    
    serviceConfigs.forEach(config => {
      this.createMicroservice(config, vpc, database, namespace, props);
    });
    
    // API Gateway for external access
    this.createApiGateway(vpc, props);
    
    // Inter-service communication monitoring
    this.addServiceMeshMonitoring(props);
  }
  
  private createMicroservice(
    config: ServiceConfig,
    vpc: ec2.IVpc,
    database: rds.IDatabaseInstance,
    namespace: servicediscovery.INamespace,
    props: MicroservicesProps
  ): void {
    
    // Load balancer for this service
    const loadBalancer = new elbv2.ApplicationLoadBalancer(this, `${config.name}LoadBalancer`, {
      vpc,
      internetFacing: false, // Internal load balancer
      loadBalancerName: `${config.name}-alb-${props.environment}`
    });
    
    this.loadBalancers.set(config.name, loadBalancer);
    
    // Target group
    const targetGroup = new elbv2.ApplicationTargetGroup(this, `${config.name}TargetGroup`, {
      port: config.port,
      protocol: elbv2.ApplicationProtocol.HTTP,
      vpc,
      targetType: elbv2.TargetType.IP,
      healthCheck: {
        enabled: true,
        healthyHttpCodes: '200',
        path: config.healthPath,
        interval: Duration.seconds(30)
      }
    });
    
    // Listener
    loadBalancer.addListener(`${config.name}Listener`, {
      port: config.port,
      protocol: elbv2.ApplicationProtocol.HTTP,
      defaultTargetGroups: [targetGroup]
    });
    
    // Task definition
    const taskDefinition = new ecs.FargateTaskDefinition(this, `${config.name}TaskDefinition`, {
      family: `${config.name}-task-${props.environment}`,
      memoryLimitMiB: 1024,
      cpu: 512
    });
    
    // Container
    const container = taskDefinition.addContainer(`${config.name}Container`, {
      containerName: config.name,
      image: ecs.ContainerImage.fromAsset(config.image),
      portMappings: [{
        containerPort: config.port,
        protocol: ecs.Protocol.TCP
      }],
      environment: {
        ...config.environment,
        ENVIRONMENT: props.environment,
        PORT: config.port.toString()
      },
      secrets: {
        DATABASE_URL: ecs.Secret.fromSecretsManager(database.secret!)
      },
      logging: ecs.LogDrivers.awsLogs({
        logGroup: new logs.LogGroup(this, `${config.name}LogGroup`, {
          logGroupName: `/ecs/${config.name}-${props.environment}`,
          retention: logs.RetentionDays.ONE_MONTH
        }),
        streamPrefix: 'ecs'
      }),
      healthCheck: {
        command: ['CMD-SHELL', `curl -f http://localhost:${config.port}${config.healthPath} || exit 1`],
        interval: Duration.seconds(30),
        timeout: Duration.seconds(5),
        retries: 3
      }
    });
    
    // Security group for service
    const serviceSecurityGroup = new ec2.SecurityGroup(this, `${config.name}SecurityGroup`, {
      vpc,
      description: `Security group for ${config.name}`,
      allowAllOutbound: true
    });
    
    // Allow traffic from load balancer
    serviceSecurityGroup.addIngressRule(
      ec2.Peer.securityGroupId(loadBalancer.connections.securityGroups[0].securityGroupId),
      ec2.Port.tcp(config.port),
      `Allow traffic to ${config.name}`
    );
    
    // Allow inter-service communication
    serviceSecurityGroup.addIngressRule(
      ec2.Peer.ipv4(vpc.vpcCidrBlock),
      ec2.Port.tcp(config.port),
      'Allow inter-service communication'
    );
    
    // Allow database access
    database.connections.allowDefaultPortFrom(serviceSecurityGroup);
    
    // ECS Service
    const service = new ecs.FargateService(this, `${config.name}Service`, {
      serviceName: `${config.name}-service-${props.environment}`,
      cluster: this.cluster,
      taskDefinition,
      desiredCount: 2,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
      },
      securityGroups: [serviceSecurityGroup],
      cloudMapOptions: {
        cloudMapNamespace: namespace,
        name: config.name,
        dnsRecordType: servicediscovery.DnsRecordType.A
      },
      circuitBreaker: { rollback: true }
    });
    
    // Attach to load balancer
    service.attachToApplicationTargetGroup(targetGroup);
    
    // Auto-scaling
    const scalableTarget = service.autoScaleTaskCount({
      minCapacity: 1,
      maxCapacity: 5
    });
    
    scalableTarget.scaleOnCpuUtilization(`${config.name}CpuScaling`, {
      targetUtilizationPercent: 70
    });
    
    this.services.set(config.name, service);
  }
  
  private createApiGateway(vpc: ec2.IVpc, props: MicroservicesProps): void {
    // API Gateway for external access to microservices
    const api = new apigateway.RestApi(this, 'MicroservicesApi', {
      restApiName: `${props.applicationName}-api-${props.environment}`,
      description: 'API Gateway for microservices access',
      endpointConfiguration: {
        types: [apigateway.EndpointType.REGIONAL]
      }
    });
    
    // VPC Link for private integration
    const vpcLink = new apigateway.VpcLink(this, 'VpcLink', {
      targets: Array.from(this.loadBalancers.values())
    });
    
    // Create API routes for each service
    this.services.forEach((service, serviceName) => {
      const resource = api.root.addResource(serviceName);
      const proxy = resource.addProxy({
        anyMethod: true,
        defaultIntegration: new apigateway.HttpIntegration(`http://${serviceName}.${props.applicationName}-${props.environment}.local`, {
          vpcLink,
          httpMethod: 'ANY',
          options: {
            requestParameters: {
              'integration.request.path.proxy': 'method.request.path.proxy'
            }
          }
        })
      });
    });
    
    // Output the API Gateway URL
    new CfnOutput(this, 'ApiGatewayUrl', {
      value: api.url,
      description: 'API Gateway URL for microservices'
    });
  }
  
  private addServiceMeshMonitoring(props: MicroservicesProps): void {
    // X-Ray tracing for distributed tracing
    const xrayConfig = new xray.CfnSamplingRule(this, 'XraySamplingRule', {
      samplingRule: {
        ruleName: `${props.applicationName}-${props.environment}-sampling`,
        priority: 9000,
        fixedRate: 0.1, // 10% sampling rate
        reservoirSize: 1,
        serviceName: '*',
        serviceType: '*',
        host: '*',
        httpMethod: '*',
        urlPath: '*',
        version: 1
      }
    });
    
    // Service map dashboard
    const dashboard = new cloudwatch.Dashboard(this, 'ServiceMeshDashboard', {
      dashboardName: `${props.applicationName}-service-mesh-${props.environment}`
    });
    
    // Create widgets for each service
    const widgets: cloudwatch.IWidget[] = [];
    
    this.services.forEach((service, serviceName) => {
      widgets.push(
        new cloudwatch.GraphWidget({
          title: `${serviceName} Metrics`,
          left: [service.metricCpuUtilization()],
          right: [service.metricMemoryUtilization()],
          width: 6,
          height: 6
        })
      );
    });
    
    dashboard.addWidgets(...widgets);
  }
}
```

#### 🛠️ Hands-On Lab 6.1: Deploy a Multi-Service Container Application

**Challenge**: Build a complete microservices architecture using ECS and CDK TypeScript

**Your Mission**: Create a realistic e-commerce microservices platform with:
1. **User Service** - Authentication and user management
2. **Product Service** - Product catalog and inventory  
3. **Order Service** - Order processing and management
4. **Payment Service** - Payment processing integration
5. **Notification Service** - Email and SMS notifications

**Architecture Requirements**:
- Each service runs in its own container with proper health checks
- Services communicate via service discovery (no hardcoded IPs)
- External API Gateway for public access
- Internal load balancers for service-to-service communication
- Shared database with proper connection pooling
- Comprehensive monitoring and logging

**Real-World Constraints**:
- Handle 1000+ concurrent users across all services
- Services must be independently deployable
- Graceful degradation when dependencies fail
- Zero-downtime deployments with blue/green strategy
- Cost-optimized with proper auto-scaling

**Success Criteria**:
- All services deploy and communicate successfully
- External API works through all service layers
- Auto-scaling triggers under load testing
- Health checks and service discovery function correctly
- Monitoring dashboards show all key metrics
- Services handle failure scenarios gracefully

**💰 Cost Warning**: Multi-service architecture costs ~$3-5/day while running. Test efficiently and tear down when done!

---

### Lesson 6.2: Container Security and Best Practices
*"Because container security is like home security - you think you're safe until someone walks through your unlocked front door"*

#### Container Security That Actually Secures Things

Container security is one of those things that everyone talks about but most people implement about as well as airport security - lots of theater, questionable effectiveness. Let's do better.

**Base Image Security (Starting with Something That Won't Embarrass You)**

```typescript
// ❌ Security nightmare fuel
export class InsecureContainerStack extends Stack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'Task', {
      memoryLimitMiB: 512,
      cpu: 256
    });
    
    // Using random base image from unknown registry
    taskDefinition.addContainer('Container', {
      image: ecs.ContainerImage.fromRegistry('random-user/sketchy-app:latest'),
      
      // Running as root because why not?
      user: 'root',
      
      // Privileged container because security is optional
      privileged: true,
      
      // Mount the Docker socket because what could go wrong?
      dockerLabels: {
        'security': 'what-security'
      },
      
      // Environment variables with secrets in plain text
      environment: {
        DATABASE_PASSWORD: 'super-secret-password-123',
        API_KEY: 'definitely-not-a-secret'
      }
    });
  }
}

// ✅ Security that actually works
export class SecureContainerStack extends Stack {
  constructor(scope: Construct, id: string, props: SecureContainerProps) {
    super(scope, id, props);
    
    // Use minimal, security-focused base images
    const baseImage = this.createSecureBaseImage(props);
    
    // Task definition with security constraints
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'SecureTask', {
      family: `${props.applicationName}-secure-task`,
      memoryLimitMiB: 1024,
      cpu: 512,
      
      // Execution role with minimal permissions
      executionRole: this.createMinimalExecutionRole(props),
      
      // Task role with least privilege
      taskRole: this.createRestrictedTaskRole(props)
    });
    
    // Container with security best practices
    const container = taskDefinition.addContainer('SecureContainer', {
      containerName: props.applicationName,
      image: baseImage,
      
      // Run as non-root user
      user: '1001:1001', // Non-root user and group
      
      // No privileged access
      privileged: false,
      
      // Read-only root filesystem
      readonlyRootFilesystem: true,
      
      // Security labels for compliance
      dockerLabels: {
        'security.scan.date': new Date().toISOString().split('T')[0],
        'security.compliance': 'SOC2-compliant',
        'app.version': props.appVersion || 'unknown'
      },
      
      // Environment variables without secrets
      environment: {
        NODE_ENV: props.environment,
        PORT: '8080',
        LOG_LEVEL: 'info',
        APP_NAME: props.applicationName
      },
      
      // Secrets from AWS Secrets Manager
      secrets: {
        DATABASE_URL: ecs.Secret.fromSecretsManager(
          this.createDatabaseSecret(props)
        ),
        API_KEY: ecs.Secret.fromSsmParameter(
          this.createApiKeyParameter(props)
        ),
        JWT_SECRET: ecs.Secret.fromSecretsManager(
          this.createJwtSecret(props)
        )
      },
      
      // Resource limits to prevent container breakout
      memoryLimitMiB: 900, // Leave some buffer
      memoryReservationMiB: 512,
      
      // Logging with security considerations
      logging: ecs.LogDrivers.awsLogs({
        logGroup: this.createSecureLogGroup(props),
        streamPrefix: 'secure-container'
      }),
      
      // Health check that doesn't expose internals
      healthCheck: {
        command: ['CMD-SHELL', 'curl -f http://localhost:8080/health || exit 1'],
        interval: Duration.seconds(30),
        timeout: Duration.seconds(5),
        retries: 3,
        startPeriod: Duration.seconds(60)
      },
      
      // Port mapping with specific protocols
      portMappings: [{
        containerPort: 8080,
        protocol: ecs.Protocol.TCP,
        name: 'http'
      }],
      
      // Essential container
      essential: true,
      
      // Linux parameters for additional security
      linuxParameters: new ecs.LinuxParameters(this, 'LinuxParams', {
        initProcessEnabled: true, // Handle zombie processes
        sharedMemorySize: 64 // Limit shared memory
      })
    });
    
    // Volume for writable directories (since root FS is read-only)
    taskDefinition.addVolume({
      name: 'tmp-volume'
    });
    
    container.addMountPoints({
      sourceVolume: 'tmp-volume',
      containerPath: '/tmp',
      readOnly: false
    });
    
    // Network security group with minimal access
    const securityGroup = new ec2.SecurityGroup(this, 'ContainerSecurityGroup', {
      vpc: props.vpc,
      description: 'Security group for secure container',
      allowAllOutbound: false // Explicit outbound rules only
    });
    
    // Only allow HTTPS outbound for external APIs
    securityGroup.addEgressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(443),
      'HTTPS outbound for external APIs'
    );
    
    // Allow DNS queries
    securityGroup.addEgressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.udp(53),
      'DNS queries'
    );
    
    // Allow database connections to specific security group
    if (props.databaseSecurityGroup) {
      securityGroup.addEgressRule(
        props.databaseSecurityGroup,
        ec2.Port.tcp(5432),
        'Database connection'
      );
    }
    
    // ECS Service with security configurations
    const service = new ecs.FargateService(this, 'SecureService', {
      serviceName: `${props.applicationName}-secure-service`,
      cluster: props.cluster,
      taskDefinition,
      desiredCount: 2,
      
      // Run in private subnets only
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
      },
      
      // Use the secure security group
      securityGroups: [securityGroup],
      
      // Platform version with latest security patches
      platformVersion: ecs.FargatePlatformVersion.LATEST,
      
      // Enable service connect for secure inter-service communication
      enableServiceConnect: true,
      
      // Circuit breaker to prevent bad deployments
      circuitBreaker: { rollback: true },
      
      // Enable logging
      enableLogging: true
    });
    
    // Add security monitoring
    this.addSecurityMonitoring(service, props);
  }
  
  private createSecureBaseImage(props: SecureContainerProps): ecs.ContainerImage {
    // Use AWS ECR Public Gallery base images or build from scratch
    return ecs.ContainerImage.fromAsset('./docker', {
      buildArgs: {
        // Use specific base image versions, not 'latest'
        BASE_IMAGE: 'public.ecr.aws/amazonlinux/amazonlinux:2023',
        APP_VERSION: props.appVersion || 'unknown'
      },
      platform: assets.Platform.LINUX_AMD64, // Specific platform
      
      // Build arguments for security scanning
      buildSecrets: {
        // No secrets in build args - use build-time secrets properly
      }
    });
  }
  
  private createMinimalExecutionRole(props: SecureContainerProps): iam.Role {
    const role = new iam.Role(this, 'SecureExecutionRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      description: 'Minimal execution role for secure container'
    });
    
    // Only the permissions absolutely necessary
    role.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonECSTaskExecutionRolePolicy')
    );
    
    // Specific permissions for secrets access
    role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'secretsmanager:GetSecretValue'
      ],
      resources: [
        `arn:aws:secretsmanager:${this.region}:${this.account}:secret:${props.applicationName}/*`
      ],
      conditions: {
        StringEquals: {
          'secretsmanager:VersionStage': 'AWSCURRENT'
        }
      }
    }));
    
    // Specific permissions for SSM parameters
    role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'ssm:GetParameter'
      ],
      resources: [
        `arn:aws:ssm:${this.region}:${this.account}:parameter/${props.applicationName}/*`
      ]
    }));
    
    return role;
  }
  
  private createRestrictedTaskRole(props: SecureContainerProps): iam.Role {
    const role = new iam.Role(this, 'SecureTaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      description: 'Restricted task role for application permissions'
    });
    
    // Add only the permissions your application actually needs
    // Example: S3 bucket access
    if (props.s3BucketArn) {
      role.addToPolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          's3:GetObject',
          's3:PutObject'
        ],
        resources: [
          `${props.s3BucketArn}/*`
        ],
        conditions: {
          StringEquals: {
            's3:x-amz-server-side-encryption': 'AES256'
          }
        }
      }));
    }
    
    // Example: DynamoDB table access
    if (props.dynamoTableArn) {
      role.addToPolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'dynamodb:GetItem',
          'dynamodb:PutItem',
          'dynamodb:UpdateItem',
          'dynamodb:DeleteItem',
          'dynamodb:Query'
        ],
        resources: [props.dynamoTableArn],
        conditions: {
          'ForAllValues:StringEquals': {
            'dynamodb:Attributes': ['id', 'data', 'timestamp'] // Specific attributes only
          }
        }
      }));
    }
    
    return role;
  }
  
  private createDatabaseSecret(props: SecureContainerProps): secretsmanager.Secret {
    return new secretsmanager.Secret(this, 'DatabaseSecret', {
      secretName: `${props.applicationName}/database-credentials`,
      description: 'Database credentials for secure container',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({
          username: 'app_user',
          host: props.databaseHost || 'localhost',
          port: 5432,
          dbname: props.databaseName || 'app_db'
        }),
        generateStringKey: 'password',
        excludeCharacters: '"@/\\',
        includeSpace: false,
        passwordLength: 32
      }
    });
  }
  
  private createApiKeyParameter(props: SecureContainerProps): ssm.StringParameter {
    return new ssm.StringParameter(this, 'ApiKeyParameter', {
      parameterName: `/${props.applicationName}/api-key`,
      stringValue: 'placeholder-api-key', // Set this through AWS Console or CLI
      description: 'API key for external service integration',
      type: ssm.ParameterType.SECURE_STRING
    });
  }
  
  private createJwtSecret(props: SecureContainerProps): secretsmanager.Secret {
    return new secretsmanager.Secret(this, 'JwtSecret', {
      secretName: `${props.applicationName}/jwt-secret`,
      description: 'JWT signing secret',
      generateSecretString: {
        generateStringKey: 'secret',
        secretStringTemplate: '{}',
        excludeCharacters: '"@/\\',
        includeSpace: false,
        passwordLength: 64
      }
    });
  }
  
  private createSecureLogGroup(props: SecureContainerProps): logs.LogGroup {
    return new logs.LogGroup(this, 'SecureLogGroup', {
      logGroupName: `/ecs/secure/${props.applicationName}`,
      retention: logs.RetentionDays.ONE_MONTH,
      
      // Encrypt logs at rest
      encryptionKey: new kms.Key(this, 'LogsEncryptionKey', {
        description: 'KMS key for encrypting container logs',
        enableKeyRotation: true
      }),
      
      // Remove logs when stack is deleted (for non-prod)
      removalPolicy: props.environment === 'prod' 
        ? RemovalPolicy.RETAIN 
        : RemovalPolicy.DESTROY
    });
  }
  
  private addSecurityMonitoring(service: ecs.FargateService, props: SecureContainerProps): void {
    // CloudWatch Insights for security monitoring
    const securityMetricFilter = new logs.MetricFilter(this, 'SecurityMetricFilter', {
      logGroup: this.createSecureLogGroup(props),
      metricNamespace: 'Security/Containers',
      metricName: 'SecurityEvents',
      filterPattern: logs.FilterPattern.anyTerm(
        'ERROR', 'SECURITY', 'UNAUTHORIZED', 'FAILED_LOGIN', 'SUSPICIOUS'
      ),
      metricValue: '1'
    });
    
    // Alarm for security events
    const securityAlarm = new cloudwatch.Alarm(this, 'SecurityEventsAlarm', {
      metric: securityMetricFilter.metric(),
      threshold: 10, // More than 10 security events in evaluation period
      evaluationPeriods: 1,
      alarmDescription: 'High number of security events detected in container logs'
    });
    
    // SNS topic for security alerts
    const securityTopic = new sns.Topic(this, 'SecurityAlerts', {
      topicName: `${props.applicationName}-security-alerts`
    });
    
    securityAlarm.addAlarmAction(new cloudwatchActions.SnsAction(securityTopic));
    
    // Lambda function for automated security response
    const securityResponseFunction = new lambda.Function(this, 'SecurityResponse', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
        const { ECSClient, UpdateServiceCommand } = require('@aws-sdk/client-ecs');
        const ecs = new ECSClient();
        
        exports.handler = async (event) => {
          console.log('Security event received:', JSON.stringify(event, null, 2));
          
          // Parse SNS message
          const message = JSON.parse(event.Records[0].Sns.Message);
          
          if (message.AlarmName.includes('SecurityEvents')) {
            console.log('Security alarm triggered - investigating...');
            
            // In a real implementation, you might:
            // 1. Analyze logs for specific threats
            // 2. Temporarily restrict access
            // 3. Scale down the service if needed
            // 4. Notify security team
            
            // For now, just log the event
            console.log('Security monitoring active - manual review recommended');
          }
          
          return { statusCode: 200 };
        };
      `),
      timeout: Duration.minutes(5)
    });
    
    // Subscribe Lambda to security topic
    securityTopic.addSubscription(
      new snsSubscriptions.LambdaSubscription(securityResponseFunction)
    );
    
    // Grant Lambda permission to update ECS service if needed
    service.grantDesiredCount(securityResponseFunction);
  }
}
```

#### Container Image Scanning and Compliance

```typescript
// Because trusting random Docker images is like eating gas station sushi
export class ContainerSecurityScanning extends Construct {
  constructor(scope: Construct, id: string, props: SecurityScanningProps) {
    super(scope, id);
    
    // ECR repository with image scanning enabled
    const repository = new ecr.Repository(this, 'SecureRepository', {
      repositoryName: `${props.applicationName}-secure`,
      imageScanOnPush: true, // Scan every image automatically
      imageTagMutability: ecr.TagMutability.IMMUTABLE, // Prevent tag overwriting
      encryptionConfiguration: {
        encryptionType: ecr.EncryptionType.KMS,
        kmsKey: new kms.Key(this, 'ECREncryptionKey', {
          description: 'KMS key for ECR encryption',
          enableKeyRotation: true
        })
      },
      lifecycleRules: [{
        rulePriority: 1,
        description: 'Delete untagged images after 1 day',
        selection: {
          tagStatus: ecr.TagStatus.UNTAGGED,
          countType: ecr.CountType.SINCE_IMAGE_PUSHED,
          countUnit: Duration.days(1)
        },
        action: ecr.LifecycleAction.EXPIRE
      }, {
        rulePriority: 2,
        description: 'Keep only 10 most recent images',
        selection: {
          tagStatus: ecr.TagStatus.ANY,
          countType: ecr.CountType.IMAGE_COUNT_MORE_THAN,
          countNumber: 10
        },
        action: ecr.LifecycleAction.EXPIRE
      }]
    });
    
    // CodeBuild project for security scanning and compliance checks
    const securityScanProject = new codebuild.Project(this, 'SecurityScanProject', {
      projectName: `${props.applicationName}-security-scan`,
      description: 'Security scanning and compliance checks for container images',
      source: codebuild.Source.gitHub({
        owner: props.githubOwner,
        repo: props.githubRepo,
        webhook: true,
        webhookFilters: [
          codebuild.FilterGroup.inEventOf(codebuild.EventAction.PUSH).andBranchIs('main'),
          codebuild.FilterGroup.inEventOf(codebuild.EventAction.PULL_REQUEST_CREATED),
          codebuild.FilterGroup.inEventOf(codebuild.EventAction.PULL_REQUEST_UPDATED)
        ]
      }),
      environment: {
        buildImage: codebuild.LinuxBuildImage.STANDARD_5_0,
        computeType: codebuild.ComputeType.MEDIUM,
        privileged: true // Needed for Docker builds
      },
      buildSpec: codebuild.BuildSpec.fromObject({
        version: '0.2',
        phases: {
          pre_build: {
            commands: [
              'echo "Logging in to Amazon ECR..."',
              'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com',
              
              'echo "Installing security scanning tools..."',
              'curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin',
              'curl -sfL https://raw.githubusercontent.com/hadolint/hadolint/master/bin/install.sh | sh -s -- -b /usr/local/bin',
              
              'echo "Setting up variables..."',
              'REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME',
              'IMAGE_TAG=${CODEBUILD_RESOLVED_SOURCE_VERSION:-latest}'
            ]
          },
          build: {
            commands: [
              'echo "Build started on `date`"',
              
              'echo "Linting Dockerfile..."',
              'hadolint Dockerfile || echo "Dockerfile linting found issues - review required"',
              
              'echo "Building the Docker image..."',
              'docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .',
              'docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $REPOSITORY_URI:$IMAGE_TAG',
              
              'echo "Running security scan with Trivy..."',
              'trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_REPO_NAME:$IMAGE_TAG || echo "High/Critical vulnerabilities found"',
              
              'echo "Running comprehensive vulnerability scan..."',
              'trivy image --format json --output trivy-report.json $IMAGE_REPO_NAME:$IMAGE_TAG',
              
              'echo "Checking for secrets in image..."',
              'trivy fs --scanners secret --format json --output secrets-report.json .',
              
              'echo "Pushing the Docker image..."',
              'docker push $REPOSITORY_URI:$IMAGE_TAG'
            ]
          },
          post_build: {
            commands: [
              'echo "Build completed on `date`"',
              'echo "Generating security report..."',
              'aws s3 cp trivy-report.json s3://$SECURITY_REPORTS_BUCKET/trivy-reports/$CODEBUILD_BUILD_ID-trivy.json',
              'aws s3 cp secrets-report.json s3://$SECURITY_REPORTS_BUCKET/secret-scans/$CODEBUILD_BUILD_ID-secrets.json',
              
              'echo "Checking ECR scan results..."',
              'aws ecr describe-image-scan-findings --repository-name $IMAGE_REPO_NAME --image-id imageTag=$IMAGE_TAG || echo "ECR scan not yet complete"'
            ]
          }
        },
        artifacts: {
          files: [
            'trivy-report.json',
            'secrets-report.json'
          ]
        }
      }),
      environmentVariables: {
        AWS_DEFAULT_REGION: { value: this.region },
        AWS_ACCOUNT_ID: { value: this.account },
        IMAGE_REPO_NAME: { value: repository.repositoryName },
        SECURITY_REPORTS_BUCKET: { value: this.createSecurityReportsBucket().bucketName }
      },
      cache: codebuild.Cache.local(codebuild.LocalCacheMode.DOCKER_LAYER)
    });
    
    // Grant permissions to CodeBuild
    repository.grantPullPush(securityScanProject);
    
    // Lambda function to process scan results
    const scanResultsProcessor = new lambda.Function(this, 'ScanResultsProcessor', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
        const { ECRClient, DescribeImageScanFindingsCommand } = require('@aws-sdk/client-ecr');
        const { SNSClient, PublishCommand } = require('@aws-sdk/client-sns');
        
        const ecr = new ECRClient();
        const sns = new SNSClient();
        
        exports.handler = async (event) => {
          console.log('Processing ECR scan results:', JSON.stringify(event, null, 2));
          
          try {
            const detail = event.detail;
            const repositoryName = detail['repository-name'];
            const imageTag = detail['image-tag'];
            const scanStatus = detail['scan-status'];
            
            if (scanStatus === 'COMPLETE') {
              // Get scan findings
              const scanFindings = await ecr.send(new DescribeImageScanFindingsCommand({
                repositoryName: repositoryName,
                imageId: { imageTag: imageTag }
              }));
              
              const findings = scanFindings.imageScanFindings;
              const criticalFindings = findings.findingCounts?.CRITICAL || 0;
              const highFindings = findings.findingCounts?.HIGH || 0;
              
              console.log('Scan results:', {
                critical: criticalFindings,
                high: highFindings,
                total: findings.findings?.length || 0
              });
              
              // Alert if critical vulnerabilities found
              if (criticalFindings > 0) {
                await sns.send(new PublishCommand({
                  TopicArn: process.env.SECURITY_TOPIC_ARN,
                  Subject: 'Critical Vulnerabilities Found in Container Image',
                  Message: JSON.stringify({
                    repository: repositoryName,
                    imageTag: imageTag,
                    criticalVulnerabilities: criticalFindings,
                    highVulnerabilities: highFindings,
                    scanArn: scanFindings.imageScanFindings?.imageScanCompletedAt
                  }, null, 2)
                }));
              }
            }
            
            return { statusCode: 200 };
          } catch (error) {
            console.error('Error processing scan results:', error);
            throw error;
          }
        };
      `),
      environment: {
        SECURITY_TOPIC_ARN: this.createSecurityTopic().topicArn
      },
      timeout: Duration.minutes(5)
    });
    
    // EventBridge rule for ECR scan completion
    new events.Rule(this, 'ECRScanCompleteRule', {
      eventPattern: {
        source: ['aws.ecr'],
        detailType: ['ECR Image Scan'],
        detail: {
          'scan-status': ['COMPLETE'],
          'repository-name': [repository.repositoryName]
        }
      },
      targets: [
        new eventsTargets.LambdaFunction(scanResultsProcessor)
      ]
    });
    
    // Grant permissions
    repository.grantRead(scanResultsProcessor);
    this.createSecurityTopic().grantPublish(scanResultsProcessor);
  }
  
  private createSecurityReportsBucket(): s3.Bucket {
    return new s3.Bucket(this, 'SecurityReportsBucket', {
      bucketName: `security-reports-${this.account}-${this.region}`.toLowerCase(),
      encryption: s3.BucketEncryption.KMS_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      lifecycleRules: [{
        id: 'DeleteOldReports',
        enabled: true,
        expiration: Duration.days(90) // Keep reports for 90 days
      }],
      removalPolicy: RemovalPolicy.DESTROY
    });
  }
  
  private createSecurityTopic(): sns.Topic {
    return new sns.Topic(this, 'SecurityAlertsTopic', {
      topicName: 'container-security-alerts',
      displayName: 'Container Security Alerts'
    });
  }
}
```

#### 🛠️ Hands-On Lab 6.2: Implement Container Security Pipeline

**Challenge**: Build a complete container security pipeline that catches vulnerabilities before they reach production

**Your Mission**: Create a security-first container deployment pipeline with:
1. **Dockerfile linting** with Hadolint to catch misconfigurations
2. **Vulnerability scanning** with Trivy for OS and application dependencies
3. **Secret detection** to prevent credentials from being baked into images
4. **Runtime security monitoring** with AWS GuardDuty and custom metrics
5. **Compliance validation** against CIS Docker benchmarks

**Security Requirements**:
- Block deployment of images with critical vulnerabilities
- Scan base images and application dependencies
- Detect secrets and sensitive data in images
- Monitor runtime behavior for suspicious activity
- Generate compliance reports for audit purposes

**Real-World Scenarios**:
- Developer accidentally includes API key in Dockerfile
- Base image has critical vulnerability published after deployment
- Container attempts unusual network connections at runtime
- Application tries to escalate privileges or access host resources

**Success Criteria**:
- Pipeline blocks images with critical security issues
- All container images are scanned before deployment
- Runtime monitoring detects and alerts on suspicious behavior
- Compliance reports generate automatically
- Security alerts are actionable and not overwhelming

**💰 Cost Warning**: Security scanning adds ~$1-2/day in additional compute and storage costs. Worth every penny!

---

### Lesson 6.3: Persistent Storage and Data Management
*"Because containers that forget everything are like goldfish with commitment issues"*

#### Storage That Actually Persists

Containers are ephemeral by nature, which is great until you need to store something important. It's like having a conversation with someone who has amnesia - charming at first, then increasingly frustrating.

**EFS Integration for Shared Storage**

```typescript
// When multiple containers need to share files like a dysfunctional family sharing a Netflix account
export class ContainerPersistentStorage extends Construct {
  public readonly fileSystem: efs.FileSystem;
  public readonly accessPoint: efs.AccessPoint;
  
  constructor(scope: Construct, id: string, props: PersistentStorageProps) {
    super(scope, id);
    
    // EFS file system for shared storage
    this.fileSystem = new efs.FileSystem(this, 'SharedFileSystem', {
      vpc: props.vpc,
      fileSystemName: `${props.applicationName}-shared-storage-${props.environment}`,
      
      // Performance mode based on environment
      performanceMode: props.environment === 'prod' 
        ? efs.PerformanceMode.MAX_IO 
        : efs.PerformanceMode.GENERAL_PURPOSE,
      
      // Throughput mode for consistent performance
      throughputMode: props.environment === 'prod'
        ? efs.ThroughputMode.PROVISIONED
        : efs.ThroughputMode.BURSTING,
      
      // Provisioned throughput for production
      ...(props.environment === 'prod' && {
        provisionedThroughputPerSecond: Size.mebibytes(100)
      }),
      
      // Encryption at rest because we're not animals
      encrypted: true,
      kmsKey: new kms.Key(this, 'EFSEncryptionKey', {
        description: 'KMS key for EFS encryption',
        enableKeyRotation: true
      }),
      
      // Lifecycle policy to save money
      lifecyclePolicy: efs.LifecyclePolicy.AFTER_30_DAYS,
      
      // Transition to IA after 30 days
      transitionToArchivePolicy: efs.LifecyclePolicy.AFTER_90_DAYS,
      
      // Security settings
      enableBackups: true,
      removalPolicy: props.environment === 'prod' 
        ? RemovalPolicy.RETAIN 
        : RemovalPolicy.DESTROY
    });
    
    // Security group for EFS
    const efsSecurityGroup = new ec2.SecurityGroup(this, 'EFSSecurityGroup', {
      vpc: props.vpc,
      description: 'Security group for EFS access',
      allowAllOutbound: false
    });
    
    // Allow NFS traffic from container security groups
    efsSecurityGroup.addIngressRule(
      props.containerSecurityGroup,
      ec2.Port.tcp(2049),
      'NFS access from containers'
    );
    
    this.fileSystem.connections.addSecurityGroup(efsSecurityGroup);
    
    // Access point for fine-grained access control
    this.accessPoint = this.fileSystem.addAccessPoint('ContainerAccessPoint', {
      path: '/shared',
      creationInfo: {
        ownerUid: 1001, // Non-root owner
        ownerGid: 1001,
        permissions: '755'
      },
      posixUser: {
        uid: 1001,
        gid: 1001
      }
    });
    
    // Mount targets in all private subnets
    props.vpc.privateSubnets.forEach((subnet, index) => {
      this.fileSystem.addMountTarget(`MountTarget${index}`, {
        subnet,
        securityGroup: efsSecurityGroup
      });
    });
    
    // CloudWatch monitoring for EFS
    this.addEFSMonitoring(props);
  }
  
  private addEFSMonitoring(props: PersistentStorageProps): void {
    // CloudWatch dashboard for EFS metrics
    const dashboard = new cloudwatch.Dashboard(this, 'EFSDashboard', {
      dashboardName: `${props.applicationName}-efs-${props.environment}`
    });
    
    // EFS metrics
    const efsMetrics = {
      totalIOBytes: new cloudwatch.Metric({
        namespace: 'AWS/EFS',
        metricName: 'TotalIOBytes',
        dimensionsMap: {
          FileSystemId: this.fileSystem.fileSystemId
        },
        statistic: 'Sum'
      }),
      clientConnections: new cloudwatch.Metric({
        namespace: 'AWS/EFS',
        metricName: 'ClientConnections',
        dimensionsMap: {
          FileSystemId: this.fileSystem.fileSystemId
        },
        statistic: 'Sum'
      }),
      burstCreditBalance: new cloudwatch.Metric({
        namespace: 'AWS/EFS',
        metricName: 'BurstCreditBalance',
        dimensionsMap: {
          FileSystemId: this.fileSystem.fileSystemId
        },
        statistic: 'Average'
      })
    };
    
    dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'EFS I/O Operations',
        left: [efsMetrics.totalIOBytes],
        width: 12
      }),
      new cloudwatch.GraphWidget({
        title: 'EFS Connections',
        left: [efsMetrics.clientConnections],
        right: [efsMetrics.burstCreditBalance],
        width: 12
      })
    );
    
    // Alarms for EFS issues
    const lowBurstCreditsAlarm = new cloudwatch.Alarm(this, 'LowBurstCreditsAlarm', {
      metric: efsMetrics.burstCreditBalance,
      threshold: 1000000000, // 1 billion bytes
      comparisonOperator: cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
      evaluationPeriods: 2,
      alarmDescription: 'EFS burst credit balance is low'
    });
    
    // SNS topic for EFS alerts
    const efsAlertTopic = new sns.Topic(this, 'EFSAlerts');
    lowBurstCreditsAlarm.addAlarmAction(new cloudwatchActions.SnsAction(efsAlertTopic));
  }
}

// Task definition with EFS volume mounting
export class ContainerWithPersistentStorage extends Construct {
  public readonly service: ecs.FargateService;
  
  constructor(scope: Construct, id: string, props: ContainerStorageProps) {
    super(scope, id);
    
    // Task definition with EFS volume
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskWithStorage', {
      family: `${props.applicationName}-storage-task`,
      memoryLimitMiB: 2048,
      cpu: 1024
    });
    
    // Add EFS volume to task definition
    taskDefinition.addVolume({
      name: 'shared-storage',
      efsVolumeConfiguration: {
        fileSystemId: props.persistentStorage.fileSystem.fileSystemId,
        transitEncryption: 'ENABLED', // Encrypt data in transit
        authorizationConfig: {
          accessPointId: props.persistentStorage.accessPoint.accessPointId
        }
      }
    });
    
    // Container with mounted EFS volume
    const container = taskDefinition.addContainer('ApplicationContainer', {
      containerName: props.applicationName,
      image: ecs.ContainerImage.fromAsset('./docker'),
      
      // Environment variables for storage paths
      environment: {
        SHARED_STORAGE_PATH: '/mnt/shared',
        LOCAL_STORAGE_PATH: '/tmp/local',
        NODE_ENV: props.environment
      },
      
      // Mount EFS volume
      mountPoints: [{
        sourceVolume: 'shared-storage',
        containerPath: '/mnt/shared',
        readOnly: false
      }],
      
      // Health check that verifies storage access
      healthCheck: {
        command: [
          'CMD-SHELL',
          'test -d /mnt/shared && echo "Storage accessible" || exit 1'
        ],
        interval: Duration.seconds(30),
        timeout: Duration.seconds(5),
        retries: 3
      },
      
      logging: ecs.LogDrivers.awsLogs({
        logGroup: new logs.LogGroup(this, 'ContainerLogGroup', {
          logGroupName: `/ecs/${props.applicationName}-storage`,
          retention: logs.RetentionDays.ONE_MONTH
        }),
        streamPrefix: 'ecs-storage'
      })
    });
    
    // ECS service
    this.service = new ecs.FargateService(this, 'ServiceWithStorage', {
      serviceName: `${props.applicationName}-storage-service`,
      cluster: props.cluster,
      taskDefinition,
      desiredCount: 2,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
      },
      securityGroups: [props.containerSecurityGroup],
      platformVersion: ecs.FargatePlatformVersion.VERSION1_4 // Required for EFS
    });
  }
}
```

**Database Integration Patterns**

```typescript
// Because sometimes containers need to talk to databases, and that conversation needs to be meaningful
export class ContainerDatabaseIntegration extends Construct {
  public readonly database: rds.DatabaseInstance;
  public readonly connectionPool: elasticache.CfnCacheCluster;
  
  constructor(scope: Construct, id: string, props: DatabaseIntegrationProps) {
    super(scope, id);
    
    // RDS instance with proper configuration
    this.database = new rds.DatabaseInstance(this, 'ApplicationDatabase', {
      databaseName: props.databaseName,
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13_7
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE3,
        props.environment === 'prod' ? ec2.InstanceSize.LARGE : ec2.InstanceSize.MICRO
      ),
      vpc: props.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
      },
      
      // Security configuration
      storageEncrypted: true,
      deletionProtection: props.environment === 'prod',
      backupRetention: Duration.days(props.environment === 'prod' ? 30 : 7),
      
      // Performance configuration
      multiAz: props.environment === 'prod',
      enablePerformanceInsights: true,
      performanceInsightRetention: rds.PerformanceInsightRetention.DEFAULT,
      
      // Monitoring
      monitoringInterval: Duration.seconds(60),
      monitoringRole: this.createRDSMonitoringRole(),
      
      // Connection configuration
      port: 5432,
      parameterGroup: this.createDatabaseParameterGroup(),
      
      // Credentials stored in Secrets Manager
      credentials: rds.Credentials.fromGeneratedSecret('dbadmin', {
        secretName: `${props.applicationName}/${props.environment}/db-credentials`,
        excludeCharacters: '"@/\\'
      }),
      
      removalPolicy: props.environment === 'prod' 
        ? RemovalPolicy.RETAIN 
        : RemovalPolicy.DESTROY
    });
    
    // ElastiCache for Redis (connection pooling and caching)
    const redisSubnetGroup = new elasticache.CfnSubnetGroup(this, 'RedisSubnetGroup', {
      description: 'Subnet group for Redis cluster',
      subnetIds: props.vpc.privateSubnets.map(subnet => subnet.subnetId)
    });
    
    this.connectionPool = new elasticache.CfnCacheCluster(this, 'RedisConnectionPool', {
      cacheNodeType: props.environment === 'prod' ? 'cache.r6g.large' : 'cache.t3.micro',
      engine: 'redis',
      numCacheNodes: 1,
      vpcSecurityGroupIds: [this.createRedisSecurityGroup(props.vpc).securityGroupId],
      cacheSubnetGroupName: redisSubnetGroup.ref,
      
      // Security settings
      transitEncryptionEnabled: true,
      atRestEncryptionEnabled: true,
      
      // Backup settings
      snapshotRetentionLimit: props.environment === 'prod' ? 7 : 1,
      snapshotWindow: '03:00-05:00',
      
      // Maintenance settings
      preferredMaintenanceWindow: 'sun:05:00-sun:07:00'
    });
    
    // Database migration and seed data Lambda
    this.createDatabaseMigrationLambda(props);
    
    // Database monitoring and alerting
    this.addDatabaseMonitoring(props);
  }
  
  private createDatabaseParameterGroup(): rds.ParameterGroup {
    return new rds.ParameterGroup(this, 'DatabaseParameterGroup', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13_7
      }),
      description: 'Custom parameter group for application database',
      parameters: {
        // Connection settings optimized for containers
        'max_connections': '200',
        'shared_buffers': '256MB',
        'effective_cache_size': '1GB',
        'work_mem': '4MB',
        'maintenance_work_mem': '64MB',
        
        // Logging settings for debugging
        'log_statement': 'all',
        'log_min_duration_statement': '1000', // Log queries taking longer than 1 second
        'log_checkpoints': 'on',
        'log_connections': 'on',
        'log_disconnections': 'on',
        
        // Performance settings
        'checkpoint_completion_target': '0.9',
        'wal_buffers': '16MB',
        'default_statistics_target': '100'
      }
    });
  }
  
  private createRDSMonitoringRole(): iam.Role {
    const role = new iam.Role(this, 'RDSMonitoringRole', {
      assumedBy: new iam.ServicePrincipal('monitoring.rds.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonRDSEnhancedMonitoringRole')
      ]
    });
    
    return role;
  }
  
  private createRedisSecurityGroup(vpc: ec2.IVpc): ec2.SecurityGroup {
    const sg = new ec2.SecurityGroup(this, 'RedisSecurityGroup', {
      vpc,
      description: 'Security group for Redis cluster',
      allowAllOutbound: false
    });
    
    // Allow Redis connections from containers
    sg.addIngressRule(
      ec2.Peer.ipv4(vpc.vpcCidrBlock),
      ec2.Port.tcp(6379),
      'Redis access from containers'
    );
    
    return sg;
  }
  
  private createDatabaseMigrationLambda(props: DatabaseIntegrationProps): lambda.Function {
    return new lambda.Function(this, 'DatabaseMigration', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
        const { Client } = require('pg');
        const AWS = require('aws-sdk');
        const secretsManager = new AWS.SecretsManager();
        
        exports.handler = async (event) => {
          console.log('Database migration event:', JSON.stringify(event, null, 2));
          
          try {
            // Get database credentials from Secrets Manager
            const secret = await secretsManager.getSecretValue({
              SecretId: process.env.DB_SECRET_ARN
            }).promise();
            
            const credentials = JSON.parse(secret.SecretString);
            
            // Connect to database
            const client = new Client({
              host: credentials.host,
              port: credentials.port,
              database: credentials.dbname,
              user: credentials.username,
              password: credentials.password,
              ssl: { rejectUnauthorized: false }
            });
            
            await client.connect();
            
            // Run migrations based on event type
            if (event.RequestType === 'Create') {
              await runInitialMigrations(client);
            } else if (event.RequestType === 'Update') {
              await runUpdateMigrations(client);
            }
            
            await client.end();
            
            return {
              PhysicalResourceId: 'database-migration-' + Date.now(),
              Data: {
                Status: 'Success',
                Timestamp: new Date().toISOString()
              }
            };
          } catch (error) {
            console.error('Migration failed:', error);
            throw error;
          }
        };
        
        async function runInitialMigrations(client) {
          console.log('Running initial database migrations...');
          
          // Create initial tables
          await client.query(\`
            CREATE TABLE IF NOT EXISTS users (
              id SERIAL PRIMARY KEY,
              email VARCHAR(255) UNIQUE NOT NULL,
              password_hash VARCHAR(255) NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
          \`);
          
          await client.query(\`
            CREATE TABLE IF NOT EXISTS sessions (
              id VARCHAR(255) PRIMARY KEY,
              user_id INTEGER REFERENCES users(id),
              data JSONB,
              expires_at TIMESTAMP NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
          \`);
          
          // Create indexes
          await client.query(\`
            CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
            CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);
          \`);
          
          console.log('Initial migrations completed');
        }
        
        async function runUpdateMigrations(client) {
          console.log('Running update migrations...');
          
          // Check current schema version and run appropriate migrations
          const result = await client.query(\`
            SELECT version FROM schema_migrations ORDER BY version DESC LIMIT 1;
          \`);
          
          const currentVersion = result.rows[0]?.version || 0;
          console.log('Current schema version:', currentVersion);
          
          // Run migrations newer than current version
          // In a real app, you'd have a proper migration system
        }
      `),
      environment: {
        DB_SECRET_ARN: this.database.secret!.secretArn
      },
      vpc: props.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
      },
      timeout: Duration.minutes(5)
    });
  }
  
  private addDatabaseMonitoring(props: DatabaseIntegrationProps): void {
    // CloudWatch dashboard for database metrics
    const dbDashboard = new cloudwatch.Dashboard(this, 'DatabaseDashboard', {
      dashboardName: `${props.applicationName}-database-${props.environment}`
    });
    
    // Database metrics
    const dbMetrics = {
      cpuUtilization: this.database.metricCPUUtilization(),
      databaseConnections: this.database.metricDatabaseConnections(),
      readLatency: this.database.metricReadLatency(),
      writeLatency: this.database.metricWriteLatency(),
      freeStorageSpace: this.database.metricFreeStorageSpace()
    };
    
    dbDashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'Database Performance',
        left: [dbMetrics.cpuUtilization],
        right: [dbMetrics.databaseConnections],
        width: 12
      }),
      new cloudwatch.GraphWidget({
        title: 'Database Latency',
        left: [dbMetrics.readLatency, dbMetrics.writeLatency],
        width: 12
      }),
      new cloudwatch.SingleValueWidget({
        title: 'Free Storage Space',
        metrics: [dbMetrics.freeStorageSpace],
        width: 6
      })
    );
    
    // Alarms for database issues
    const highCpuAlarm = new cloudwatch.Alarm(this, 'DatabaseHighCPU', {
      metric: dbMetrics.cpuUtilization,
      threshold: 80,
      evaluationPeriods: 2,
      alarmDescription: 'Database CPU utilization is high'
    });
    
    const lowStorageAlarm = new cloudwatch.Alarm(this, 'DatabaseLowStorage', {
      metric: dbMetrics.freeStorageSpace,
      threshold: 2000000000, // 2GB in bytes
      comparisonOperator: cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
      evaluationPeriods: 1,
      alarmDescription: 'Database free storage space is low'
    });
    
    // SNS topic for database alerts
    const dbAlertTopic = new sns.Topic(this, 'DatabaseAlerts');
    
    [highCpuAlarm, lowStorageAlarm].forEach(alarm => {
      alarm.addAlarmAction(new cloudwatchActions.SnsAction(dbAlertTopic));
    });
  }
}
```

#### 🛠️ Hands-On Lab 6.3: Build a Data-Persistent Container Application

**Challenge**: Create a containerized application that properly handles persistent data and database connections

**Your Mission**: Build a file processing service that:
1. **Accepts file uploads** via API and stores them in EFS
2. **Processes files asynchronously** using container workers
3. **Stores metadata** in PostgreSQL with proper connection pooling
4. **Caches results** in Redis for fast retrieval
5. **Handles file sharing** between multiple container instances

**Data Requirements**:
- Files must persist across container restarts
- Database connections must be properly pooled
- File processing must be resumable after failures
- Shared storage must be accessible by all containers
- Data must be encrypted at rest and in transit

**Real-World Challenges**:
- Multiple containers processing the same file simultaneously
- Database connection limits under high load
- EFS performance bottlenecks with large files
- Container crashes during file processing
- Storage costs growing out of control

**Success Criteria**:
- Files persist correctly across container deployments
- Database connections are properly managed and pooled
- Multiple containers can share files without conflicts
- System handles failures gracefully with proper recovery
- Storage costs are optimized with lifecycle policies
- Performance meets requirements under load

**💰 Cost Warning**: EFS and RDS costs ~$2-4/day depending on usage. Monitor storage growth and implement lifecycle policies!

---

## 📋 Module 6 Assessment

### Knowledge Check Quiz

**Question 1**: What's the main advantage of ECS over running containers directly on EC2?
- a) It's cheaper
- b) It provides orchestration, scaling, and health management ✓
- c) It's faster
- d) It supports more container runtimes

**Question 2**: Which is the most important security practice for container images?
- a) Using the latest tag for base images
- b) Running containers as root for full permissions
- c) Scanning images for vulnerabilities before deployment ✓
- d) Disabling all security features for performance

**Question 3**: When should you use EFS with containers?
- a) Never, containers should be stateless
- b) When multiple containers need to share persistent files ✓
- c) Only for temporary storage
- d) When you want to save money on storage

### Final Container Orchestration Challenge: Distributed Processing Platform

**The Ultimate Test**: Build a complete distributed data processing platform using containers

**System Architecture**:
Your platform must include:
1. **Web Interface**: React app served from S3/CloudFront
2. **API Gateway**: For external access and rate limiting
3. **Processing Queue**: SQS for job distribution
4. **Worker Containers**: ECS services that process jobs
5. **Shared Storage**: EFS for input/output files
6. **Database Layer**: PostgreSQL for job metadata and results
7. **Caching Layer**: Redis for performance optimization
8. **Monitoring**: Comprehensive observability and alerting

**Processing Requirements**:
- Handle 1000+ concurrent processing jobs
- Support multiple job types (image processing, data analysis, file conversion)
- Implement job prioritization and retry logic
- Provide real-time job status updates
- Support batch processing for large datasets

**Container Requirements**:
- All services run in containers with proper security
- Auto-scaling based on queue depth and CPU utilization
- Blue/green deployments with zero downtime
- Health checks and circuit breakers for resilience
- Proper resource limits and security constraints

**Data Requirements**:
- All data encrypted at rest and in transit
- Shared file storage accessible by all workers
- Database connection pooling for high concurrency
- Backup and disaster recovery procedures
- Compliance with data retention policies

**Security Requirements**:
- Container images scanned for vulnerabilities
- Secrets managed through AWS Secrets Manager
- Network segmentation with security groups
- Runtime security monitoring and alerting
- Compliance with container security benchmarks

**The Stress Tests**:
1. **Black Friday Load**: 10,000 jobs submitted in 5 minutes
2. **Worker Node Failure**: Random container failures during processing
3. **Database Failover**: Primary database becomes unavailable
4. **Storage Exhaustion**: EFS reaches capacity limits
5. **Network Partitioning**: Inter-service communication disrupted
6. **Security Incident**: Malicious container behavior detected

**Success Criteria**:
- ✅ System processes all job types without data loss
- ✅ Auto-scaling responds appropriately to load changes
- ✅ Failure scenarios are handled gracefully with recovery
- ✅ Security scans pass with no critical vulnerabilities
- ✅ Monitoring provides actionable insights and alerts
- ✅ Performance meets requirements under all test conditions
- ✅ Cost optimization keeps operational expenses reasonable
- ✅ Documentation supports operational maintenance

**💰 Cost Warning**: Full distributed platform costs ~$20-40/day at scale. Build incrementally and tear down between major testing phases!

**Timeline**: 2-3 weeks for complete implementation and testing

---

## 🚀 Ready for Module 7?

**Before proceeding, ensure you can:**
- ✅ Deploy and orchestrate multi-container applications with ECS
- ✅ Implement container security best practices throughout the lifecycle
- ✅ Handle persistent storage and database integration correctly
- ✅ Design for scalability and resilience in container environments
- ✅ Monitor and troubleshoot containerized applications effectively
- ✅ Optimize costs while maintaining performance and reliability

**Next Up**: [Module 7: CDK TypeScript Mastery & Enterprise Patterns](/learning-plans/cdk-typescript/module-7)

---

## 💡 Reflection Prompts

1. **How does container orchestration change your approach to application architecture compared to traditional server deployments?**

2. **What are the trade-offs between container security and operational convenience?**

3. **When would you choose ECS over Lambda, and vice versa?**

4. **How do you balance stateless container design with real-world data persistence needs?**

5. **What container monitoring strategies have proven most valuable for troubleshooting production issues?**

---

*Congratulations! You've mastered the art of making containers do useful work without falling over. Your applications now scale like a well-oiled machine and handle data like a responsible adult. Time for the final boss level - enterprise patterns that won't make your colleagues question your life choices! 🏆*