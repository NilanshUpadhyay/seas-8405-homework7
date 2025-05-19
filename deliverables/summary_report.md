# Security Remediation Report

## Steps Taken
1. **Code Remediation**:
   - Removed hardcoded PASSWORD, used .env with python-dotenv.
   - Added password authentication to /, /ping, /calculate endpoints.
   - Fixed command injection in /ping with IP validation and subprocess.run (no shell=True).
   - Replaced eval() in /calculate with ast.literal_eval and added expression validation.
   - Restricted Flask to localhost (127.0.0.1).

2. **Docker Hardening**:
   - Switched to python:3.9-slim with multi-stage builds.
   - Ensured non-root user (appuser).
   - Added HEALTHCHECK directive.
   - Minimized dependencies with requirements.txt (Flask==3.0.3, python-dotenv==0.19.0).

3. **Docker Compose Improvements**:
   - Restricted port to 127.0.0.1:6000:5000.
   - Added read_only, no-new-privileges, mem_limit, pids_limit for web and db services.
   - Moved PostgreSQL credentials to .env.
   - Maintained network isolation (frontend, backend).
   - Added named volume for db persistence.

4. **Threat Modeling**:
   - Conducted STRIDE analysis (spoofing, tampering, privilege escalation).
   - Mapped to MITRE ATT&CK (T1190, T1059, T1611) and NIST 800-53 (SC-12, AC-6).
   - Documented in deliverables/threat_model.md.

5. **Automation**:
   - Created docker_security_fixes.py to harden daemon.json, Dockerfile, and docker-compose.yml.

## Vulnerabilities Found and Fixed
- **Hardcoded Password**: Detected by Bandit (make check), moved to .env.
- **Command Injection**: In /ping, fixed with IP validation and subprocess.run.
- **Insecure eval()**: In /calculate, replaced with ast.literal_eval (detected by Bandit).
- **No Authentication**: Added password checks (STRIDE: Spoofing).
- **Root User**: Ensured non-root user (Docker Bench, make host-security).
- **Exposed Ports**: Changed host='0.0.0.0' to '127.0.0.1', restricted to localhost:6000 (vs. 15001:5000).
- **Hardcoded DB Credentials**: Moved to .env for PostgreSQL.

## Architecture Improvements
The hardened architecture includes:
- Minimal container image (python:3.9-slim, Flask==3.0.3).
- Non-root execution (appuser).
- Resource constraints (mem_limit: 256m web, 512m db; pids_limit: 100).
- Read-only filesystem and no-new-privileges.
- Network isolation (frontend, backend bridge networks).
- Secure secrets via .env for Flask and PostgreSQL.
See deliverables/architecture_diagram.png.

## Lessons Learned
- Authentication mitigates spoofing risks (STRIDE).
- Input validation prevents injection (OWASP A1).
- Non-root containers reduce escalation risks (MITRE T1611).
- Environment variables enhance secret management (NIST SC-28).
- Automation ensures consistent hardening.
This exercise emphasized layered security, validated by Bandit, pip-audit, and Docker Bench, and the importance of threat modeling in the SSDLC.