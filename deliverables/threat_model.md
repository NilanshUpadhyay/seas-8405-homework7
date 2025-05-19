# Threat Model: Secure Containerized Microservices

## 1. Overview
This threat model analyzes the insecure Flask application using STRIDE and MITRE ATT&CK for Containers, identifying vulnerabilities and mitigations.

## 2. STRIDE Analysis
| Threat Category | Example | Impact | Mitigation |
|----------------|---------|--------|------------|
| Spoofing | No authentication on endpoints | Unauthorized access | Added password check in /, /ping, /calculate |
| Tampering | Unsafe IP input to /ping | Command injection | IP validation with regex |
| Information Disclosure | Hardcoded PASSWORD, DB credentials | Credential leak | Used .env file |
| Denial of Service | Unrestricted ping/calculate | Resource exhaustion | Resource limits in docker-compose.yml |
| Elevation of Privilege | Potential root access in container | System compromise | Non-root user in Dockerfile |

## 3. MITRE ATT&CK Mapping (Containers)
| Tactic | Technique ID | Technique Name | Application Relevance |
|--------|--------------|----------------|-----------------------|
| Initial Access | T1190 | Exploit Public-Facing Application | Command injection in /ping |
| Execution | T1059 | Command and Scripting Interpreter | eval() in /calculate |
| Persistence | T1525 | Implant Container Image | No image validation |
| Privilege Escalation | T1611 | Escape to Host | Root user risks |
| Defense Evasion | T1211 | Exploitation for Defense Evasion | No filesystem isolation |

## 4. Controls Mapping
| Issue | Recommended Control | Framework Reference |
|-------|---------------------|---------------------|
| Hardcoded PASSWORD, DB credentials | Environment variables | NIST 800-53: SC-12, SC-28 |
| Root user | USER appuser | NIST 800-53: AC-6, CM-6 |
| Network exposure | Restrict to localhost, network isolation | NIST 800-53: SC-7 |
| Missing health check | HEALTHCHECK directive | CIS Docker Benchmark |
| Unvalidated inputs | Regex validation | OWASP Top 10: A1-Injection |

## 5. Risk Rating Summary
| Threat | Risk | Likelihood | Impact | Mitigation Priority |
|--------|------|------------|--------|---------------------|
| Command Injection | High | High | Critical | Immediate |
| Credential Exposure | Medium | High | Medium | High |
| Eval-based Execution | High | Medium | High | Immediate |
| Root User | High | Medium | Critical | Immediate |

## 6. Conclusion
The remediated application reduces the attack surface through authentication, input validation, non-root execution, network isolation, and secure secret management, aligning with secure defaults and least privilege principles.