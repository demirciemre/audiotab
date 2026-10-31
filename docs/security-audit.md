# AudioTab security audit: run-1

## 1. Run

| | |
|---|---|
| Method | [Cloudflare security-audit skill](https://github.com/cloudflare/security-audit-skill), full audit mode, **standard** profile |
| Target | `demirciemre/audiotab` at `d4c099a` (v2.5.1), clean worktree |
| Scope | `Sources/` (22 Swift files), `build.sh`, `install.sh`, `.github/workflows/release.yml`, `.gitignore`, `.githooks/commit-msg`, `VERSION` |
| Budget | 26 agent calls set, **18 spent**: 4 reconnaissance, 8 hunters (7 in wave 1, 1 in wave 2), 4 coverage critics, 2 verifiers |
| Execution | Sandboxed: source review plus local checks only. Harnesses ran under `sandbox-exec` with network denied and writes limited to scratch, plus `env -i`, `ulimit` and `timeout`. Nothing contacted GitHub, Apple or any deployed service. Artifacts were promoted with a no-follow, size-bounded copy. |
| Prior runs | None compatible. Upstream had only a prose report from a quick-profile pass on v2.3.0. All units were seeded `prior_status: none`. |
| Deferred / out of scope | None. The wave-1 final-clean critic added one unit (`Tiling.swift`). Wave 2 covered it, and the wave-2 post-wave and final-clean critics both returned no work. |

This is one full pass with complete ledger coverage. It does not prove the app is free of vulnerabilities. In particular, runtime behaviour that needs TCC grants, real displays or a macOS VM was not exercised.

## 2. Posture

There are **no confirmed vulnerabilities**. The update channel is the most valuable boundary, and it is sound:
- Each update must carry an Apple-anchored Developer ID signature from the running copy's own Team ID and be notarized, with strict validation on every architecture.
- The signed bundle version must equal the version the release metadata names.
- Downgrades happen only when the user picks an older version.
- Traffic goes over HTTPS only, to an exact allowlist of GitHub hosts, and that check is repeated on every redirect.

CI signs only on `v*` tags. Pull-request code never gets secrets.

One lead remains open: an insecure archive decode in Finder favorites. Whether anyone outside the user's own processes can write the file it reads is unknown.

## 3. Confirmed findings

None.

## 4. Needs validation

| Lead | Trace | Blocker | Local next step | Owner check |
|---|---|---|---|---|
| Finder favorites archive decoded with `requiresSecureCoding = false` (`audiotab:Favorites.fromSFL:NSKeyedUnarchiver-requiresSecureCoding-false`) | `Switcher.swift:802` → `Favorites.swift:60` → `:77` (fallback) → `:90` → `:94` `decodeTopLevelObject` | (a) It is unknown whether a process with less authority than AudioTab can write `~/Library/Application Support/com.apple.sharedfilelist/*.sfl3`. `listxattr` on that directory fails with EPERM, which suggests OS protection. (b) No gadget chain has been shown. (c) The path is reachable only through the fallback and only when "Finder favorites" is on (default off). | On a dummy-user VM, try writing that file from a process that has no TCC grants and from a sandboxed app. If either can write it, check whether a benign NSCoding class gets instantiated. | Confirm whether the directory is TCC or data-vault protected on macOS 13 and later. |

**Fixed regardless of the open question.** The decode now uses `NSKeyedUnarchiver.unarchivedObject(ofClasses:)` with a plist-type allowlist. The hunter's harness showed that this rejects the non-plist class (error 4864) and still decodes a benign archive.

## 5. Hardening applied after the audit

| Area | Change |
|---|---|
| Updater | `tag_name` is validated with `^v?\d{1,6}\.\d{1,6}\.\d{1,6}$` on every path, and the URL force-unwrap is gone. `html_url` is opened only if it passes the GitHub host allowlist. A symlinked `AudioTab.app` in the zip is rejected. The bundle is copied next to the destination, the **copy is verified again**, and then it is moved into place in one step, which closes the verify/copy window and the half-copy window. `kSecCSEnforceRevocationChecks` was added. |
| CI | Split into a `build` job (`contents: read`) and a `release` job (`contents: write`). The release job runs only after a signed tag build. Signing secrets reach the runner only on tag pushes and `workflow_dispatch`. Build timeout is 180 minutes. |
| `build.sh` | `xattr -cr` is now limited to the built app. Notarization waits up to 2 hours (Apple is slow on first submissions) and reports a timeout separately from a rejection. |
| `install.sh` | A symlinked `AudioTab.app` is rejected, and the installed copy is checked again with `codesign -R` after `ditto`. |
| `.gitignore` | Adds `*.p8`, `*.pem`, `.env*` and `notary.json`. |
| Favorites | Uses the secure decode above. A package (`.app`) favorite is now revealed in Finder instead of launched. |
| Diagnostics copy | E-mails are redacted *before* truncation, so a cut-off address no longer leaks a partial local part. Account names are masked. |
| Hotkeys / signals | SIGTERM and SIGINT are handled with a `DispatchSourceSignal` on the main queue, so no unsafe code runs in a signal handler. Toggling ⌘Tab during secure input no longer re-disables macOS ⌘Tab. The blackout keyboard lock now applies only while its ⌘⇧< escape is enabled. |
| DDC | The reported current value is clamped to the maximum. |

**Not applied (reasons):**
- Exclusive-create for capture files: the default folder is the user's own Desktop.
- Re-validating tiling targets at apply time: no impact found.
- An explicit allowlist for the migration key: the same writer can already set AudioTab's own domain.
- Repository settings the owner should set: an `environment: release` with required reviewers, a `v*` tag ruleset, and an `--is-ancestor origin/main` check.
- Documentation only: after a crash or SIGKILL, macOS hotkeys stay disabled until the next launch.

## 6. Positive patterns

- The update trust root is Apple's, not a self-signed certificate. The Team ID is read from the running copy's own signature, so ad-hoc builds cannot self-update.
- No secrets exist in the tree or in the history. Actions are pinned by SHA. `persist-credentials: false` is set. `VERSION` and ref names are validated before they reach a shell.
- Every process launch uses a fixed absolute executable with an argv array. The only `sh -c` passes the path as a quoted `$0`.
- The keystroke tap reads only the keycode and flags, and stores, logs and forwards nothing. All overlays use `sharingType = .none`.
- Private API calls match their C ABI. A harness checked buffer sizes. The DDC reply parse and the scrolling stitcher stayed in bounds under thousands of hostile and edge-case inputs.

## 7. Coverage

There are 19 ledger units:

| Status | Count |
|---|---|
| Covered | 18 |
| Candidate (needs_validation, verified in Phase 5) | 1 |
| Blocked | 0 |
| Deferred | 0 |

Companions selected:
- `SUPPLY-CHAIN-AND-RELEASE`
- `DESKTOP-MOBILE-AND-LOCAL-IPC`
- `MEMORY-SAFETY-AND-BINARY`

Companions excluded, with the reason in the ledger: web/auth, client-side, cloud, protocols/RPC, AI, data isolation and resource exhaustion. The app has no server, webview, IPC listener, tenants or shared service.

Final critic result: clean, from both the post-wave and the final-clean critic after wave 2.
