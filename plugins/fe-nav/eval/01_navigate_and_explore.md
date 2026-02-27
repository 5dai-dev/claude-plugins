# Eval: Navigate and Explore Major Pages

## Goal

Visit 4 major pages (Home, Threads, Skills, Data Rooms), take screenshots at each, and verify the layout matches what the skill files describe.

## Context files to read

- SKILL.md (for domain, timing, tools reference, site map)
- pages/HOME.md
- pages/THREADS.md
- pages/SKILLS.md
- pages/DATA_ROOMS.md
- pages/SIDEBAR.md

## Preconditions

- Logged in (auth token in browser)
- Chrome MCP connected

## Steps

1. Follow "Navigate to Home" recipe from HOME.md
2. Take snapshot — verify welcome heading, search input, tool cards are present
3. Take screenshot

4. Follow "Navigate via sidebar" recipe from SIDEBAR.md — click "Threads"
5. Wait(slow)
6. Take snapshot — verify "Threads" heading, "All" / "Unread" tabs visible
7. Take screenshot

8. Follow "Navigate via sidebar" recipe — click "Skills"
9. Wait(slow)
10. Take snapshot — verify "Skills" heading, "Create Skill" button, search input
11. Take screenshot

12. Follow "Navigate via sidebar" recipe — click a data room from the sidebar
13. Wait(slow)
14. Take snapshot — verify file/folder table is visible
15. Take screenshot

## Pass criteria

- All 4 pages loaded successfully (no error screens)
- Snapshots confirm key elements described in the skill files (headings, buttons, inputs)
- Screenshots show recognizable page layouts
- Navigation via sidebar worked for all transitions
