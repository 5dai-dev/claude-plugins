# Eval: Create a Skill

## Goal

Create a new skill from the Skills page, then verify it appears in the skills list.

## Context files to read

- SKILL.md (for domain, timing, tools reference)
- pages/SKILLS.md (for skill recipes and UI elements)

## Preconditions

- Logged in (auth token in browser)
- Skills feature is enabled for the user's organization

## Steps

1. Follow "Navigate to Skills List" recipe from SKILLS.md
2. Take snapshot — verify "Create Skill" button visible

3. Follow "Create a skill" recipe:
   - Click "Create Skill"
   - Wait(fast)
   - Type "Eval Test Skill" in the name input
   - Click the Description textarea
   - Type "This skill was created by the fe-nav eval suite"
   - Click the Instructions textarea
   - Type "Step 1: Summarize the document\nStep 2: Extract key dates"
   - Click "Create Skill" (submit button in dialog footer)
   - Wait(slow)

4. Take screenshot — verify redirected to skill detail page
5. Take snapshot — verify skill name "Eval Test Skill" is visible

6. Navigate back to skills list (click back arrow or use sidebar)
7. Follow "Search" recipe — search for "Eval Test Skill"
8. Take snapshot — verify the skill appears in search results

## Cleanup

After the eval, delete the created skill:
1. Click into "Eval Test Skill"
2. Follow "Delete a skill" recipe

## Pass criteria

- Create Skill dialog opened successfully
- Skill was created (redirected to detail page with correct name)
- Skill appears in the skills list when searched
- (Cleanup) Skill was deleted successfully
