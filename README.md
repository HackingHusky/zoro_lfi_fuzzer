# ⚔️ Santoryu LFI Fuzzer (wado_ichimonji_lfi.py)

An ultra-fast, asynchronous Local File Inclusion (LFI) fuzzing tool forged in the spirit of Pirate Hunter Roronoa Zoro. Built specifically to eliminate noise and slash open targets during high-speed triage environments like **CPTS** and **OSCP**.


,/|      _   _/|_   ( )( )_        --- SANTORYU LFI FUZZER ---(  _  ) (_  _ _  _)       [ Wado Ichimonji | Sandai Kitetsu | Shusui ]| || |   | | | |__/   () ()

## ⚡ Features

*   **Three-Sword Speed**: Powered by Python's `asyncio` and `aiohttp` for blindingly fast concurrent network requests.
*   **Haki Baseline Calibration**: Automatically fingerprints the target's normal response size to dynamically filter out 404/403 false positives.
*   **Oni Giri Strikes**: High-contrast, color-coded terminal alerts that trigger immediately when system file signatures (`root:x:`, `boot.ini`) are sliced open.
*   **Clean Output**: Network timeouts and blocked paths drop silently into the dust, keeping your screen clean under exam pressure.

## 🛠️ Prerequisites

Install the asynchronous HTTP client library before unsheathing the script:

```bash
pip install aiohttp
```

## 🚀 Usage

```bash
python wado_ichimonji_lfi.py -u <TARGET_URL> -p <PARAM> -w <WORDLIST> [OPTIONS]
```

### Options
*   `-u`, `--url` : Target URL containing the vulnerable parameter (e.g., `http://10.10.11`)
*   `-p`, `--param` : The specific query parameter to slice open (e.g., `page`)
*   `-w`, `--wordlist` : Path to your collection of sword techniques / payload wordlist
*   `-c`, `--concurrency` : Number of concurrent slashes to unleash (Default: `20`)

### Combat Example

```bash
python wado_ichimonji_lfi.py -u "http://10.10.11" -p file -w paths.txt -c 30
```

## 🎯 Visual Feed Output

*   `[!!!] ONI GIRI! Guard Broken` : **[Moss Green]** Confirmed structural hit matching known OS file signatures.
*   `[+] CHITOSE HAZAMI! Guard Altered` : **[Gold]** Behavioral shift or size/status anomaly compared to baseline defense.

---
*Disclaimer: Created for authorized penetration testing, CTFs, and security evaluations only. Nothin' personal, it's just a job.*
