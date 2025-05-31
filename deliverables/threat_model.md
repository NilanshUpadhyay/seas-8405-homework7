# Threat Model: Secure Containerized Microservices
## 1. Overview
This document outlines the threat modeling exercise performed on the initial insecure Flask application, following STRIDE and MITRE ATT&CK methodologies. The analysis informed remediation efforts, resulting in a hardened application.
## 2. STRIDE Analysis
| Threat Category | Example | Impact | Mitigation |
|----------------|---------|--------|------------|
| Spoofing        | Lack of auth on /calculate | Unauthorized access | Added input validation; authentication not implemented due to scope |
| Tampering       | Unsafe IP input to ping | Command injection | Implemented strict IP validation and removed shell=True in pp.py |
| Repudiation     | No logging | Difficult to audit usage | Logging not implemented; recommend adding Flask logging in production |
| Information Disclosure | Hardcoded passwords | Credential leak | Moved to .env file with python-dotenv |
| Denial of Service | Unrestricted ping or eval | Resource exhaustion | Added mem_limit: 256m, pids_limit: 100, and input validation |
| Elevation of Privilege | Root container user | Full system compromise | Used USER appuser and security_opt: no-new-privileges:true |
## 3. MITRE ATT&CK Mapping (Containers)
| Tactic         | Technique ID | Technique Name | Application Relevance |
|----------------|--------------|----------------|------------------------|
| Initial Access | T1190         | Exploit Public-Facing Application | Command injection in /ping (mitigated with validation) |
| Execution      | T1059         | Command and Scripting Interpreter | Use of eval() (replaced with st.literal_eval) |
| Persistence    | T1525         | Implant Container Image | No image signing (recommend adding in production) |
| Privilege Escalation | T1611  | Escape to Host | Root user (mitigated with non-root ppuser) |
| Defense Evasion | T1211        | Exploitation for Defense Evasion | Lack of file system isolation (mitigated with ead_only: true) |
## 4. Controls Mapping
| Issue | Recommended Control | Framework Reference |
|-------|---------------------|---------------------|
| Hardcoded secrets | Use .env with python-dotenv | NIST 800-53: SC-12, SC-28 |
| Root container user | USER appuser in Dockerfile | NIST 800-53: AC-6, CM-6 |
| No network restrictions | internal: true networks and 127.0.0.1 port binding | NIST 800-53: SC-7 |
| Missing health check | HEALTHCHECK in Dockerfile | CIS Docker Benchmark |
| Unvalidated inputs | Strict validation in pp.py | OWASP Top 10: A1-Injection |
## 5. Risk Rating Summary
| Threat | Risk | Likelihood | Impact | Mitigation Priority | Post-Remediation Risk |
|--------|------|------------|--------|----------------------|-----------------------|
| Command Injection | High | High | Critical | Immediate | Low |
| Credential Exposure | Medium | High | Medium | High | Low |
| Eval-based execution | High | Medium | High | Immediate | Low |
| Root user in container | High | Medium | Critical | Immediate | Low |
## 6. Conclusion
This threat model identified critical flaws in the initial application, such as command injection, hardcoded secrets, and root user privileges. Remediation efforts, including input validation, st.literal_eval, non-root users, and Docker hardening, significantly reduced the attack surface. Post-remediation scans (deliverables/scan_check_after.txt, scan_docker_after.txt) confirm reduced vulnerabilities. The final implementation enforces least privilege, defense in depth, and secure defaults, aligning with NIST 800-53 and CIS Docker Benchmark standards.
