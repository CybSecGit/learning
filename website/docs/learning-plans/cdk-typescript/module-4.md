# Module 4: CDK TypeScript Data Flow & Event-Driven Patterns
*"Mastering complex CDK orchestration, or: How I Learned to Stop Worrying and Love Asynchronous Chaos"*

> **Duration**: 1-2 weeks  
> **Cost**: ~$8-15/day while running (2-3 hour deployment windows max - seriously, don't be that person who leaves OpenSearch running overnight and then cries about the bill)  
> **Prerequisites**: Modules 1-3 completed, basic understanding that events are not just things that happen at Christmas parties

---

## 🎯 Module Learning Objectives

By the end of this module, you will:
- **Master event-driven architecture** in CDK TypeScript (because polling is for people who hate themselves)
- **Orchestrate complex data flows** between AWS services like a conductor who actually knows what they're doing
- **Build resilient async patterns** that don't collapse at the first sign of trouble
- **Create custom CDK resources** when AWS doesn't give you exactly what you want (which is often)
- **Design loosely-coupled systems** that won't make your colleagues plot your demise

---

## 📚 Core Lessons

### Lesson 4.1: Event-Driven Architecture in CDK
*"Welcome to the world where everything happens eventually, and order is more of a suggestion"*

#### Why Event-Driven Architecture Exists

Look, someone clever realized that making services sit around waiting for other services to finish their business is about as efficient as a British queue for tea during a heatwave. So instead, we throw events around like confetti at a wedding nobody wanted to attend.

**The Traditional Approach (Synchronous Hell)**:
```typescript
// ❌ This is how people who hate themselves build systems
export class SynchronousDisasterStack extends Stack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    
    // API Gateway calls Lambda, which calls RDS, which calls another Lambda,
    // which probably calls an external API that's down half the time
    const api = new apigateway.RestApi(this, 'API');
    const lambda1 = new lambda.Function(this, 'Step1', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'step1.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async (event) => {
          // Synchronously call the next service and pray it works
          const result = await callNextServiceAndHopeForTheBest(event);
          return { statusCode: result.success ? 200 : 500 };
        };
      `),
      timeout: Duration.seconds(30) // Optimistic, aren't we?
    });
    
    // When this fails (and it will), good luck debugging the chain
    api.root.addMethod('POST', new apigateway.LambdaIntegration(lambda1));
  }
}
```

**The Event-Driven Approach (Asynchronous Bliss)**:
```typescript
// ✅ This is how adults build systems
export class EventDrivenStack extends Stack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    
    // Event bus - the town square where all the gossip happens
    const eventBus = new events.EventBus(this, 'EventBus', {
      eventBusName: 'application-events'
    });
    
    // SQS queues - because sometimes services need to take their time
    const processingQueue = new sqs.Queue(this, 'ProcessingQueue', {
      deadLetterQueue: {
        queue: new sqs.Queue(this, 'DeadLetterQueue'),
        maxReceiveCount: 3 // After 3 tries, we give up and blame someone else
      },
      visibilityTimeout: Duration.seconds(300) // 5 minutes should be enough for anyone
    });
    
    // SNS topic - for when you need to tell everyone about something
    const notificationTopic = new sns.Topic(this, 'NotificationTopic');
    
    // Lambda functions that actually do useful work
    const eventProcessor = new lambda.Function(this, 'EventProcessor', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'processor.handler',
      code: lambda.Code.fromAsset('lambda/processor'),
      events: [
        new lambdaEventSources.SqsEventSource(processingQueue, {
          batchSize: 10 // Process up to 10 messages at once, because we're efficient
        })
      ]
    });
    
    const notificationHandler = new lambda.Function(this, 'NotificationHandler', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'notifications.handler',
      code: lambda.Code.fromAsset('lambda/notifications'),
      events: [
        new lambdaEventSources.SnsEventSource(notificationTopic)
      ]
    });
    
    // EventBridge rules - the bouncers that decide who gets in
    new events.Rule(this, 'ProcessingRule', {
      eventBus,
      eventPattern: {
        source: ['myapp.orders'],
        detailType: ['Order Placed']
      },
      targets: [
        new eventsTargets.SqsQueue(processingQueue),
        new eventsTargets.SnsTopic(notificationTopic)
      ]
    });
    
    // API Gateway that just throws events and walks away
    const api = new apigateway.RestApi(this, 'API', {
      restApiName: 'Event-Driven API',
      description: 'An API that delegates like a proper manager'
    });
    
    const eventPublisher = new lambda.Function(this, 'EventPublisher', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'publisher.handler',
      code: lambda.Code.fromInline(`
        const { EventBridgeClient, PutEventsCommand } = require('@aws-sdk/client-eventbridge');
        const eventbridge = new EventBridgeClient();
        
        exports.handler = async (event) => {
          try {
            // Publish event and immediately return - fire and forget, baby!
            await eventbridge.send(new PutEventsCommand({
              Entries: [{
                Source: 'myapp.orders',
                DetailType: 'Order Placed',
                Detail: JSON.stringify(JSON.parse(event.body)),
                EventBusName: '${eventBus.eventBusName}'
              }]
            }));
            
            return {
              statusCode: 202, // Accepted - we'll get to it when we get to it
              body: JSON.stringify({ message: 'Event published successfully' })
            };
          } catch (error) {
            console.error('Failed to publish event:', error);
            return {
              statusCode: 500,
              body: JSON.stringify({ error: 'Event publishing failed, blame AWS' })
            };
          }
        };
      `),
      environment: {
        EVENT_BUS_NAME: eventBus.eventBusName
      }
    });
    
    // Grant permissions because AWS security is tighter than a jar of pickles
    eventBus.grantPutEventsTo(eventPublisher);
    
    api.root.addMethod('POST', new apigateway.LambdaIntegration(eventPublisher));
  }
}
```

#### Advanced Event Patterns That Don't Suck

**1. The Saga Pattern (For When You Need Coordination Without Tears)**

```typescript
// Because sometimes you need to coordinate multiple services
// without turning into a microservices horror story
export class OrderSagaPattern extends Construct {
  public readonly stateMachine: stepfunctions.StateMachine;
  
  constructor(scope: Construct, id: string, props: OrderSagaProps) {
    super(scope, id);
    
    // Define the saga steps - because life is a series of small disappointments
    const validateOrder = this.createValidationTask(props);
    const reserveInventory = this.createInventoryTask(props);
    const processPayment = this.createPaymentTask(props);
    const fulfillOrder = this.createFulfillmentTask(props);
    
    // Compensation tasks - for when things go wrong (and they will)
    const releaseInventory = this.createInventoryReleaseTask(props);
    const refundPayment = this.createRefundTask(props);
    const cancelOrder = this.createCancellationTask(props);
    
    // Build the workflow - like a Choose Your Own Adventure book, but for commerce
    const definition = validateOrder
      .next(
        new stepfunctions.Choice(this, 'OrderValidChoice')
          .when(
            stepfunctions.Condition.booleanEquals('$.orderValid', true),
            reserveInventory
              .next(
                new stepfunctions.Choice(this, 'InventoryChoice')
                  .when(
                    stepfunctions.Condition.booleanEquals('$.inventoryReserved', true),
                    processPayment
                      .next(
                        new stepfunctions.Choice(this, 'PaymentChoice')
                          .when(
                            stepfunctions.Condition.booleanEquals('$.paymentProcessed', true),
                            fulfillOrder
                          )
                          .otherwise(
                            // Payment failed - release inventory and cry
                            releaseInventory.next(cancelOrder)
                          )
                      )
                  )
                  .otherwise(
                    // No inventory - just cancel
                    cancelOrder
                  )
              )
          )
          .otherwise(
            // Invalid order - immediate cancellation
            cancelOrder
          )
      );
    
    this.stateMachine = new stepfunctions.StateMachine(this, 'OrderSaga', {
      definition,
      timeout: Duration.minutes(30), // If it takes longer than this, something's definitely wrong
      tracingEnabled: true // So we can see where it all went wrong
    });
  }
  
  private createValidationTask(props: OrderSagaProps): stepfunctions.Task {
    const validateFunction = new lambda.Function(this, 'ValidateOrder', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'validate.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async (event) => {
          // Simulate validation logic that occasionally has opinions
          const isValid = Math.random() > 0.1; // 90% success rate, which is optimistic
          
          return {
            ...event,
            orderValid: isValid,
            validationMessage: isValid 
              ? 'Order looks legitimate' 
              : 'Order validation failed - probably user error'
          };
        };
      `),
      timeout: Duration.seconds(30)
    });
    
    return new stepfunctionsTasks.LambdaInvoke(this, 'ValidateOrderTask', {
      lambdaFunction: validateFunction,
      resultPath: '$'
    });
  }
  
  private createInventoryTask(props: OrderSagaProps): stepfunctions.Task {
    const inventoryFunction = new lambda.Function(this, 'ReserveInventory', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'inventory.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async (event) => {
          // Simulate inventory check - sometimes we're out of stock
          const hasInventory = Math.random() > 0.2; // 80% availability
          
          return {
            ...event,
            inventoryReserved: hasInventory,
            inventoryMessage: hasInventory 
              ? 'Inventory successfully reserved' 
              : 'Out of stock - blame supply chain issues'
          };
        };
      `),
      timeout: Duration.seconds(30)
    });
    
    return new stepfunctionsTasks.LambdaInvoke(this, 'ReserveInventoryTask', {
      lambdaFunction: inventoryFunction,
      resultPath: '$'
    });
  }
  
  private createPaymentTask(props: OrderSagaProps): stepfunctions.Task {
    // Payment processing - where dreams go to die
    const paymentFunction = new lambda.Function(this, 'ProcessPayment', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'payment.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async (event) => {
          // Simulate payment processing - credit cards are mysterious
          const paymentSuccess = Math.random() > 0.15; // 85% success rate
          
          return {
            ...event,
            paymentProcessed: paymentSuccess,
            paymentMessage: paymentSuccess 
              ? 'Payment processed successfully' 
              : 'Payment failed - insufficient funds or expired card'
          };
        };
      `),
      timeout: Duration.seconds(60) // Payments take longer because banks
    });
    
    return new stepfunctionsTasks.LambdaInvoke(this, 'ProcessPaymentTask', {
      lambdaFunction: paymentFunction,
      resultPath: '$'
    });
  }
  
  private createFulfillmentTask(props: OrderSagaProps): stepfunctions.Task {
    const fulfillmentFunction = new lambda.Function(this, 'FulfillOrder', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'fulfillment.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async (event) => {
          // Final step - actually fulfill the order
          return {
            ...event,
            orderFulfilled: true,
            fulfillmentMessage: 'Order fulfilled successfully - customer will be happy',
            orderStatus: 'COMPLETED'
          };
        };
      `),
      timeout: Duration.seconds(30)
    });
    
    return new stepfunctionsTasks.LambdaInvoke(this, 'FulfillOrderTask', {
      lambdaFunction: fulfillmentFunction,
      resultPath: '$'
    });
  }
  
  // Compensation functions - for when we need to undo our mistakes
  private createInventoryReleaseTask(props: OrderSagaProps): stepfunctions.Task {
    const releaseFunction = new lambda.Function(this, 'ReleaseInventory', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'release.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async (event) => {
          return {
            ...event,
            inventoryReleased: true,
            releaseMessage: 'Inventory released back to stock'
          };
        };
      `),
      timeout: Duration.seconds(30)
    });
    
    return new stepfunctionsTasks.LambdaInvoke(this, 'ReleaseInventoryTask', {
      lambdaFunction: releaseFunction,
      resultPath: '$'
    });
  }
  
  private createRefundTask(props: OrderSagaProps): stepfunctions.Task {
    const refundFunction = new lambda.Function(this, 'RefundPayment', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'refund.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async (event) => {
          return {
            ...event,
            paymentRefunded: true,
            refundMessage: 'Payment refunded - customer slightly less angry'
          };
        };
      `),
      timeout: Duration.seconds(60)
    });
    
    return new stepfunctionsTasks.LambdaInvoke(this, 'RefundPaymentTask', {
      lambdaFunction: refundFunction,
      resultPath: '$'
    });
  }
  
  private createCancellationTask(props: OrderSagaProps): stepfunctions.Task {
    const cancelFunction = new lambda.Function(this, 'CancelOrder', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'cancel.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async (event) => {
          return {
            ...event,
            orderCancelled: true,
            cancellationMessage: 'Order cancelled - better luck next time',
            orderStatus: 'CANCELLED'
          };
        };
      `),
      timeout: Duration.seconds(30)
    });
    
    return new stepfunctionsTasks.LambdaInvoke(this, 'CancelOrderTask', {
      lambdaFunction: cancelFunction,
      resultPath: '$'
    });
  }
}
```

**2. The Circuit Breaker Pattern (For When External APIs Have Trust Issues)**

```typescript
// Because external APIs are like unreliable friends - sometimes they're there, sometimes they're not
export class CircuitBreakerConstruct extends Construct {
  public readonly processor: lambda.Function;
  public readonly statusTable: dynamodb.Table;
  
  constructor(scope: Construct, id: string, props: CircuitBreakerProps) {
    super(scope, id);
    
    // DynamoDB table to track circuit breaker state
    this.statusTable = new dynamodb.Table(this, 'CircuitBreakerStatus', {
      tableName: `circuit-breaker-${props.serviceName}`,
      partitionKey: { name: 'serviceEndpoint', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      timeToLiveAttribute: 'ttl',
      removalPolicy: RemovalPolicy.DESTROY // For learning purposes
    });
    
    this.processor = new lambda.Function(this, 'CircuitBreakerProcessor', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'circuitbreaker.handler',
      code: lambda.Code.fromInline(`
        const { DynamoDBClient, GetItemCommand, PutItemCommand } = require('@aws-sdk/client-dynamodb');
        const { marshall, unmarshall } = require('@aws-sdk/util-dynamodb');
        const dynamodb = new DynamoDBClient();
        
        const FAILURE_THRESHOLD = 5; // After 5 failures, we give up temporarily
        const RECOVERY_TIMEOUT = 60000; // 1 minute timeout before trying again
        
        exports.handler = async (event) => {
          const endpoint = event.endpoint || 'default';
          const tableName = process.env.STATUS_TABLE_NAME;
          
          try {
            // Check circuit breaker status
            const status = await getCircuitBreakerStatus(tableName, endpoint);
            
            if (status.state === 'OPEN') {
              // Circuit is open - fail fast
              return {
                statusCode: 503,
                body: JSON.stringify({
                  error: 'Service temporarily unavailable - circuit breaker is open',
                  message: 'External service is having issues, try again later'
                })
              };
            }
            
            if (status.state === 'HALF_OPEN') {
              // Circuit is half-open - one attempt allowed
              console.log('Circuit breaker is half-open, attempting single request');
            }
            
            // Attempt the external call
            const result = await callExternalService(event);
            
            if (result.success) {
              // Success - reset the circuit breaker
              await updateCircuitBreakerStatus(tableName, endpoint, 'CLOSED', 0);
              return {
                statusCode: 200,
                body: JSON.stringify(result.data)
              };
            } else {
              // Failure - increment failure count
              const newFailureCount = status.failureCount + 1;
              
              if (newFailureCount >= FAILURE_THRESHOLD) {
                // Open the circuit breaker
                await updateCircuitBreakerStatus(tableName, endpoint, 'OPEN', newFailureCount);
                console.log('Circuit breaker opened due to excessive failures');
              } else {
                await updateCircuitBreakerStatus(tableName, endpoint, 'CLOSED', newFailureCount);
              }
              
              return {
                statusCode: 502,
                body: JSON.stringify({
                  error: 'External service call failed',
                  failureCount: newFailureCount
                })
              };
            }
          } catch (error) {
            console.error('Circuit breaker error:', error);
            return {
              statusCode: 500,
              body: JSON.stringify({ error: 'Internal circuit breaker error' })
            };
          }
        };
        
        async function getCircuitBreakerStatus(tableName, endpoint) {
          try {
            const result = await dynamodb.send(new GetItemCommand({
              TableName: tableName,
              Key: marshall({ serviceEndpoint: endpoint })
            }));
            
            if (result.Item) {
              const status = unmarshall(result.Item);
              
              // Check if we should transition from OPEN to HALF_OPEN
              if (status.state === 'OPEN' && Date.now() - status.lastFailureTime > RECOVERY_TIMEOUT) {
                await updateCircuitBreakerStatus(tableName, endpoint, 'HALF_OPEN', status.failureCount);
                return { state: 'HALF_OPEN', failureCount: status.failureCount };
              }
              
              return status;
            } else {
              // No record - circuit is closed by default
              return { state: 'CLOSED', failureCount: 0 };
            }
          } catch (error) {
            console.error('Error getting circuit breaker status:', error);
            return { state: 'CLOSED', failureCount: 0 };
          }
        }
        
        async function updateCircuitBreakerStatus(tableName, endpoint, state, failureCount) {
          const item = {
            serviceEndpoint: endpoint,
            state: state,
            failureCount: failureCount,
            lastFailureTime: Date.now(),
            ttl: Math.floor(Date.now() / 1000) + 3600 // 1 hour TTL
          };
          
          await dynamodb.send(new PutItemCommand({
            TableName: tableName,
            Item: marshall(item)
          }));
        }
        
        async function callExternalService(event) {
          // Simulate calling an external service that sometimes fails
          // In real life, this would be your actual external API call
          const failureRate = 0.3; // 30% failure rate to test circuit breaker
          
          // Simulate network delay
          await new Promise(resolve => setTimeout(resolve, Math.random() * 1000));
          
          if (Math.random() < failureRate) {
            return { success: false, error: 'External service timeout or error' };
          } else {
            return { 
              success: true, 
              data: { 
                message: 'External service call successful',
                timestamp: Date.now()
              }
            };
          }
        }
      `),
      environment: {
        STATUS_TABLE_NAME: this.statusTable.tableName
      },
      timeout: Duration.seconds(30)
    });
    
    // Grant permissions
    this.statusTable.grantReadWriteData(this.processor);
  }
}
```

#### 🛠️ Hands-On Lab 4.1: Build a Real-World Event-Driven System

**Challenge**: Create an e-commerce order processing system that handles the chaos of real-world commerce

**Your Mission**: Build a system that can handle:
- Order validation (because customers lie)
- Inventory management (because stock is finite)
- Payment processing (because money is complicated)
- Shipping coordination (because logistics is hard)
- Customer notifications (because people like to know what's happening)

**The Twist**: Your system must handle failures gracefully and provide full observability because when things go wrong (and they will), you need to know why.

**Architecture Requirements**:
```
API Gateway → Lambda → EventBridge → [Multiple Processing Flows]
                          ↓
├── Order Validation Queue → Lambda → DynamoDB
├── Inventory Queue → Lambda → RDS/DynamoDB  
├── Payment Queue → Lambda → External Payment API
├── Shipping Queue → Lambda → External Shipping API
└── Notification Queue → Lambda → SNS/SES
```

**Success Criteria**:
- System handles 1000+ concurrent orders without breaking
- Failed orders automatically retry with exponential backoff
- Dead letter queues capture unprocessable messages
- Circuit breakers protect against external service failures
- Full tracing with X-Ray shows you exactly where things went wrong
- CloudWatch alarms notify you before customers start complaining

**💰 Cost Warning**: This will cost ~$5-10/day while running. Deploy → test thoroughly → screenshot everything → destroy same day!

---

### Lesson 4.2: Complex Data Flow Orchestration
*"Making data dance between services like a choreographer who's had too much coffee"*

#### The Art of Data Choreography

Look, data doesn't just magically appear where you need it. It needs to be coaxed, cajoled, and occasionally threatened into moving from Point A to Point B. And sometimes Point C, D, and E because your architecture grew organically like a weed.

**Stream Processing with Kinesis (For When You Have Trust Issues with Batch Processing)**

```typescript
export class DataStreamingPattern extends Construct {
  public readonly dataStream: kinesis.Stream;
  public readonly analyticsStream: kinesisanalytics.CfnApplication;
  public readonly destinationBucket: s3.Bucket;
  
  constructor(scope: Construct, id: string, props: DataStreamingProps) {
    super(scope, id);
    
    // Kinesis stream - the highway for your data
    this.dataStream = new kinesis.Stream(this, 'DataStream', {
      streamName: props.streamName,
      shardCount: props.shardCount || 2, // Start small, scale later when you realize you underestimated
      retentionPeriod: Duration.days(7), // A week should be enough to fix any disasters
      streamModeDetails: {
        streamMode: kinesis.StreamMode.PROVISIONED // Because on-demand is for quitters
      }
    });
    
    // S3 bucket for storing processed data
    this.destinationBucket = new s3.Bucket(this, 'ProcessedDataBucket', {
      bucketName: `processed-data-${props.environment}-${this.node.addr}`.toLowerCase(),
      lifecycleRules: [{
        id: 'DataLifecycle',
        transitions: [
          {
            storageClass: s3.StorageClass.INTELLIGENT_TIERING,
            transitionAfter: Duration.days(30)
          },
          {
            storageClass: s3.StorageClass.GLACIER,
            transitionAfter: Duration.days(90)
          }
        ]
      }],
      removalPolicy: RemovalPolicy.DESTROY // For learning - don't do this in prod unless you enjoy panic
    });
    
    // Kinesis Data Firehose - for when you want data delivered like a reliable pizza service
    const deliveryStream = new kinesisfirehose.CfnDeliveryStream(this, 'DataDeliveryStream', {
      deliveryStreamName: `${props.streamName}-delivery`,
      deliveryStreamType: 'KinesisStreamAsSource',
      kinesisStreamSourceConfiguration: {
        kinesisStreamArn: this.dataStream.streamArn,
        roleArn: this.createFirehoseRole().roleArn
      },
      s3DestinationConfiguration: {
        bucketArn: this.destinationBucket.bucketArn,
        prefix: 'year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/',
        errorOutputPrefix: 'errors/',
        bufferingHints: {
          sizeInMBs: 5, // Buffer size - balance between latency and efficiency
          intervalInSeconds: 300 // 5 minutes - not too fast, not too slow
        },
        compressionFormat: 'GZIP', // Because storage costs money
        processingConfiguration: {
          enabled: true,
          processors: [{
            type: 'Lambda',
            parameters: [{
              parameterName: 'LambdaArn',
              parameterValue: this.createDataProcessor().functionArn
            }]
          }]
        }
      }
    });
    
    // Real-time analytics application
    this.analyticsStream = new kinesisanalytics.CfnApplication(this, 'RealTimeAnalytics', {
      applicationName: `${props.streamName}-analytics`,
      applicationDescription: 'Real-time analytics that hopefully provides insights',
      inputs: [{
        namePrefix: 'source_sql_stream',
        kinesisStreamsInput: {
          resourceArn: this.dataStream.streamArn,
          roleArn: this.createAnalyticsRole().roleArn
        },
        inputSchema: {
          recordColumns: [
            { name: 'timestamp', sqlType: 'TIMESTAMP', mapping: '$.timestamp' },
            { name: 'user_id', sqlType: 'VARCHAR(32)', mapping: '$.userId' },
            { name: 'event_type', sqlType: 'VARCHAR(64)', mapping: '$.eventType' },
            { name: 'data', sqlType: 'VARCHAR(1024)', mapping: '$.data' }
          ],
          recordFormat: {
            recordFormatType: 'JSON',
            mappingParameters: {
              jsonMappingParameters: {
                recordRowPath: '$'
              }
            }
          }
        }
      }],
      applicationCode: `
        -- SQL for people who like to pretend they're data scientists
        CREATE OR REPLACE STREAM \"DESTINATION_SQL_STREAM\" (
          event_type VARCHAR(64),
          event_count INTEGER,
          window_start TIMESTAMP,
          window_end TIMESTAMP
        );
        
        CREATE OR REPLACE PUMP \"STREAM_PUMP\" AS INSERT INTO \"DESTINATION_SQL_STREAM\"
        SELECT STREAM 
          event_type,
          COUNT(*) as event_count,
          ROWTIME_TO_TIMESTAMP(RANGE_START) as window_start,
          ROWTIME_TO_TIMESTAMP(RANGE_END) as window_end
        FROM SOURCE_SQL_STREAM_001
        GROUP BY event_type, RANGE(PARTITION BY event_type RANGE INTERVAL '1' MINUTE);
      `
    });
    
    // Lambda function for processing data before storage
    const dataProcessor = this.createDataProcessor();
    
    // Grant necessary permissions because AWS security is like an overprotective parent
    this.dataStream.grantRead(deliveryStream);
    this.destinationBucket.grantWrite(deliveryStream);
  }
  
  private createDataProcessor(): lambda.Function {
    return new lambda.Function(this, 'DataProcessor', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'processor.handler',
      code: lambda.Code.fromInline(`
        const zlib = require('zlib');
        
        exports.handler = async (event) => {
          const output = [];
          
          for (const record of event.records) {
            try {
              // Decode the data - because Kinesis likes to be cryptic
              const payload = Buffer.from(record.data, 'base64').toString('utf-8');
              const data = JSON.parse(payload);
              
              // Process the data - add timestamps, validation, enrichment
              const processedData = {
                ...data,
                processedAt: new Date().toISOString(),
                processingVersion: '1.0',
                isValid: this.validateData(data),
                enrichedData: this.enrichData(data)
              };
              
              // Encode back to base64
              const outputRecord = {
                recordId: record.recordId,
                result: 'Ok',
                data: Buffer.from(JSON.stringify(processedData)).toString('base64')
              };
              
              output.push(outputRecord);
            } catch (error) {
              console.error('Processing error:', error);
              
              // Mark record as failed - it goes to error prefix in S3
              output.push({
                recordId: record.recordId,
                result: 'ProcessingFailed'
              });
            }
          }
          
          return { records: output };
        };
        
        function validateData(data) {
          // Basic validation - in real life, this would be more sophisticated
          return data && 
                 data.userId && 
                 data.eventType && 
                 data.timestamp;
        }
        
        function enrichData(data) {
          // Add some enrichment - user segment, geographic info, etc.
          return {
            userSegment: data.userId ? getUserSegment(data.userId) : 'unknown',
            region: data.sourceIp ? getRegionFromIp(data.sourceIp) : 'unknown',
            deviceType: data.userAgent ? getDeviceType(data.userAgent) : 'unknown'
          };
        }
        
        function getUserSegment(userId) {
          // Simulate user segmentation logic
          const hash = userId.split('').reduce((a, b) => {
            a = ((a << 5) - a) + b.charCodeAt(0);
            return a & a;
          }, 0);
          
          const segments = ['premium', 'standard', 'basic'];
          return segments[Math.abs(hash) % segments.length];
        }
        
        function getRegionFromIp(ip) {
          // Simulate IP geolocation - in real life, use a proper service
          return 'us-east-1'; // Everyone is in us-east-1, obviously
        }
        
        function getDeviceType(userAgent) {
          if (!userAgent) return 'unknown';
          if (userAgent.includes('Mobile')) return 'mobile';
          if (userAgent.includes('Tablet')) return 'tablet';
          return 'desktop';
        }
      `),
      timeout: Duration.minutes(5) // Firehose gives us up to 5 minutes
    });
  }
  
  private createFirehoseRole(): iam.Role {
    const role = new iam.Role(this, 'FirehoseRole', {
      assumedBy: new iam.ServicePrincipal('firehose.amazonaws.com'),
      inlinePolicies: {
        FirehoseDeliveryRolePolicy: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              effect: iam.Effect.ALLOW,
              actions: [
                'kinesis:DescribeStream',
                'kinesis:GetShardIterator',
                'kinesis:GetRecords'
              ],
              resources: [this.dataStream.streamArn]
            }),
            new iam.PolicyStatement({
              effect: iam.Effect.ALLOW,
              actions: [
                's3:AbortMultipartUpload',
                's3:GetBucketLocation',
                's3:GetObject',
                's3:ListBucket',
                's3:ListBucketMultipartUploads',
                's3:PutObject'
              ],
              resources: [
                this.destinationBucket.bucketArn,
                `${this.destinationBucket.bucketArn}/*`
              ]
            })
          ]
        })
      }
    });
    
    return role;
  }
  
  private createAnalyticsRole(): iam.Role {
    return new iam.Role(this, 'AnalyticsRole', {
      assumedBy: new iam.ServicePrincipal('kinesisanalytics.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/KinesisAnalyticsServiceRole')
      ]
    });
  }
}
```

**Data Lake Architecture (For When You Want to Store Everything and Figure Out What to Do With It Later)**

```typescript
export class DataLakePattern extends Construct {
  public readonly rawDataBucket: s3.Bucket;
  public readonly processedDataBucket: s3.Bucket;
  public readonly catalogDatabase: glue.CfnDatabase;
  public readonly etlJob: glue.CfnJob;
  
  constructor(scope: Construct, id: string, props: DataLakeProps) {
    super(scope, id);
    
    // Raw data bucket - where data goes to live before it gets cleaned up
    this.rawDataBucket = new s3.Bucket(this, 'RawDataBucket', {
      bucketName: `raw-data-${props.environment}-${this.node.addr}`.toLowerCase(),
      partitionKeyTransforms: [
        s3.PartitionKeyTransform.prefix('year='),
        s3.PartitionKeyTransform.prefix('month='),
        s3.PartitionKeyTransform.prefix('day=')
      ],
      eventBridgeEnabled: true, // So we know when new data arrives
      lifecycleRules: [{
        id: 'RawDataLifecycle',
        transitions: [
          {
            storageClass: s3.StorageClass.INTELLIGENT_TIERING,
            transitionAfter: Duration.days(30)
          }
        ]
      }],
      removalPolicy: RemovalPolicy.DESTROY
    });
    
    // Processed data bucket - where data goes after it's been through the washing machine
    this.processedDataBucket = new s3.Bucket(this, 'ProcessedDataBucket', {
      bucketName: `processed-data-${props.environment}-${this.node.addr}`.toLowerCase(),
      lifecycleRules: [{
        id: 'ProcessedDataLifecycle',
        transitions: [
          {
            storageClass: s3.StorageClass.INTELLIGENT_TIERING,
            transitionAfter: Duration.days(30)
          },
          {
            storageClass: s3.StorageClass.GLACIER,
            transitionAfter: Duration.days(90)
          }
        ]
      }],
      removalPolicy: RemovalPolicy.DESTROY
    });
    
    // Glue Data Catalog - the librarian of your data lake
    this.catalogDatabase = new glue.CfnDatabase(this, 'DataCatalog', {
      catalogId: Stack.of(this).account,
      databaseInput: {
        name: `${props.databaseName}_${props.environment}`,
        description: 'Data catalog for our magnificent data lake'
      }
    });
    
    // Glue Crawler - the scout that explores your data and figures out what it is
    const crawler = new glue.CfnCrawler(this, 'DataCrawler', {
      name: `${props.databaseName}-crawler-${props.environment}`,
      role: this.createGlueRole().roleArn,
      databaseName: this.catalogDatabase.ref,
      targets: {
        s3Targets: [
          {
            path: `s3://${this.rawDataBucket.bucketName}/`,
            exclusions: ['**/_SUCCESS', '**/_metadata']
          },
          {
            path: `s3://${this.processedDataBucket.bucketName}/`,
            exclusions: ['**/_SUCCESS', '**/_metadata']
          }
        ]
      },
      schedule: {
        scheduleExpression: 'cron(0 6 * * ? *)' // Run daily at 6 AM because data doesn't sleep
      },
      configuration: JSON.stringify({
        Version: '1.0',
        CrawlerOutput: {
          Partitions: { AddOrUpdateBehavior: 'InheritFromTable' },
          Tables: { AddOrUpdateBehavior: 'MergeNewColumns' }
        }
      })
    });
    
    // ETL Job - the data janitor that cleans up your mess
    this.etlJob = new glue.CfnJob(this, 'DataETLJob', {
      name: `${props.databaseName}-etl-${props.environment}`,
      role: this.createGlueRole().roleArn,
      command: {
        name: 'glueetl',
        scriptLocation: `s3://${this.createScriptBucket().bucketName}/etl-script.py`,
        pythonVersion: '3'
      },
      defaultArguments: {
        '--job-language': 'python',
        '--job-bookmark-option': 'job-bookmark-enable',
        '--enable-continuous-cloudwatch-log': 'true',
        '--enable-spark-ui': 'true',
        '--spark-event-logs-path': `s3://${this.processedDataBucket.bucketName}/spark-logs/`,
        '--source-bucket': this.rawDataBucket.bucketName,
        '--target-bucket': this.processedDataBucket.bucketName,
        '--database-name': this.catalogDatabase.ref
      },
      maxRetries: 3, // Because sometimes Spark has mood swings
      timeout: 60, // 60 minutes should be enough for most ETL jobs
      glueVersion: '3.0',
      numberOfWorkers: 2, // Start small, scale up when you realize your data is bigger than expected
      workerType: 'Standard' // Because we're not made of money
    });
    
    // EventBridge rule to trigger ETL when new data arrives
    new events.Rule(this, 'NewDataRule', {
      eventPattern: {
        source: ['aws.s3'],
        detailType: ['Object Created'],
        detail: {
          bucket: {
            name: [this.rawDataBucket.bucketName]
          }
        }
      },
      targets: [
        new eventsTargets.SfnStateMachine(this.createETLWorkflow())
      ]
    });
  }
  
  private createGlueRole(): iam.Role {
    const role = new iam.Role(this, 'GlueServiceRole', {
      assumedBy: new iam.ServicePrincipal('glue.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSGlueServiceRole')
      ],
      inlinePolicies: {
        DataLakeAccess: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              effect: iam.Effect.ALLOW,
              actions: [
                's3:GetObject',
                's3:PutObject',
                's3:DeleteObject',
                's3:ListBucket'
              ],
              resources: [
                this.rawDataBucket.bucketArn,
                `${this.rawDataBucket.bucketArn}/*`,
                this.processedDataBucket.bucketArn,
                `${this.processedDataBucket.bucketArn}/*`
              ]
            })
          ]
        })
      }
    });
    
    return role;
  }
  
  private createScriptBucket(): s3.Bucket {
    const scriptBucket = new s3.Bucket(this, 'GlueScriptBucket', {
      removalPolicy: RemovalPolicy.DESTROY
    });
    
    // Deploy the ETL script
    new s3deploy.BucketDeployment(this, 'DeployETLScript', {
      sources: [s3deploy.Source.data('etl-script.py', `
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F

# Get job arguments
args = getResolvedOptions(sys.argv, [
    'JOB_NAME', 
    'source-bucket', 
    'target-bucket', 
    'database-name'
])

# Initialize Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data from the catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database=args['database_name'],
    table_name="raw_data"  # This would be created by the crawler
)

# Transform the data - because raw data is like raw fish, it needs preparation
def process_data(glue_df):
    # Convert to Spark DataFrame for easier manipulation
    df = glue_df.toDF()
    
    # Add processing timestamp
    df = df.withColumn("processed_timestamp", F.current_timestamp())
    
    # Clean up data types
    df = df.withColumn("user_id", F.col("user_id").cast("string"))
    df = df.withColumn("event_timestamp", F.to_timestamp("event_timestamp"))
    
    # Add derived columns
    df = df.withColumn("event_date", F.to_date("event_timestamp"))
    df = df.withColumn("event_hour", F.hour("event_timestamp"))
    
    # Filter out invalid records because garbage in, garbage out
    df = df.filter(
        F.col("user_id").isNotNull() & 
        F.col("event_timestamp").isNotNull() &
        F.col("event_type").isNotNull()
    )
    
    # Convert back to DynamicFrame
    return DynamicFrame.fromDF(df, glueContext, "processed_data")

# Process the data
processed_data = process_data(datasource)

# Write processed data back to S3 in Parquet format
glueContext.write_dynamic_frame.from_options(
    frame=processed_data,
    connection_type="s3",
    connection_options={
        "path": f"s3://{args['target_bucket']}/processed/",
        "partitionKeys": ["event_date", "event_hour"]
    },
    format="parquet"
)

job.commit()
      `)],
      destinationBucket: scriptBucket,
      destinationKeyPrefix: ''
    });
    
    return scriptBucket;
  }
  
  private createETLWorkflow(): stepfunctions.StateMachine {
    // Define ETL workflow steps
    const startJob = new stepfunctionsTasks.GlueStartJobRun(this, 'StartETLJob', {
      glueJobName: this.etlJob.name!,
      integrationPattern: stepfunctions.IntegrationPattern.RUN_JOB
    });
    
    const runCrawler = new stepfunctionsTasks.CallAwsService(this, 'RunCrawler', {
      service: 'glue',
      action: 'startCrawler',
      parameters: {
        'Name': `${this.catalogDatabase.ref}-crawler`
      },
      integrationPattern: stepfunctions.IntegrationPattern.REQUEST_RESPONSE
    });
    
    // Define the workflow
    const definition = startJob
      .next(
        new stepfunctions.Wait(this, 'WaitForETL', {
          time: stepfunctions.WaitTime.duration(Duration.minutes(2))
        })
      )
      .next(runCrawler);
    
    return new stepfunctions.StateMachine(this, 'ETLWorkflow', {
      definition,
      timeout: Duration.hours(2) // ETL jobs can take a while
    });
  }
}
```

#### 🛠️ Hands-On Lab 4.2: Build a Real-Time Analytics Pipeline

**Challenge**: Create a system that processes streaming data and provides real-time insights

**Your Mission**: Build a pipeline that:
1. Ingests real-time user activity data
2. Processes and enriches the data in real-time
3. Stores both raw and processed data for different use cases
4. Provides real-time dashboards and alerts
5. Handles late-arriving data and out-of-order events

**The Reality Check**: Your system needs to handle real-world messiness:
- Data arrives out of order (because the internet is chaotic)
- Some events are duplicated (because retry logic is aggressive)
- External enrichment services sometimes fail (because they're maintained by someone else)
- Schema evolution happens (because requirements change)

**Success Criteria**:
- Processes 10,000+ events per minute without choking
- Handles duplicate events gracefully
- Enriches data with external APIs using circuit breakers
- Provides sub-minute latency for alerts
- Stores data cost-effectively with proper lifecycle management
- Maintains data quality metrics and alerts

**💰 Cost Warning**: This beast will cost ~$10-15/day while running. Test thoroughly, then tear it down like you're demolishing a poorly built shed!

---

### Lesson 4.3: Custom CDK Resources and Providers
*"When AWS doesn't give you exactly what you want, you make your own"*

#### Sometimes AWS Just Doesn't Get It

Look, AWS is brilliant, but sometimes they're like that friend who almost gets what you're asking for but not quite. That's when you roll up your sleeves and build your own custom resources.

**Custom Resource Pattern (The "Fine, I'll Do It Myself" Approach)**

```typescript
export class CustomResourceConstruct extends Construct {
  public readonly customResource: CustomResource;
  public readonly provider: cr.Provider;
  
  constructor(scope: Construct, id: string, props: CustomResourceProps) {
    super(scope, id);
    
    // Lambda function that does the actual work
    const onEventHandler = new lambda.Function(this, 'OnEventHandler', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.onEvent',
      code: lambda.Code.fromInline(`
        const aws = require('aws-sdk');
        
        exports.onEvent = async (event) => {
          console.log('Custom resource event:', JSON.stringify(event, null, 2));
          
          const requestType = event.RequestType;
          const properties = event.ResourceProperties;
          
          try {
            switch (requestType) {
              case 'Create':
                return await handleCreate(properties);
              case 'Update':
                return await handleUpdate(properties, event.OldResourceProperties);
              case 'Delete':
                return await handleDelete(properties);
              default:
                throw new Error('Unknown request type: ' + requestType);
            }
          } catch (error) {
            console.error('Custom resource error:', error);
            throw error;
          }
        };
        
        async function handleCreate(properties) {
          // Create your custom resource
          console.log('Creating custom resource with properties:', properties);
          
          // Simulate some work - in real life, this might be:
          // - Calling an external API
          // - Setting up a third-party service
          // - Configuring something AWS doesn't support yet
          
          const resourceId = generateResourceId();
          
          // Example: Configure external monitoring service
          const monitoringConfig = await configureExternalMonitoring({
            serviceName: properties.ServiceName,
            alertEmail: properties.AlertEmail,
            thresholds: properties.Thresholds
          });
          
          return {
            PhysicalResourceId: resourceId,
            Data: {
              ResourceId: resourceId,
              MonitoringUrl: monitoringConfig.url,
              ApiKey: monitoringConfig.apiKey // Don't do this in real life - use Secrets Manager
            }
          };
        }
        
        async function handleUpdate(properties, oldProperties) {
          console.log('Updating custom resource');
          console.log('New properties:', properties);
          console.log('Old properties:', oldProperties);
          
          // Update logic here
          const resourceId = properties.ResourceId || generateResourceId();
          
          return {
            PhysicalResourceId: resourceId,
            Data: {
              ResourceId: resourceId,
              UpdatedAt: new Date().toISOString()
            }
          };
        }
        
        async function handleDelete(properties) {
          console.log('Deleting custom resource with properties:', properties);
          
          // Cleanup logic here
          await cleanupExternalMonitoring(properties.ResourceId);
          
          return {
            PhysicalResourceId: properties.ResourceId
          };
        }
        
        function generateResourceId() {
          return 'custom-resource-' + Math.random().toString(36).substr(2, 9);
        }
        
        async function configureExternalMonitoring(config) {
          // Simulate external API call
          console.log('Configuring external monitoring for:', config.serviceName);
          
          // In real life, this would be an actual API call
          return {
            url: 'https://monitoring.example.com/dashboard/' + config.serviceName,
            apiKey: 'fake-api-key-' + Math.random().toString(36).substr(2, 9)
          };
        }
        
        async function cleanupExternalMonitoring(resourceId) {
          console.log('Cleaning up external monitoring for:', resourceId);
          // Cleanup logic here
        }
      `),
      timeout: Duration.minutes(5), // Custom resources can take a while
      logRetention: logs.RetentionDays.ONE_WEEK
    });
    
    // Optional: IsComplete handler for async operations
    const isCompleteHandler = new lambda.Function(this, 'IsCompleteHandler', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.isComplete',
      code: lambda.Code.fromInline(`
        exports.isComplete = async (event) => {
          console.log('Checking if custom resource operation is complete:', JSON.stringify(event, null, 2));
          
          const properties = event.ResourceProperties;
          const requestType = event.RequestType;
          
          // Check if the operation is complete
          // For async operations, you might check external service status
          
          if (requestType === 'Create' || requestType === 'Update') {
            // Simulate checking external service status
            const isReady = await checkExternalServiceStatus(properties.ResourceId);
            
            if (isReady) {
              return {
                IsComplete: true,
                Data: {
                  Status: 'Ready',
                  CompletedAt: new Date().toISOString()
                }
              };
            } else {
              return {
                IsComplete: false,
                Data: {
                  Status: 'Pending'
                }
              };
            }
          }
          
          // Delete operations are usually immediate
          return { IsComplete: true };
        };
        
        async function checkExternalServiceStatus(resourceId) {
          // Simulate checking external service - sometimes it's ready, sometimes not
          return Math.random() > 0.3; // 70% chance it's ready
        }
      `),
      timeout: Duration.minutes(1)
    });
    
    // Custom resource provider
    this.provider = new cr.Provider(this, 'CustomResourceProvider', {
      onEventHandler,
      isCompleteHandler, // Optional - only if you need async operations
      queryInterval: Duration.seconds(30), // How often to check if operation is complete
      totalTimeout: Duration.minutes(30), // Total timeout for the operation
      logRetention: logs.RetentionDays.ONE_WEEK
    });
    
    // The actual custom resource
    this.customResource = new CustomResource(this, 'CustomResource', {
      serviceToken: this.provider.serviceToken,
      properties: {
        ServiceName: props.serviceName,
        AlertEmail: props.alertEmail,
        Thresholds: props.thresholds,
        // Add a timestamp to force updates when needed
        UpdateTimestamp: new Date().toISOString()
      }
    });
  }
  
  // Getter methods to access custom resource attributes
  public getResourceId(): string {
    return this.customResource.getAtt('ResourceId').toString();
  }
  
  public getMonitoringUrl(): string {
    return this.customResource.getAtt('MonitoringUrl').toString();
  }
}
```

**Advanced Custom Resource: DNS Zone Manager**

```typescript
// Because sometimes you need to manage DNS zones in ways AWS Route53 doesn't quite support
export class DNSZoneManagerConstruct extends Construct {
  public readonly dnsZoneResource: CustomResource;
  
  constructor(scope: Construct, id: string, props: DNSZoneManagerProps) {
    super(scope, id);
    
    // IAM role for the custom resource Lambda
    const customResourceRole = new iam.Role(this, 'DNSManagerRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole')
      ],
      inlinePolicies: {
        DNSManagement: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              effect: iam.Effect.ALLOW,
              actions: [
                'route53:CreateHostedZone',
                'route53:DeleteHostedZone',
                'route53:GetHostedZone',
                'route53:ListHostedZones',
                'route53:ChangeResourceRecordSets',
                'route53:ListResourceRecordSets'
              ],
              resources: ['*'] // Be more specific in production
            }),
            new iam.PolicyStatement({
              effect: iam.Effect.ALLOW,
              actions: [
                'route53domains:UpdateDomainNameservers',
                'route53domains:GetDomainDetail'
              ],
              resources: ['*']
            })
          ]
        })
      }
    });
    
    const dnsManagerFunction = new lambda.Function(this, 'DNSManagerFunction', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      role: customResourceRole,
      code: lambda.Code.fromInline(`
        const aws = require('aws-sdk');
        const route53 = new aws.Route53();
        const route53Domains = new aws.Route53Domains();
        
        exports.handler = async (event) => {
          console.log('DNS Zone Manager event:', JSON.stringify(event, null, 2));
          
          const requestType = event.RequestType;
          const properties = event.ResourceProperties;
          
          try {
            switch (requestType) {
              case 'Create':
                return await createDNSZone(properties);
              case 'Update':
                return await updateDNSZone(properties, event.OldResourceProperties);
              case 'Delete':
                return await deleteDNSZone(properties);
              default:
                throw new Error('Unknown request type: ' + requestType);
            }
          } catch (error) {
            console.error('DNS Zone Manager error:', error);
            throw error;
          }
        };
        
        async function createDNSZone(properties) {
          const domainName = properties.DomainName;
          const isPrivate = properties.IsPrivate === 'true';
          const vpcId = properties.VpcId;
          const region = properties.Region;
          
          console.log('Creating hosted zone for domain:', domainName);
          
          const params = {
            Name: domainName,
            CallerReference: 'dns-manager-' + Date.now(),
            HostedZoneConfig: {
              Comment: 'Created by CDK DNS Zone Manager',
              PrivateZone: isPrivate
            }
          };
          
          if (isPrivate && vpcId) {
            params.VPC = {
              VPCRegion: region,
              VPCId: vpcId
            };
          }
          
          const result = await route53.createHostedZone(params).promise();
          const hostedZoneId = result.HostedZone.Id.replace('/hostedzone/', '');
          
          // If it's a public zone, update domain nameservers
          if (!isPrivate && properties.UpdateNameservers === 'true') {
            await updateDomainNameservers(domainName, result.DelegationSet.NameServers);
          }
          
          return {
            PhysicalResourceId: hostedZoneId,
            Data: {
              HostedZoneId: hostedZoneId,
              NameServers: result.DelegationSet.NameServers.join(',')
            }
          };
        }
        
        async function updateDNSZone(properties, oldProperties) {
          const hostedZoneId = properties.HostedZoneId;
          
          // DNS zones can't really be "updated" - most changes require recreation
          // But we can update records within the zone
          console.log('DNS Zone update requested - limited operations available');
          
          return {
            PhysicalResourceId: hostedZoneId,
            Data: {
              HostedZoneId: hostedZoneId,
              UpdatedAt: new Date().toISOString()
            }
          };
        }
        
        async function deleteDNSZone(properties) {
          const hostedZoneId = properties.HostedZoneId;
          
          if (!hostedZoneId) {
            console.log('No hosted zone ID provided, skipping deletion');
            return { PhysicalResourceId: 'deleted' };
          }
          
          console.log('Deleting hosted zone:', hostedZoneId);
          
          try {
            // First, clean up all records except NS and SOA
            await cleanupDNSRecords(hostedZoneId);
            
            // Then delete the hosted zone
            await route53.deleteHostedZone({
              Id: hostedZoneId
            }).promise();
            
            console.log('Hosted zone deleted successfully');
          } catch (error) {
            if (error.code === 'NoSuchHostedZone') {
              console.log('Hosted zone already deleted');
            } else {
              throw error;
            }
          }
          
          return { PhysicalResourceId: hostedZoneId };
        }
        
        async function cleanupDNSRecords(hostedZoneId) {
          console.log('Cleaning up DNS records in zone:', hostedZoneId);
          
          const records = await route53.listResourceRecordSets({
            HostedZoneId: hostedZoneId
          }).promise();
          
          // Delete all records except NS and SOA (which are required)
          const recordsToDelete = records.ResourceRecordSets.filter(
            record => record.Type !== 'NS' && record.Type !== 'SOA'
          );
          
          if (recordsToDelete.length > 0) {
            const changes = recordsToDelete.map(record => ({
              Action: 'DELETE',
              ResourceRecordSet: record
            }));
            
            await route53.changeResourceRecordSets({
              HostedZoneId: hostedZoneId,
              ChangeBatch: {
                Comment: 'Cleanup before zone deletion',
                Changes: changes
              }
            }).promise();
            
            console.log('Deleted', recordsToDelete.length, 'DNS records');
          }
        }
        
        async function updateDomainNameservers(domainName, nameServers) {
          console.log('Updating nameservers for domain:', domainName);
          
          try {
            await route53Domains.updateDomainNameservers({
              DomainName: domainName,
              Nameservers: nameServers.map(ns => ({ Name: ns }))
            }).promise();
            
            console.log('Domain nameservers updated successfully');
          } catch (error) {
            console.error('Failed to update domain nameservers:', error);
            // Don't fail the whole operation if nameserver update fails
          }
        }
      `),
      timeout: Duration.minutes(15), // DNS operations can be slow
      logRetention: logs.RetentionDays.ONE_WEEK
    });
    
    const provider = new cr.Provider(this, 'DNSZoneProvider', {
      onEventHandler: dnsManagerFunction,
      logRetention: logs.RetentionDays.ONE_WEEK
    });
    
    this.dnsZoneResource = new CustomResource(this, 'DNSZoneResource', {
      serviceToken: provider.serviceToken,
      properties: {
        DomainName: props.domainName,
        IsPrivate: props.isPrivate ? 'true' : 'false',
        VpcId: props.vpcId,
        Region: props.region || Stack.of(this).region,
        UpdateNameservers: props.updateNameservers ? 'true' : 'false'
      }
    });
  }
  
  public getHostedZoneId(): string {
    return this.dnsZoneResource.getAtt('HostedZoneId').toString();
  }
  
  public getNameServers(): string[] {
    return this.dnsZoneResource.getAtt('NameServers').toString().split(',');
  }
}
```

#### 🛠️ Hands-On Lab 4.3: Build a Multi-Cloud Integration Custom Resource

**Challenge**: Create a custom resource that integrates AWS with external services

**Your Mission**: Build a custom resource that:
1. Integrates with a third-party monitoring service (simulate with a mock API)
2. Handles async operations with polling
3. Manages secrets securely
4. Provides proper error handling and rollback
5. Includes comprehensive logging and observability

**The Scenario**: Your organization uses a third-party security monitoring service that needs to be configured whenever you deploy new infrastructure. AWS doesn't have native integration, so you need to build your own.

**Success Criteria**:
- Custom resource successfully creates/updates/deletes external monitoring configs
- Handles API rate limits and retries gracefully
- Secrets are managed securely (no hardcoded API keys)
- Operations are idempotent (running twice doesn't break things)
- Comprehensive error handling with meaningful error messages
- Full integration with CloudFormation lifecycle

**💰 Cost Warning**: Minimal cost for Lambda and CloudWatch logs, but don't leave test resources running!

---

## 📋 Module 4 Assessment

### Knowledge Check Quiz

**Question 1**: What's the main advantage of event-driven architecture over synchronous request-response?
- a) It's always faster
- b) It decouples services and improves resilience ✓  
- c) It uses less memory
- d) It's easier to debug

**Question 2**: When should you use a custom CDK resource?
- a) Never, AWS provides everything you need
- b) When you need to integrate with external services or APIs ✓
- c) Only for complex applications
- d) When you want to show off your Lambda skills

**Question 3**: What's the purpose of a circuit breaker pattern?
- a) To save electricity
- b) To prevent cascading failures when external services are down ✓
- c) To make systems run faster
- d) To reduce costs

### Practical Assessment: The Ultimate Event-Driven System

**Capstone Project**: Build a comprehensive event-driven e-commerce platform that doesn't fall apart at the first sign of trouble.

**Requirements**:

Your system must handle the complete order lifecycle:
1. **Order Placement** via API Gateway → EventBridge
2. **Inventory Check** with circuit breaker protection
3. **Payment Processing** with retry logic and compensation
4. **Shipping Coordination** with external service integration
5. **Customer Notifications** via multiple channels
6. **Analytics Pipeline** for business intelligence

**Architecture Requirements**:
```
API Gateway → Lambda → EventBridge → Multiple Processing Flows
     ↓
├── Order Validation Queue → Lambda → DynamoDB
├── Inventory Queue → Lambda (Circuit Breaker) → External Inventory API
├── Payment Queue → Lambda (Retry Logic) → External Payment API  
├── Shipping Queue → Lambda (Custom Resource) → External Shipping API
├── Notification Queue → Lambda → SNS/SES
└── Analytics Stream → Kinesis → S3 Data Lake
```

**Advanced Features Required**:
- **Saga Pattern** for order orchestration with compensation
- **Circuit Breakers** for external service protection
- **Dead Letter Queues** for failed message handling
- **Custom Resources** for third-party service integration
- **Real-time Analytics** with Kinesis and OpenSearch
- **Cost Optimization** with intelligent data lifecycle management

**Real-World Constraints**:
- Handle 1000+ orders per minute during peak times
- External APIs have 30% failure rate during Black Friday
- Data must be retained for 7 years for compliance
- System must recover gracefully from AWS service outages
- Customer notifications must be delivered within 30 seconds

**The Evil Testing Scenarios**:
1. **Payment API goes down** during checkout → System should queue orders and process when service recovers
2. **Inventory service returns inconsistent data** → Circuit breaker should open and provide graceful degradation
3. **Customer places duplicate orders** rapidly → Idempotency should prevent double charging
4. **Shipping service changes API contract** → Custom resource should handle gracefully
5. **Data lake storage costs explode** → Lifecycle policies should optimize automatically

**Success Criteria**:
- ✅ System processes orders end-to-end without manual intervention
- ✅ External service failures don't bring down the entire system  
- ✅ All events are traceable with X-Ray distributed tracing
- ✅ Real-time dashboards show system health and business metrics
- ✅ Cost optimization keeps storage costs under control
- ✅ Recovery procedures work when tested with chaos engineering
- ✅ Code is properly tested with integration and load tests

**💰 Cost Warning**: This beast costs ~$15-25/day while running at full scale. Build it, test it thoroughly with proper load, document everything, then tear it down like you're dismantling a poorly designed IKEA bookshelf!

---

## 🚀 Ready for Module 5?

**Before proceeding, ensure you can:**
- ✅ Design and implement event-driven architectures that don't collapse
- ✅ Orchestrate complex data flows across multiple AWS services
- ✅ Build custom CDK resources when AWS doesn't give you what you need
- ✅ Handle real-world messiness like failures, retries, and external dependencies
- ✅ Create systems that are observable, debuggable, and maintainable

**Next Up**: [Module 5: Production-Grade CDK TypeScript Applications](/learning-plans/cdk-typescript/module-5)

---

## 💡 Reflection Prompts

1. **How does event-driven architecture change your approach to system design compared to traditional synchronous systems?**

2. **What are the trade-offs between eventual consistency and immediate consistency in distributed systems?**

3. **When would you choose custom resources over trying to force AWS services to do something they weren't designed for?**

4. **How do you balance system resilience with complexity when dealing with external dependencies?**

---

*Congratulations! You've mastered the dark arts of event-driven architecture and data orchestration. Your systems now communicate like a well-oiled machine rather than a group of toddlers trying to organize a birthday party. Time to make it all production-ready! 🎭*