# UEFN Remote Control API Availability Check

**Purpose**: Determine if UEFN supports Remote Control API for editor automation (Phase 5 decision)

**Duration**: 5-10 minutes

**Result**: Either proceed with Phase 5 (automation) or skip to Phase 6 (manual workflow)

---

## Background

### Remote Control in UE5

Remote Control API is a well-documented UE5 plugin that:
- Runs HTTP/WebSocket server inside editor (default port: 30010)
- Exposes Blueprint/Python functions and properties via REST API
- Allows external processes to control the editor
- Documented at: https://docs.unrealengine.com/5.3/en-US/remote-control-api-in-unreal-engine/

### Remote Control in UEFN?

**Unknown.** UEFN documentation doesn't explicitly mention Remote Control support.

Since UEFN is a modified UE editor:
- Plugins might be compiled in but undocumented
- Or they might be disabled/removed for Fortnite Creative
- Only way to know: check your UEFN installation

---

## Check Procedure

### Step 1: Check for Remote Control Plugins

1. **Open UEFN Editor**
   - Launch Fortnite
   - Open UEFN from Fortnite launcher
   - Open any project (or create test project)

2. **Open Plugins Window**
   - Menu: `Edit` → `Plugins`
   - Or press `Ctrl+Shift+P` (might not work in UEFN)

3. **Search for Remote Control Plugins**

   In the plugins search box, try each of these:
   - `Remote Control API`
   - `Remote Control Web Interface`
   - `RemoteControl` (no space)
   - `WebControl`

4. **Check Category**

   If search doesn't work, browse by category:
   - Look in `Messaging` category
   - Look in `Virtual Production` category
   - Look in `Developer Tools` category

### Step 1 Results:

**If you find "Remote Control API" plugin:**
- ✅ **FOUND** - Proceed to Step 2
- Note if it's enabled or disabled
- Screenshot the plugin entry

**If NO Remote Control plugins found:**
- ❌ **NOT AVAILABLE** - Skip to Conclusion (no Remote Control in UEFN)
- This means Phase 5 automation is not possible
- Proceed directly to Phase 6 with manual workflow

---

### Step 2: Enable Remote Control Plugin (if found)

1. **Enable the Plugin**
   - Check the checkbox next to `Remote Control API`
   - If prompted, click `Yes` to enable dependencies

2. **Optional: Enable Web Interface**
   - If `Remote Control Web Interface` exists, enable it too
   - This adds a web GUI for debugging (useful but not required)

3. **Restart UEFN**
   - Click `Restart Now` when prompted
   - Wait for UEFN to restart

---

### Step 3: Test Remote Control Server

1. **Open Output Log**
   - Menu: `Window` → `Developer Tools` → `Output Log`
   - Or `Window` → `Output Log`

2. **Start Remote Control Server**

   In the command input at bottom of Output Log, type:
   ```
   WebControl.StartServer
   ```

   Press Enter.

3. **Check Output Log**

   Look for one of these messages:

   **SUCCESS:**
   ```
   LogWebRemoteControl: Display: Started listening on port 30010
   ```

   **FAILURE:**
   ```
   Unknown command: WebControl.StartServer
   ```
   or
   ```
   LogRemoteControl: Error: ...
   ```

4. **If Server Started: Test HTTP Endpoint**

   Open a new terminal (PowerShell or cmd) and run:
   ```powershell
   curl http://localhost:30010/remote/info
   ```

   Or in Python:
   ```python
   import requests
   response = requests.get('http://localhost:30010/remote/info')
   print(response.status_code)
   print(response.json())
   ```

   **Expected response:**
   - HTTP 200 OK
   - JSON with server info (version, capabilities, etc.)

   **If connection refused:**
   - Server isn't actually running
   - Check firewall/antivirus
   - Try different port: `WebControl.StartServer 30011`

---

## Results & Next Steps

### ✅ Result: Remote Control IS Available

**What this means:**
- Phase 5 automation is possible
- MCP can control UEFN editor via HTTP
- Can automate: asset imports, Verse builds, device placement

**Next Steps:**
1. Document HTTP endpoints that work in UEFN
2. Implement Phase 5 MCP tools:
   - `uefn_import_assets()` - trigger asset import
   - `uefn_build_verse()` - trigger Verse compilation
   - `uefn_create_preset()` - create Remote Control presets
3. Test automation workflow
4. Proceed to Phase 6 with automation support

**Report Back:**
```
✅ Remote Control AVAILABLE in UEFN

Plugin Version: [check in Plugins window]
Server Port: 30010
Test Endpoint: http://localhost:30010/remote/info
Response: [paste JSON]

Ready for Phase 5 implementation.
```

---

### ❌ Result: Remote Control NOT Available

**What this means:**
- Phase 5 automation not possible in UEFN
- Asset import, Verse builds remain manual steps
- This is expected - UEFN is locked down for Fortnite Creative

**Next Steps:**
1. Skip Phase 5 entirely
2. Proceed directly to Phase 6: Integration & Testing
3. Use manual workflow documented in EXPORT_WORKFLOW_GUIDE.md
4. Focus on testing export pipeline end-to-end

**Report Back:**
```
❌ Remote Control NOT AVAILABLE in UEFN

Plugins searched: Remote Control API, RemoteControl, WebControl
Found: None
UEFN Version: [check Help → About]

Skipping Phase 5. Proceeding to Phase 6.
```

---

### ⚠️ Result: Plugin Found but Server Won't Start

**What this means:**
- Plugin compiled in but might be disabled for UEFN
- Or requires additional configuration
- Treat as "NOT AVAILABLE" unless we can fix it

**Troubleshooting:**
1. Check plugin dependencies are all enabled
2. Try alternative commands:
   - `RemoteControl.StartServer`
   - Look in `Edit → Project Settings → Plugins → Remote Control` for settings
3. Check UEFN logs for errors:
   - `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\Logs\UnrealEditorFortnite.log`

**If can't resolve in 15 minutes:**
- Treat as "NOT AVAILABLE"
- Skip Phase 5
- Proceed to Phase 6

---

## Additional Checks (Optional)

If Remote Control IS available, test these capabilities:

### Test 1: Execute Console Command

```python
import requests

response = requests.post('http://localhost:30010/remote/batch',
    json={
        "Requests": [{
            "RequestId": 1,
            "URL": "/remote/preset/call",
            "Verb": "PUT",
            "Body": {
                "ObjectPath": "/Script/Engine.Default__KismetSystemLibrary",
                "FunctionName": "PrintString",
                "Parameters": {
                    "InString": "Hello from Remote Control!"
                }
            }
        }]
    }
)

print(response.json())
```

Expected: "Hello from Remote Control!" appears in UEFN Output Log

### Test 2: List Available Presets

```bash
curl http://localhost:30010/remote/presets
```

Expected: JSON array of Remote Control presets (likely empty on first run)

### Test 3: Get Editor Properties

```bash
curl http://localhost:30010/remote/search/assets?Query=*
```

Expected: JSON list of assets in project

---

## Summary Checklist

Run through this checklist and report results:

- [ ] Opened UEFN Plugins window
- [ ] Searched for "Remote Control API"
- [ ] Plugin found: YES / NO
- [ ] If YES: Enabled plugin and restarted
- [ ] Ran `WebControl.StartServer` command
- [ ] Server started: YES / NO
- [ ] If YES: Tested `curl http://localhost:30010/remote/info`
- [ ] HTTP endpoint works: YES / NO

**Final Verdict:** Remote Control in UEFN is: **AVAILABLE** / **NOT AVAILABLE**

---

## What This Means for the Project

### If AVAILABLE:
- Implement Phase 5 (1-2 days)
- Add editor automation MCP tools
- Streamline workflow: export → auto-import → auto-build

### If NOT AVAILABLE:
- Skip Phase 5
- Go straight to Phase 6 (end-to-end testing)
- Manual workflow is well-documented in EXPORT_WORKFLOW_GUIDE.md
- Still have full UE5 → UEFN export pipeline

**Either way, Phase 4 export pipeline works!**

---

*Remote Control Check Guide - UEFN Migration Project*
*Created: November 13, 2025*
