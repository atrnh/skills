# Lab Style Guide

Editorial conventions for lab content. This guide is used by the `review-lab` skill to evaluate drafts from subject matter experts and provide structured feedback.

## Audience and voice

- **Address the learner directly** — use "you" and "your", not "participants", "students", or "the user". Labs are instructions the learner follows, not descriptions of what a third party will do.
- **Use a conversational but professional tone** — avoid stiff or overly formal phrasing. Prefer "you'll" over "you will" where it reads naturally.
- **Don't assume prior knowledge unless stated** — if a lab is introductory, explain foundational concepts and commands (e.g., what `ls` does, what `cat` does). Match the level of explanation to the stated audience.
- **Remove instructor-facing language** — drafts often contain notes like "estimated time", "learning objectives", or "upon completion, participants will be able to..." that read as lesson-plan metadata rather than learner-facing content. These should be reworked into learner-oriented framing or removed.

## Structure and organization

- **Use task-oriented section headings** — headings should describe what the learner will do, not enumerate steps. Prefer "Switch AWS Regions" over "Step 3: Identify and Switch AWS Regions". Drop step numbers from headings entirely.
- **Separate "further study" into its own page** — optional/bonus content belongs in a dedicated `further-study.rst`, not inline at the end of the main lab.
- **Include a "Getting Started" section** — at the top of every lab, include setup instructions (e.g., tools to have open, files to download, accounts to create). Don't assume the learner knows what to prepare.
- **Include a "What you'll be doing" subsection** — state what the learner will be able to do after completing the lab. Frame these as outcomes, not academic "learning objectives". Use natural phrasing like "After this lab, you'll be able to:" followed by a bullet list.
- **End with a "Finished?" section** — summarize what the learner should now be comfortable with, point to further study, and give submission instructions.
- **Use a "Reflection" section for open-ended questions** — if the lab asks the learner to write responses, group these in a clearly labeled reflection section with instructions on how to submit.

## Safety and warnings

- **Flag account/billing requirements early** — if setup involves a credit card, payment method, or anything that could alarm learners, call it out explicitly with a reassuring note (e.g., "Don't worry — you will not enable any paid services at this time").
- **Add caution notices before exploratory sections** — when learners are browsing dashboards or services, remind them not to create, modify, or delete resources. This is especially important for cloud platform labs.
- **Use appropriate admonition levels** — match the severity of the warning:
  - `important` — things the learner must know before proceeding (e.g., credit card required)
  - `caution` — things the learner should avoid doing (e.g., don't create resources)
  - `error` — troubleshooting steps for common problems (e.g., "If you're unable to switch regions...")
  - `note` — supplementary context that aids understanding but isn't critical

## UI references and navigation

- **Be specific about UI element locations** — don't just say "click Support". Describe where the element is ("In the toolbar, locate the Support button") and what it looks like ("It looks like a question mark enclosed in a circle").
- **Use consistent terminology for UI elements** — refer to buttons, dropdown menus, panels, and links using their actual labels. When referencing a labeled UI element, use a consistent markup convention (e.g., `:guilabel:` in RST).
- **Describe visual appearance of icons** — learners may not recognize icons by name alone. Include a brief description of what the icon looks like in addition to its label.
- **Describe the expected result of each action** — after "Click on the Services button", tell the learner what they should see ("A panel should appear below the button, showing..."). This confirms they did the right thing.

## Content accuracy

- **Verify service names and navigation paths match the actual platform** — drafts often use approximate names. Check that service names, menu labels, and navigation paths reflect the current UI. For example, the IAM dashboard navigation panel groups resources under "Access Management" — don't just list "Users, Roles, Policies" if that doesn't match the actual grouping.
- **Use correct terminology** — prefer official/canonical names for services and features. Use "AWS Management Console" (not "AWS Console"), "Region Selector" (not "region dropdown"), etc.
- **Check that titles accurately describe the content** — if a section is about creating a file and observing it disappear, the title should reflect that ("The Disappearing File" not "The Disappearing Computer").

## Formatting and consistency

- **Lowercase service categories in running text** — don't capitalize common nouns like "services" or "service categories" mid-sentence unless they are proper names or UI labels. "Browse other service categories" not "Browse other Service categories".
- **Consistent list formatting** — use numbered lists for sequential steps and bullet lists for non-sequential items. Don't mix the two within a single procedure.
- **Don't front-load step numbers into headings** — "AWS Account Setup" not "Step 1: AWS Account Setup".
- **Avoid redundant instructions** — if a concept was explained earlier (e.g., how to find services), reference it rather than re-explaining. "Using one of the methods above, search for..."

## Submission and deliverables

- **Be explicit about deliverable format** — if the learner must submit a PDF, say so and remind them to ensure their software can export to PDF.
- **Tell learners to prepare their submission tool early** — "Before you continue, open the word processing software you'll use to create the report."
- **For reflection questions, tell learners to copy-paste** — rather than having learners manually type out questions, instruct them to copy and paste from the lab into their report document.

## Images and screenshots

- **Every screenshot must have a descriptive caption** — never use auto-generated alt text like "A screenshot of a computer AI-generated content may be incorrect."
- **Screenshots should be annotated or cropped to highlight the relevant area** — don't include full-screen captures when only a toolbar or menu is relevant.
- **Provide a figure description** — briefly explain what the screenshot shows and why it's there (e.g., "A portion of the AWS Management Console toolbar, with the region selector highlighted").

## Common SME draft issues

These are frequently observed patterns in drafts that should be flagged during review:

1. **Third-person voice** — "participants will..." or "students should..." instead of direct address
2. **Step-numbered headings** — "Step 1:", "Step 2:" prefixed to section titles
3. **Missing safety warnings** — no caution notices before sections where learners explore live dashboards
4. **Assumed knowledge** — referencing commands, tools, or concepts without explanation for the target audience
5. **Vague UI references** — "click the button" without specifying which button, where it is, or what it looks like
6. **Auto-generated screenshot alt text** — "AI-generated content may be incorrect" or generic descriptions
7. **Instructor-facing metadata left in** — estimated times, lesson plan language, facilitator notes
8. **Inconsistent capitalization** — capitalizing common nouns like "Services" or "Dashboard" inconsistently
9. **Missing expected outcomes** — telling learners to do something without describing what they should see as confirmation
10. **Inaccurate titles or labels** — section titles that don't match the actual content or activity
