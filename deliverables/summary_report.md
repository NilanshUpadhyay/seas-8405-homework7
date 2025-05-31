# Summary Report: Securing Containerized Microservices

## 1. Introduction
This report summarizes the process of securing a vulnerable Flask application, including environment setup, code remediation, Docker hardening, threat modeling, and architecture design.

## 2. Steps Taken
1. **Environment Setup**:
   - Cloned the repository and ran make start in efore/ to launch the Flask app and PostgreSQL.
   - Tested endpoints (/, /ping?ip=8.8.8.8, /calculate?expr=2+3).
   - Performed scans (make check, make scan, make host-security) to identify vulnerabilities.
2. **Code Remediation**:
   - Refactored pp.py to remove hardcoded secrets, replace eval() with st.literal_eval, validate inputs, and restrict Flask to 127.0.0.1.
   - Added python-dotenv for secrets management.
3. **Docker Hardening**:
   - Updated Dockerfile with multi-stage builds, HEALTHCHECK, and non-root user.
   - Improved docker-compose.yml with ead_only, security_opt, mem_limit, pids_limit, and .env secrets.
4. **Threat Modeling**:
   - Conducted STRIDE analysis and MITRE ATT&CK mapping, documented in 	hreat_model.md.
   - Mapped controls to NIST 800-53 and CIS Docker Benchmark.
5. **Security Architecture**:
   - Created rchitecture_diagram.png showing hardened infrastructure.
   - Wrote docker_security_fixes.py to automate hardening of daemon.json, Dockerfile, and docker-compose.yml.
6. **Verification**:
   - Re-ran scans in fter/ to confirm reduced vulnerabilities.
   - Recorded a simulation (simulation.mp4) demonstrating the process.

## 3. Vulnerabilities Found and Fixed
- **Hardcoded Secrets**: Moved to .env file.
- **Command Injection**: Validated IP inputs and removed shell=True in /ping.
- **Insecure eval()**: Replaced with st.literal_eval in /calculate.
- **Root User**: Used USER appuser in Dockerfile.
- **Exposed Ports**: Restricted to 127.0.0.1 in docker-compose.yml.
- **Lack of Resource Limits**: Added mem_limit and pids_limit.

## 4. Architecture and Security Improvements
The hardened architecture includes:
- **Flask Container**: Runs as non-root, read-only, with HEALTHCHECK and input validation.
- **PostgreSQL Container**: Uses .env secrets and read-only filesystem.
- **Networks**: Isolated with internal: true.
- **Docker Host**: Hardened with daemon.json (e.g., userns-remap, 
o-new-privileges).
These align with NIST 800-53 (SC-7, AC-6) and CIS Docker Benchmark, enforcing least privilege and defense in depth.

## 5. Lessons Learned
- **Input Validation**: Critical for preventing injection attacks.
- **Container Security**: Non-root users and resource limits reduce risks.
- **Threat Modeling**: STRIDE and MITRE ATT&CK provide structured risk identification.
- **Automation**: Scripts like docker_security_fixes.py streamline hardening.
- **Secure Defaults**: Using .env and restricted ports prevents misconfigurations.

## 6. Conclusion
This assignment transformed a vulnerable application into a secure deployment, reducing risks like command injection and credential exposure. The process highlighted the importance of secure coding, container hardening, and systematic threat modeling in the SSDLC.
