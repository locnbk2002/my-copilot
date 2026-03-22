// Extension: context-reporter
// Subscribes to session.usage_info events and injects real context window
// usage into the conversation via onPostToolUse additionalContext.
// Replaces usage-context-awareness.py (which used an estimated proxy).
//
// NOTE: session.usage_info is an internal CLI event (not in public SDK docs).
// If it never fires, latestUsage stays null and injection is silently skipped.

import { joinSession } from "@github/copilot-sdk/extension";

const THROTTLE_MS = 60_000; // inject at most once per minute

let latestUsage = null; // { percent, tokens, limit }
let lastInjected = 0;
let usageInfoReceived = false;

const session = await joinSession({
    hooks: {
        onSessionStart: async () => {
            await session.log("context-reporter loaded — waiting for session.usage_info events");
        },
        onPostToolUse: async (_input, _invocation) => {
            if (!latestUsage) return null;

            const now = Date.now();
            if (now - lastInjected < THROTTLE_MS) return null;
            lastInjected = now;

            const { percent, tokens, limit } = latestUsage;
            const tokensK = Math.round(tokens / 1000);
            const limitK = Math.round(limit / 1000);

            const label = percent >= 90
                ? `Context: ${percent}% [CRITICAL] (${tokensK}K/${limitK}K tokens) — start fresh session`
                : percent >= 70
                ? `Context: ${percent}% [WARNING] (${tokensK}K/${limitK}K tokens) — consider /compact`
                : `Context: ${percent}% (${tokensK}K/${limitK}K tokens)`;

            return {
                additionalContext: `<usage-awareness>\n${label}\n</usage-awareness>`,
            };
        },
    },
    tools: [],
});

// Subscribe to real context window data from CLI runtime.
// session.usage_info is ephemeral — fires after each model call.
session.on("session.usage_info", (event) => {
    const { tokenLimit, currentTokens } = event.data ?? {};

    if (typeof tokenLimit !== "number" || tokenLimit <= 0 || typeof currentTokens !== "number" || currentTokens < 0) {
        session.log(`context-reporter: invalid session.usage_info payload — tokenLimit=${tokenLimit}, currentTokens=${currentTokens}`, { level: "warning" });
        return;
    }

    if (!usageInfoReceived) {
        usageInfoReceived = true;
        session.log("context-reporter: receiving real token usage data");
    }

    const percent = Math.min(100, Math.round((currentTokens / tokenLimit) * 100));
    latestUsage = { percent, tokens: currentTokens, limit: tokenLimit };
});
