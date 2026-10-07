# Privilege Escalation

## Overview

Privilege escalation occurs when a user or process obtains permissions beyond those normally assigned to it.

Privilege escalation can allow an attacker or compromised account to access sensitive systems or perform administrative actions.

## Common Indicators

- Unexpected administrative privileges
- A normal user obtaining elevated permissions
- Unexpected root or administrator activity
- Changes to user privileges or group memberships
- Suspicious execution of privileged commands
- Administrative activity from an unusual source

## Investigation Steps

1. Identify the account associated with the privilege escalation.
2. Determine the source IP or system where the activity originated.
3. Review the events immediately before the escalation.
4. Identify the process, command, or service responsible.
5. Check whether the account normally has administrative privileges.
6. Review subsequent activity performed with the elevated privileges.
7. Search for related authentication or system events.

## Defensive Response

- Remove unauthorized elevated privileges.
- Disable or restrict a compromised account when appropriate.
- Rotate credentials if compromise is suspected.
- Isolate affected systems when necessary.
- Review administrative group membership.
- Investigate related processes and system activity.
- Preserve relevant logs for further investigation.

## Severity Considerations

Unexpected privilege escalation should generally be treated as a high-risk security event, particularly when it involves administrative or root-level access.