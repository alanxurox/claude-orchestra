# Twitter Engagement Playbook

*Strategy for building presence and engaging with Claude Code community*

---

## Phase 1: Pre-Launch Engagement (Before Posting Thread)

### Target Accounts to Follow & Engage

**Tier 1 - Claude Code Team (Engage carefully, build goodwill first)**
| Handle | Role | Notes |
|--------|------|-------|
| @bcherny | Creator of Claude Code | Viral workflow post. Don't pitch - share value first |
| @anthroploic | Official Anthropic | General announcements |
| @claudeai | Claude official | Product updates |

**Tier 2 - Influencers Who Cover Claude Code**
| Handle | Why | Engagement Strategy |
|--------|-----|---------------------|
| @eduardojld | Wrote about subagent orchestration | Comment on his posts, share related insights |
| @carlvellotti | 55k followers, Claude Code tutorials | Engage with tutorials, offer genuine tips |

**Tier 3 - Developer Tool Builders**
| Handle | Why | Engagement Strategy |
|--------|-----|---------------------|
| Various dev tool creators | Community overlap | Genuine engagement, not promotion |

### Pre-Launch Actions (Do This Week)

1. **Day 1-2:** Follow target accounts, like/retweet their Claude Code content
2. **Day 3-4:** Reply to threads about Claude Code with helpful tips (NOT promotional)
3. **Day 5:** Share a "building in public" post about your project (no link yet)
4. **Day 6-7:** Engage with responses, build small audience before launch

### Example Pre-Launch Tweets

**Building in Public (Day 5):**
```
Working on a side project: session discovery for Claude Code.

Ever close your laptop and forget what you were working on? Sessions are buried in ~/.claude/projects/ with no way to browse them.

Building a simple pip-installable tool to fix this. More soon.
```

**Technical Insight (Day 3):**
```
TIL: Claude Code sessions are stored as JSONL files in ~/.claude/projects/<project-hash>/

Each file contains full conversation history. Great for:
- Analyzing token usage patterns
- Finding that context you lost yesterday
- Understanding how Claude approaches problems
```

---

## Phase 2: Launch Day Twitter Thread

See LAUNCH_READY.md for the full 6-tweet thread.

### Posting Strategy

1. **Time:** Tuesday-Thursday, 9-11 AM EST (developer activity peak)
2. **Format:** Thread, not single tweet
3. **First tweet must hook:** Problem statement + curiosity
4. **Include code snippets:** Devs love seeing actual commands
5. **Tag nobody in the launch thread** (looks desperate)

### Thread Tips

- Use whitespace for readability
- Each tweet should stand alone (will be seen in replies)
- End with clear CTA (GitHub link, pip command)
- Don't use hashtags excessively (looks spammy)

---

## Phase 3: Post-Launch Engagement

### Respond to Every Reply

**Positive feedback:**
```
Thanks! Let me know if you run into any issues - we're actively fixing things this week.
```

**Questions about features:**
```
Good question! Currently [answer]. We're tracking this as a potential addition: [link to issue]
```

**Comparison to competitors:**
```
Valid point - claude-flow is excellent for [use case]. We're focused on [our niche]. Use what fits your workflow!
```

**Bug reports:**
```
Appreciate the report! Can you open an issue on GitHub with your environment details? I'll look at it today.
```

### Quote Tweet Strategy

When someone shares or discusses the tool:

```
Thanks for trying it out! Session discovery was the feature I was most excited about - let me know how it works for your workflow.
```

### Engaging With Competitors' Tweets

**DO:**
- Genuinely compliment their features
- Answer questions if you have helpful context
- Point people to them when their tool fits better

**DON'T:**
- Compare directly without being asked
- Insert yourself into every Claude Code thread
- Disparage other tools

Example of good engagement:
```
Great thread on [competitor's approach]. We took a different path with claude-orchestra - no infrastructure, but also fewer features. Both valid depending on what you need!
```

---

## Phase 4: Ongoing Content Calendar

### Weekly Posting Rhythm

**Monday:** Share a user win or interesting use case
**Wednesday:** Technical tip about Claude Code (general, not just our tool)
**Friday:** Building in public update (what we shipped this week)

### Content Ideas

1. **Session discovery tips**
   ```
   Quick tip: `orchestra sessions --hours 24` + `orchestra search "authentication"`

   Find that Claude session where you designed your auth flow last week.
   ```

2. **Git worktree patterns**
   ```
   Why we use git worktrees for agent isolation:

   - Isolated file state
   - Each agent has its own branch
   - No merge conflicts between parallel agents
   - PRs are natural output

   Native git feature, underused for AI workflows.
   ```

3. **Claude Code general tips (not about our tool)**
   ```
   Underrated Claude Code feature: the CLAUDE.md file

   Put your project context there:
   - Architecture decisions
   - Key files to reference
   - Common commands

   Agents read it automatically. Game changer for context.
   ```

4. **Honest limitations**
   ```
   What claude-orchestra is NOT good for:

   - 50+ agent orchestration (use claude-flow)
   - Enterprise auth/audit (use claude-flow)
   - Persistent memory (use claude-squad)

   We're the lightweight option. Know when to use alternatives.
   ```

---

## Metrics to Track

### Week 1
- Thread impressions
- Profile visits from thread
- GitHub stars from Twitter referrals
- Replies received

### Month 1
- Follower growth
- Engagement rate on tweets
- Click-through to GitHub
- Community sentiment

### Success Signals
- Unsolicited shares/recommendations
- Feature requests in replies
- "I've been using this for X" posts
- Mentions by larger accounts

---

## What NOT To Do

1. **No paid promotion** - Organic only for dev tools
2. **No buying followers** - Obvious and destroys credibility
3. **No automated DMs** - Instant block
4. **No excessive hashtags** - #AI #Claude #Dev #Coding looks spammy
5. **No arguing with critics** - Thank them and improve
6. **No self-promotion in replies to others** - Only when directly relevant
7. **No brigading from other platforms** - Don't ask Discord/Reddit to retweet

---

## Templates for Common Situations

### Someone asks "What's the difference from X?"

```
Good question! [Competitor] is excellent for [their strength].

We focused on:
1. pip-only install (no Docker)
2. Session discovery (unique to us)
3. Designed for 2-8 agents, not enterprise scale

Use whatever fits your workflow - both are open source!
```

### Bug report in tweet

```
Thanks for the report! Mind opening a GitHub issue with:
- Your Python version
- OS
- Steps to reproduce

I'll prioritize fixing it this week: [link to issues]
```

### Feature request

```
Great idea! I've added this to our roadmap: [link to issue]

If you want to see it prioritized, feel free to +1 the issue or add context about your use case.
```

### Celebrity account mentions you

```
[Short, genuine thanks - don't be sycophantic]

Thanks! Built it to scratch my own itch - glad others find it useful too.
```
