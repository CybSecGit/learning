---
id: plan-3-api-security
title: "Plan 3: Go + IDOR/BOLA API Security Buster"
sidebar_label: "🛡️ Plan 3: API Security"
description: "Learn Go while building an automated IDOR/BOLA vulnerability scanner for OpenAPI specifications"
keywords: [golang, security, api testing, idor, bola, openapi, bug bounty]
---

# Plan 3: Go + IDOR/BOLA API Security Buster
### *Building the Bug Hunter's Best Friend (The Ethical Way)*

> "Give a person a fish, they eat for a day. Teach them to automatically find IDOR vulnerabilities in APIs, and they'll never go hungry on bug bounty platforms again." - Ancient Bug Hunter Proverb

**The Big Idea**: You'll learn Go by building a comprehensive API security testing platform that can take an OpenAPI specification and automatically discover IDOR (Insecure Direct Object Reference) and BOLA (Broken Object Level Authorization) vulnerabilities. Think of it as your personal bug bounty assistant that finds the easy money while you focus on the complex stuff.

**Why This Works**:
- API security is where the money is in bug bounties
- IDOR/BOLA bugs are common but tedious to find manually
- Go's HTTP client libraries are perfect for API testing
- You'll learn real-world vulnerability patterns that actually pay
- By the end, you'll have a tool that could literally pay for itself

**What You'll Build**: A complete API security testing suite with:
- OpenAPI specification parser and analyzer
- Intelligent test case generation
- Multi-user authentication simulation
- Automated IDOR/BOLA detection
- Professional vulnerability reporting
- Integration with bug bounty workflows
- Vulnerable test APIs for practice

## Phase 1: OpenAPI Parser and Go Fundamentals (Week 1-2)
*"Reading API Docs So You Don't Have To"*

**Learning Goals**: Go structs, JSON parsing, HTTP clients, error handling, file I/O, testing
**Security Concepts**: API specification analysis, endpoint enumeration, parameter identification

**What You'll Build**: A robust OpenAPI 3.0 specification parser that understands endpoints, parameters, authentication, and data models.

### Day 1-3: The Foundation

```go
// File: cmd/api-buster/main.go
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "os"
    
    "github.com/yourusername/api-buster/internal/parser"
    "github.com/yourusername/api-buster/internal/config"
)

func main() {
    if len(os.Args) < 2 {
        log.Fatal("Usage: api-buster <openapi-spec.json>")
    }
    
    cfg := config.NewConfig()
    specFile := os.Args[1]
    
    spec, err := parser.ParseOpenAPISpec(specFile)
    if err != nil {
        log.Fatalf("Failed to parse spec: %v", err)
    }
    
    fmt.Printf("Successfully parsed API: %s\n", spec.Info.Title)
    fmt.Printf("Found %d endpoints\n", len(spec.GetEndpoints()))
}
```

```go
// File: internal/parser/openapi.go
package parser

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "strings"
)

// OpenAPISpec represents the root of an OpenAPI 3.0 specification
type OpenAPISpec struct {
    OpenAPI    string                 `json:"openapi"`
    Info       Info                   `json:"info"`
    Servers    []Server              `json:"servers"`
    Paths      map[string]PathItem   `json:"paths"`
    Components Components            `json:"components"`
    Security   []SecurityRequirement `json:"security,omitempty"`
}

type Info struct {
    Title       string `json:"title"`
    Description string `json:"description,omitempty"`
    Version     string `json:"version"`
}

type Server struct {
    URL         string            `json:"url"`
    Description string            `json:"description,omitempty"`
    Variables   map[string]string `json:"variables,omitempty"`
}

type PathItem struct {
    Get    *Operation `json:"get,omitempty"`
    Post   *Operation `json:"post,omitempty"`
    Put    *Operation `json:"put,omitempty"`
    Delete *Operation `json:"delete,omitempty"`
    Patch  *Operation `json:"patch,omitempty"`
}

type Operation struct {
    OperationID string              `json:"operationId,omitempty"`
    Summary     string              `json:"summary,omitempty"`
    Description string              `json:"description,omitempty"`
    Parameters  []Parameter         `json:"parameters,omitempty"`
    RequestBody *RequestBody        `json:"requestBody,omitempty"`
    Responses   map[string]Response `json:"responses"`
    Security    []SecurityRequirement `json:"security,omitempty"`
    Tags        []string            `json:"tags,omitempty"`
}

type Parameter struct {
    Name        string      `json:"name"`
    In          string      `json:"in"` // "query", "header", "path", "cookie"
    Description string      `json:"description,omitempty"`
    Required    bool        `json:"required,omitempty"`
    Schema      *Schema     `json:"schema,omitempty"`
    Example     interface{} `json:"example,omitempty"`
}

type RequestBody struct {
    Description string               `json:"description,omitempty"`
    Content     map[string]MediaType `json:"content"`
    Required    bool                 `json:"required,omitempty"`
}

type MediaType struct {
    Schema   *Schema     `json:"schema,omitempty"`
    Example  interface{} `json:"example,omitempty"`
    Examples map[string]Example `json:"examples,omitempty"`
}

type Schema struct {
    Type        string            `json:"type,omitempty"`
    Format      string            `json:"format,omitempty"`
    Properties  map[string]Schema `json:"properties,omitempty"`
    Items       *Schema           `json:"items,omitempty"`
    Required    []string          `json:"required,omitempty"`
    Example     interface{}       `json:"example,omitempty"`
    Ref         string            `json:"$ref,omitempty"`
}

type Response struct {
    Description string               `json:"description"`
    Content     map[string]MediaType `json:"content,omitempty"`
}

type Components struct {
    Schemas         map[string]Schema         `json:"schemas,omitempty"`
    SecuritySchemes map[string]SecurityScheme `json:"securitySchemes,omitempty"`
}

type SecurityScheme struct {
    Type         string `json:"type"`
    Scheme       string `json:"scheme,omitempty"`
    BearerFormat string `json:"bearerFormat,omitempty"`
    In           string `json:"in,omitempty"`
    Name         string `json:"name,omitempty"`
}

type SecurityRequirement map[string][]string

type Example struct {
    Summary     string      `json:"summary,omitempty"`
    Description string      `json:"description,omitempty"`
    Value       interface{} `json:"value,omitempty"`
}

// Endpoint represents a parsed API endpoint with all its details
type Endpoint struct {
    Method      string
    Path        string
    Operation   *Operation
    Parameters  []Parameter
    HasPathParams bool
    PathParams    []string
    SecurityReqs []SecurityRequirement
}

// ParseOpenAPISpec reads and parses an OpenAPI specification file
func ParseOpenAPISpec(filename string) (*OpenAPISpec, error) {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        return nil, fmt.Errorf("failed to read spec file: %w", err)
    }
    
    var spec OpenAPISpec
    if err := json.Unmarshal(data, &spec); err != nil {
        return nil, fmt.Errorf("failed to parse JSON: %w", err)
    }
    
    // Validate that this is actually OpenAPI 3.x
    if !strings.HasPrefix(spec.OpenAPI, "3.") {
        return nil, fmt.Errorf("unsupported OpenAPI version: %s (only 3.x supported)", spec.OpenAPI)
    }
    
    return &spec, nil
}

// GetEndpoints extracts all endpoints from the OpenAPI spec
func (spec *OpenAPISpec) GetEndpoints() []Endpoint {
    var endpoints []Endpoint
    
    for path, pathItem := range spec.Paths {
        methods := map[string]*Operation{
            "GET":    pathItem.Get,
            "POST":   pathItem.Post,
            "PUT":    pathItem.Put,
            "DELETE": pathItem.Delete,
            "PATCH":  pathItem.Patch,
        }
        
        for method, operation := range methods {
            if operation == nil {
                continue
            }
            
            endpoint := Endpoint{
                Method:    method,
                Path:      path,
                Operation: operation,
                Parameters: operation.Parameters,
                SecurityReqs: operation.Security,
            }
            
            // If no operation-level security, use global security
            if len(endpoint.SecurityReqs) == 0 {
                endpoint.SecurityReqs = spec.Security
            }
            
            // Extract path parameters
            endpoint.PathParams = spec.extractPathParams(path)
            endpoint.HasPathParams = len(endpoint.PathParams) > 0
            
            endpoints = append(endpoints, endpoint)
        }
    }
    
    return endpoints
}

// extractPathParams finds all path parameters in a path string
func (spec *OpenAPISpec) extractPathParams(path string) []string {
    var params []string
    parts := strings.Split(path, "/")
    
    for _, part := range parts {
        if strings.HasPrefix(part, "{") && strings.HasSuffix(part, "}") {
            param := strings.Trim(part, "{}")
            params = append(params, param)
        }
    }
    
    return params
}

// GetPotentialIDOREndpoints identifies endpoints that might be vulnerable to IDOR
func (spec *OpenAPISpec) GetPotentialIDOREndpoints() []Endpoint {
    endpoints := spec.GetEndpoints()
    var candidates []Endpoint
    
    for _, endpoint := range endpoints {
        // Look for endpoints with path parameters (common IDOR pattern)
        if endpoint.HasPathParams {
            // Check if any path params look like IDs
            for _, param := range endpoint.PathParams {
                if spec.looksLikeID(param) {
                    candidates = append(candidates, endpoint)
                    break
                }
            }
        }
        
        // Look for query parameters that might be IDs
        for _, param := range endpoint.Parameters {
            if param.In == "query" && spec.looksLikeID(param.Name) {
                candidates = append(candidates, endpoint)
                break
            }
        }
    }
    
    return candidates
}

// looksLikeID determines if a parameter name suggests it contains an ID
func (spec *OpenAPISpec) looksLikeID(paramName string) bool {
    idPatterns := []string{
        "id", "ID", "Id",
        "userId", "user_id", "userID",
        "accountId", "account_id", "accountID",
        "orderId", "order_id", "orderID",
        "documentId", "document_id", "documentID",
        "fileId", "file_id", "fileID",
        "resourceId", "resource_id", "resourceID",
    }
    
    paramLower := strings.ToLower(paramName)
    
    for _, pattern := range idPatterns {
        if strings.Contains(paramLower, strings.ToLower(pattern)) {
            return true
        }
    }
    
    return false
}
```

### Day 4-7: Vulnerable Test APIs

Let's create some intentionally vulnerable OpenAPI specs for testing:

```json
# File: testdata/vulnerable-banking-api.json
{
  "openapi": "3.0.3",
  "info": {
    "title": "Vulnerable Banking API",
    "description": "A purposely vulnerable banking API for IDOR/BOLA testing",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://vulnerable-bank.example.com/api/v1",
      "description": "Production server (obviously fake)"
    }
  ],
  "security": [
    {
      "bearerAuth": []
    }
  ],
  "paths": {
    "/accounts/{accountId}": {
      "get": {
        "summary": "Get account details",
        "description": "Retrieve details for a specific account - VULNERABLE TO IDOR!",
        "parameters": [
          {
            "name": "accountId",
            "in": "path",
            "required": true,
            "schema": {
              "type": "integer",
              "example": 12345
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Account details",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Account"
                }
              }
            }
          }
        }
      }
    },
    "/accounts/{accountId}/transactions": {
      "get": {
        "summary": "Get account transactions",
        "description": "List transactions for an account - VULNERABLE TO IDOR!",
        "parameters": [
          {
            "name": "accountId",
            "in": "path",
            "required": true,
            "schema": {
              "type": "integer"
            }
          },
          {
            "name": "limit",
            "in": "query",
            "schema": {
              "type": "integer",
              "default": 50
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Transaction list",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Transaction"
                  }
                }
              }
            }
          }
        }
      }
    },
    "/users/{userId}/profile": {
      "get": {
        "summary": "Get user profile",
        "description": "Get user profile information - VULNERABLE TO IDOR!",
        "parameters": [
          {
            "name": "userId",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "example": "user123"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "User profile",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UserProfile"
                }
              }
            }
          }
        }
      },
      "put": {
        "summary": "Update user profile",
        "description": "Update user profile - VULNERABLE TO BOLA!",
        "parameters": [
          {
            "name": "userId",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/UserProfileUpdate"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Profile updated"
          }
        }
      }
    },
    "/documents": {
      "get": {
        "summary": "List user documents",
        "description": "List documents with optional userId filter - VULNERABLE TO IDOR!",
        "parameters": [
          {
            "name": "userId",
            "in": "query",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Document list",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Document"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Account": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer"
          },
          "accountNumber": {
            "type": "string"
          },
          "balance": {
            "type": "number"
          },
          "userId": {
            "type": "string"
          }
        }
      },
      "Transaction": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "amount": {
            "type": "number"
          },
          "description": {
            "type": "string"
          },
          "timestamp": {
            "type": "string",
            "format": "date-time"
          }
        }
      },
      "UserProfile": {
        "type": "object",
        "properties": {
          "userId": {
            "type": "string"
          },
          "email": {
            "type": "string"
          },
          "firstName": {
            "type": "string"
          },
          "lastName": {
            "type": "string"
          },
          "ssn": {
            "type": "string",
            "description": "Social Security Number - very sensitive!"
          }
        }
      },
      "UserProfileUpdate": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string"
          },
          "firstName": {
            "type": "string"
          },
          "lastName": {
            "type": "string"
          }
        }
      },
      "Document": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "userId": {
            "type": "string"
          },
          "sensitive": {
            "type": "boolean"
          }
        }
      }
    },
    "securitySchemes": {
      "bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
      }
    }
  }
}
```

### Testing Your Parser

```go
// File: internal/parser/parser_test.go
package parser

import (
    "testing"
)

func TestParseOpenAPISpec(t *testing.T) {
    spec, err := ParseOpenAPISpec("../../testdata/vulnerable-banking-api.json")
    if err != nil {
        t.Fatalf("Failed to parse test spec: %v", err)
    }
    
    if spec.Info.Title != "Vulnerable Banking API" {
        t.Errorf("Expected title 'Vulnerable Banking API', got '%s'", spec.Info.Title)
    }
    
    endpoints := spec.GetEndpoints()
    if len(endpoints) == 0 {
        t.Error("Expected to find endpoints, got none")
    }
    
    // Test IDOR endpoint detection
    idorEndpoints := spec.GetPotentialIDOREndpoints()
    if len(idorEndpoints) == 0 {
        t.Error("Expected to find potential IDOR endpoints, got none")
    }
    
    t.Logf("Found %d total endpoints, %d potential IDOR endpoints", 
           len(endpoints), len(idorEndpoints))
}

func TestIDDetection(t *testing.T) {
    spec := &OpenAPISpec{}
    
    testCases := []struct {
        param    string
        expected bool
    }{
        {"userId", true},
        {"accountId", true},
        {"id", true},
        {"name", false},
        {"email", false},
        {"user_id", true},
        {"documentID", true},
    }
    
    for _, tc := range testCases {
        result := spec.looksLikeID(tc.param)
        if result != tc.expected {
            t.Errorf("looksLikeID('%s'): expected %v, got %v", 
                     tc.param, tc.expected, result)
        }
    }
}
```

**Phase 1 Validation Checklist**:
- [ ] Successfully parse OpenAPI 3.0 specifications
- [ ] Extract all endpoints with methods and parameters
- [ ] Identify potential IDOR-vulnerable endpoints
- [ ] Pass all unit tests
- [ ] Handle malformed JSON gracefully
- [ ] Support both path and query parameter ID detection

**🎯 What You've Learned**:
- Go struct tags and JSON marshaling/unmarshaling
- Error handling with wrapped errors
- File I/O and data validation
- Regular expressions and string manipulation
- Test-driven development in Go
- API specification parsing and analysis

**🔐 Security Concepts Mastered**:
- OpenAPI specification structure and security implications
- IDOR vulnerability patterns and identification
- API endpoint analysis and attack surface mapping
- Parameter injection points and data flow analysis

**Next**: Phase 2 will teach you HTTP client programming and authentication simulation while building the actual testing engine!