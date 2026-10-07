# Security Incident Response

## Overview

Incident response is the process of identifying, investigating, containing, and recovering from security incidents.

The AI security assistant should provide investigation guidance and defensive recommendations while leaving final response decisions to authorized security personnel.

## Investigation Process

### 1. Identify

Determine what security event or alert triggered the investigation.

Record:

- Event type
- Timestamp
- Source IP
- Username
- Service
- Severity
- Alert reason

### 2. Investigate

Review related events and determine whether the activity represents a genuine threat.

Look for:

- Repeated suspicious activity
- Related authentication events
- Privilege changes
- Unusual source addresses
- Activity immediately before and after the alert

### 3. Correlate

Connect related events that may belong to the same incident.

For example:

Authentication failures
→ Successful login
→ Privilege escalation
→ Suspicious system activity

This sequence may indicate a larger security incident.

### 4. Contain

Recommended defensive containment actions may include:

- Restricting suspicious source addresses
- Disabling compromised accounts
- Removing unauthorized privileges
- Isolating affected systems
- Increasing monitoring

Containment actions should be performed only by authorized personnel.

### 5. Recover

After containment:

- Restore affected services
- Reset compromised credentials
- Remove unauthorized access
- Verify system integrity
- Continue monitoring

### 6. Document

Record:

- What happened
- When it happened
- Which systems were affected
- Which accounts were involved
- Evidence collected
- Actions taken
- Final outcome

## AI Assistant Guidance

The AI assistant should explain detected threats, summarize relevant evidence, retrieve applicable security knowledge, and recommend defensive investigation steps.

The AI assistant should not independently perform destructive or irreversible actions.