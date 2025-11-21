# TreeDocs

TreeDocs is a Go-based GUI text editor for creating and managing multiple documents in Markdown, plain text, and other text formats. It organizes documents into workspaces and features a live Markdown previewer.

## Features
- Multi-document editing (Markdown, text, etc.)
- Workspace organization
- Live Markdown preview
- Extensible Go codebase using Fyne GUI

## Getting Started

1. Install Go 1.21 or newer.
2. Run `go mod tidy` to install dependencies.
3. Run the app:
   ```sh
   go run ./cmd/treedocs.go
   ```

## Project Structure
- `cmd/treedocs.go` — Application entry point
- `internal/gui/` — GUI logic (Fyne)
- `internal/documents/` — Document and workspace management
- `internal/preview/` — Markdown preview logic

## Dependencies
- [Fyne](https://fyne.io/) for GUI
- [gomarkdown/markdown](https://github.com/gomarkdown/markdown) for Markdown rendering

---
This is an early scaffold. More features and improvements coming soon.
