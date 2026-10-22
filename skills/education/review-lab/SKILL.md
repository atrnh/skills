---
name: review-lab
description: >
  Reviews lab content drafts from subject matter experts and provides structured editorial
  feedback. Use this skill whenever the user wants to review, critique, edit, or get feedback
  on a lab, exercise, or hands-on activity — even if they just say "review this", "check this
  draft", "give me feedback on this lab", or share a document and ask what needs to change.
  Trigger when the user shares a .docx, .pdf, .md, .rst, or .txt file and asks for editorial
  review, or when they paste lab content directly. Do NOT trigger for creating content from
  scratch — this skill is for reviewing existing drafts.
---

# Review Lab

Review a lab draft against the lab style guide and produce structured editorial feedback.

## Step 1: Read the source material

Determine where the content is coming from and extract the text:

- **Word document (.docx)** — convert with `pandoc` to read the content: `pandoc input.docx -o /tmp/lab-review-input.md` then read `/tmp/lab-review-input.md`
- **PDF file** — use the `Read` tool on the file path
- **Markdown or RST file** — use the `Read` tool on the file path
- **Plain text** pasted into the conversation — use it directly
- **URL or web page** — use the `WebFetch` tool to retrieve the page content

If no source material has been provided, ask for it before proceeding.

## Step 2: Read the style guide

Read the style guide at `${CLAUDE_SKILL_DIR}/lab-style-guide.md`. This contains the editorial conventions to review against.

## Step 3: Analyze the draft

Review the draft against every section of the style guide. For each issue found, note:

- **What** — the specific text, section, or pattern that has the issue
- **Why** — which style guide convention it violates and why it matters
- **Suggestion** — a concrete fix (rewritten text, restructured section, added warning, etc.)

Organize issues into these categories:

1. **Audience & Voice** — third-person language, instructor-facing metadata, tone issues
2. **Structure & Organization** — heading style, missing sections, content ordering
3. **Safety & Warnings** — missing cautions, inadequate billing/resource warnings
4. **UI References & Navigation** — vague references, missing icon descriptions, missing expected outcomes
5. **Content Accuracy** — incorrect terminology, mismatched titles, inaccurate navigation paths
6. **Formatting & Consistency** — capitalization, list style, redundant instructions
7. **Submission & Deliverables** — unclear submission instructions, missing format requirements
8. **Images & Screenshots** — missing captions, auto-generated alt text, uncropped screenshots

Skip categories where no issues are found — don't pad the report with "no issues" entries.

## Step 4: Produce the feedback

The output format depends on the input format:

### If the input is a .docx file

Add comments directly to the .docx file using the docx editing workflow (unpack, add comments, repack). Each comment should contain the issue description and suggested fix.

Additionally, produce a **summary report** as a markdown file that lists all issues by category with an overall assessment. Save this alongside the annotated .docx.

**Steps:**

1. Unpack the original .docx:
   ```bash
   python scripts/office/unpack.py input.docx /tmp/lab-review-unpacked/
   ```

2. Read `/tmp/lab-review-unpacked/word/document.xml` to locate the text spans where issues occur.

3. For each issue, add a comment using `comment.py`:
   ```bash
   python scripts/comment.py /tmp/lab-review-unpacked/ <id> "Comment text"
   ```
   Then add comment range markers in `document.xml` around the relevant text.

4. Repack:
   ```bash
   python scripts/office/pack.py /tmp/lab-review-unpacked/ output.docx --original input.docx
   ```

5. Write the summary report as a markdown file.

6. Tell the user the paths to both output files.

### If the input is any other format

Produce a **markdown report** with this structure:

```markdown
# Lab Review: [Draft Title]

## Summary

[2-3 sentence overall assessment: what's working well and the most important areas to address]

## Issues

### [Category Name]

#### [Issue title]

**Location:** [section name or quote from the draft]

**Issue:** [description of the problem and which convention it violates]

**Suggestion:**
> [concrete rewritten text or specific action to take]

---

[repeat for each issue]

## Checklist

- [ ] [one-line summary of each issue, suitable for tracking]
```

Save the report to a file and tell the user the path.

## Step 5: Present results

After producing the feedback:

1. State how many issues were found and which categories they fall into
2. Highlight the top 2-3 most impactful issues — the ones that would most improve the draft if addressed
3. Note what the draft does well — always include at least one positive observation
4. Tell the user the output file path(s)
