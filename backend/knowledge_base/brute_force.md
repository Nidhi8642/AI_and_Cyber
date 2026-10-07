# Brute Force Attack

## Overview

A brute force attack occurs when an attacker repeatedly attempts to authenticate to an account or service using different passwords or credentials.

Repeated authentication failures from the same source IP can indicate a brute force or password guessing attack.

## Common Indicators

- Multiple authentication failures from the same IP address
- Repeated failed login attempts against the same username
- Login attempts occurring at a high frequency
- Multiple accounts targeted from a single source
- Successful authentication following many failed attempts

## Investigation Steps

1. Identify the source IP generating the failed authentication attempts.
2. Determine which usernames or accounts were targeted.
3. Check the number and frequency of failed attempts.
4. Look for a successful login following the failures.
5. Review other security events from the same source IP.
6. Determine whether the source IP is known or trusted.
7. Check whether the affected account performed any suspicious activity after authentication.

## Defensive Response

- Temporarily block or rate-limit the suspicious source IP when appropriate.
- Enforce account lockout or authentication rate limiting.
- Require multi-factor authentication.
- Reset credentials if compromise is suspected.
- Review authentication logs for related activity.
- Monitor the affected accounts for additional suspicious behavior.

## Severity Considerations

A small number of failed attempts may be normal user behavior.

A large number of repeated failures, especially when followed by a successful login, should be investigated as a potentially high-risk event.