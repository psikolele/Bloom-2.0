# Bloom 2.0 Development Task List

-[x] Research & Preparation
    -[x] Locate the "GitHub connection script" mentioned by the user.
    -[x] Identify paths/repositories for "Caption Flow", "Social Media Client", and "Store Brand Profile" (Web app Brand Profile).
    -[x] Create `implementation_plan.md` for the new Bloom 2.0 architecture.

-[x] Scaffold Bloom 2.0
    -[x] Initialize a new Web Application (Next.js or Vite) in `c:\Users\psiko\Desktop\Antigravity\Bloom 2.0`.
    -[x] Set up the basic directory structure.

-[x] Implementation
    -[x] Implement the "Collector/Dispatcher" Dashboard.
    -[x] Integrate "Caption Flow".
    -[x] Integrate "Social Media Client".
    -[x] Integrate "Web app Brand Profile".
    -[x] Style the application (Premium/Vibrant design).

-[x] Verify navigation between the integrated apps (Router setup).
    -[x] Verify GitHub connection/integration if applicable to the app's logic (Deployment Script Created).
    -[x] Create `walkthrough.md`.

-[x] OpenRouter Migration & N8N V.2
    -[x] **Research**: Best OpenRouter models for Web Scraping/Analysis (Brainstorming).
    -[x] **Backup**: Export all current Bloom workflows to `Bloom 2.0/backup_workflows`.
    -[x] **Duplicate**: Re-import workflows as `_V.2`.
    -[x] **Update**: Fetch new Webhook URLs for V.2 workflows and update App config.
    -[x] **Refactor**: Switch `BrandProfile` from Google GenAI to OpenRouter.

    -[x] **Audit**: Check for missing workflows.

-[x] UI Refinement
    -[x] **Assets**: Locate and migrate Logo/Loader from Bloom V1.
    -[x] **Header**: Move 'Back to Hub' to right, remove legacy 'Back to Bloom'.
    -[x] **Integration**: Apply standardized header/loader to CaptionFlow, SocialClient, BrandProfile.
    -[x] **Fix**: Resolve duplicate menu in CaptionFlow.
    -[x] **Polish**: Standardize Loaders and Transitions (Fluid animation, no masks).
    -[x] **Fix**: Brand Profile Jina AI protocol error (400).
    -[x] **UI**: Loader updated to show only icon with glow effect.

## 📝 Notes
- **Language Preferences**: Always respond in **Italian** and explain bug fixes.
