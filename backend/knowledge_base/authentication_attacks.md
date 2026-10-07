# Authentication Attacks

## Overview

Authentication attacks target the mechanisms used to verify user identity.

These attacks may involve password guessing, credential reuse, stolen credentials, or repeated failed authentication attempts.

## Common Indicators

- Repeated authentication failures
- Login attempts from unusual source IP addresses
- Successful login after multiple failures
- Login activity at unusual times
- Multiple accounts accessed from the same source
- Authentication activity from unexpected locations or systems

## Investigation Steps

1. Identify the affected account.
2. Identify the source IP address.
3. Review successful and failed authentication attempts.
4. Determine the frequency and timing of the activity.
5. Check whether multiple accounts were targeted.
6. Review activity after successful authentication.
7. Compare the activity with normal account behavior.

## Defensive Response

- Require multi-factor authentication.
- Enforce strong password policies.
- Apply authentication rate limiting.
- Lock or temporarily restrict compromised accounts.
- Reset credentials when compromise is suspected.
- Monitor suspicious source IP addresses.
- Review authentication logs for related activity.

## Investigation Priority

Authentication failures alone do not always indicate an attack.

The risk increases when repeated failures are associated with:

- A single suspicious source
- Multiple targeted accounts
- A subsequent successful login
- Privilege escalation
- Other suspicious system activity