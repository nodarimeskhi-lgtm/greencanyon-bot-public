# Tesseract 3D Architecture Editor -- Setup Guide

Tesseract is a 3D architecture editor that connects to AI via MCP.
Use this when you need to visualize codebases, design system architectures, or document data flows in 3D.

Website: https://tesseract.infrastellar.dev/

## Setup Steps

### 1. Download Tesseract

Download from https://tesseract.infrastellar.dev/ for your platform (Windows/macOS/Linux).

### 2. MCP Configuration

The MCP config is already set up in `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tesseract": {
      "url": "http://localhost:7440/mcp",
      "type": "http"
    }
  }
}
```

### 3. Launch and Connect

1. Launch Tesseract desktop app
2. Open your project in Tesseract
3. Tesseract starts MCP server on `localhost:7440` automatically
4. Cursor will detect the MCP server from `.cursor/mcp.json`

### 4. Usage

Once connected, ask the AI to:

- "Analyze the src/ directory and build the architecture diagram in Tesseract"
- "Create a system architecture diagram showing the project structure"
- "Map the data flow from frontend to database in Tesseract"
- "Generate a 3D visualization of the microservices architecture"

## Capabilities

- **Code to Diagram**: Point at codebase, auto-generate 3D architecture
- **Diagram to Code**: Design visually, generate implementation code
- **Visual AI Assistant**: Ask questions, see answers highlighted on 3D diagram
- **Data Flow Recording** (Pro): Record, replay, animate data paths

## Pricing

- Free: Unlimited diagrams, basic components, MCP integration
- Pro ($9.90/mo): Data flow recording, detailed 3D models, extended library
- Enterprise: Team collaboration (coming soon)
