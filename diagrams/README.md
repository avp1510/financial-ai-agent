# Architecture Diagrams

This directory contains PlantUML diagrams documenting the Financial AI Agent architecture.

## Available Diagrams

### 1. Component Architecture
- **File**: `component_diagrams.puml`
- **Description**: DDD layered architecture showing domain, application, and infrastructure layers
- **Formats**: PNG, SVG

### 2. Query Processing Sequence
- **File**: `sequence_diagrams.puml`
- **Description**: Request flow through the multi-agent system
- **Formats**: PNG, SVG

### 3. Multi-Agent System Sequence
- **File**: `multi_agent_sequence.puml`
- **Description**: Detailed agent orchestration and communication flow
- **Formats**: PNG, SVG

### 4. Deployment Architecture
- **File**: `deployment_diagram.puml`
- **Description**: System deployment and infrastructure organization
- **Formats**: PNG, SVG

### 5. Package Structure
- **File**: `package_diagram.puml`
- **Description**: Python module organization and dependencies
- **Formats**: PNG, SVG

### 6. Fault Tolerance Overview
- **File**: `fault_tolerance_overview.puml`
- **Description**: Fault tolerance patterns and resilience architecture
- **Formats**: PNG, SVG

### 7. Fault Tolerance Sequence
- **File**: `fault_tolerance_sequence.puml`
- **Description**: Error handling and recovery flow
- **Formats**: PNG, SVG

## Viewing Options

### 1. Local Viewing
- **PNG files**: Open directly in any image viewer
- **SVG files**: Open in web browsers or vector graphics editors

### 2. Online PlantUML Viewer
Visit [PlantUML Online Server](https://www.plantuml.com/plantuml/) and paste the .puml file contents

### 3. IDE Integration
Many IDEs have PlantUML plugins:
- VS Code: PlantUML extension
- IntelliJ: PlantUML Integration plugin
- Cursor: Built-in PlantUML support

## Regenerating Diagrams

To regenerate all diagrams:

```bash
cd diagrams
plantuml *.puml          # Generate PNG files
plantuml -tsvg *.puml    # Generate SVG files
```

## Tools Required

- **Graphviz**: `brew install graphviz` (provides `dot` command)
- **PlantUML**: `brew install plantuml`

## Troubleshooting

If you get errors like "Cannot run program '/opt/local/bin/dot'":

1. Install Graphviz: `brew install graphviz`
2. Install PlantUML: `brew install plantuml`
3. Verify installation: `which dot && which plantuml`

## Architecture Overview

The diagrams document:

- **Domain Driven Design** implementation with clean boundaries
- **Fault tolerance** patterns (circuit breakers, retries, fallbacks)
- **Layered architecture** (UI, Application, Domain, Infrastructure)
- **Multi-agent orchestration** for financial data analysis
- **Test-driven development** approach with comprehensive testing
