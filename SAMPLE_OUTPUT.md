# Sample Outputs — Enterprise Knowledge Assistant

**Author:** Vivek Kumar  
**Project:** Project 2 — Enterprise Knowledge Assistant with Advanced RAG  
**Organization:** Oeeggis Corporation (fictional, for academic practice)

This document shows example questions and expected assistant behaviour for evaluators.

---

## Sample Input 1 — Leave policy

**User:** What is the leave policy?

**Expected assistant answer (summary):**
- Describes annual leave, sick leave, and related rules from company documents.
- Grounded only in retrieved policy text.

**Expected sources:**
- `Leave_Policy.pdf`

---

## Sample Input 2 — Sick days

**User:** How many sick days do employees get?

**Expected assistant answer (summary):**
- States the sick leave allowance from the leave policy document.

**Expected sources:**
- `Leave_Policy.pdf`

---

## Sample Input 3 — Follow-up with memory

**Previous context:** User asked about leave policy.

**User:** What about carry-forward?

**Expected assistant answer (summary):**
- Understands the follow-up refers to leave policy.
- Explains carry-forward rules from documents.

**Expected sources:**
- `Leave_Policy.pdf`

---

## Sample Input 4 — IT / VPN policy

**User:** What is the VPN policy?

**Expected assistant answer (summary):**
- Explains VPN usage rules for remote access from IT policy.

**Expected sources:**
- `IT_Policy.txt`

---

## Sample Input 5 — Hallucination guard

**User:** What is the salary for the CEO?

**Expected assistant answer:**
- `I could not find this information in the available documents.`

**Expected sources:**
- None (no unsupported answer invented)

---

## Sample Input 6 — Casual introduction (no document search)

**User:** Hi, my name is Abhishek and I am from Bangalore.

**Expected assistant answer (summary):**
- Brief friendly acknowledgement of name/location.
- Does **not** volunteer WFH or other policy information unless asked.

**Expected sources:**
- None

---

## Sample Input 7 — Benefits

**User:** What health insurance benefits are available?

**Expected assistant answer (summary):**
- Summarises benefits from benefits documentation.

**Expected sources:**
- `Benefits_Documentation.txt`

---

## Sample Input 8 — Travel policy

**User:** What is the travel reimbursement policy?

**Expected assistant answer (summary):**
- Explains travel and expense rules from travel policy.

**Expected sources:**
- `Travel_Policy.txt`

---

## UI behaviour checklist

| Feature | Expected behaviour |
|---------|-------------------|
| Welcome page | Project overview shown first; **Start Conversation** opens chat |
| Chat history | Previous messages remain visible |
| Source citations | Shown below policy answers |
| Clear / Reset | Clears chat and memory |
| Startup preload | Models load once when app opens |
| Error handling | Friendly message if API or runtime fails |

---

## Notes for evaluators

1. Run `python scripts/ingest.py` before first use.
2. Use `start.bat` or `streamlit run app/main.py`.
3. Open `http://localhost:8501` (local deployment only).
4. Click **Start Conversation** on the welcome page before testing chat.
4. Sample documents are in `data/documents/`.
5. Detailed logs are written to `logs/` during each session.
