import google.generativeai as genai
import os
from dotenv import load_dotenv
import colorama
from colorama import Fore, Style
import re
from config import PROMPT_TEMPLATES

# Initialize colorama
colorama.init()

# Load manuals from files
def load_manual(filename):
    try:
        with open(os.path.join('manuals', filename), 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Manual file '{filename}' not found in manuals/ directory.{Style.RESET_ALL}")
        return ""
    except Exception as e:
        print(f"{Fore.RED}Error reading manual file '{filename}': {e}{Style.RESET_ALL}")
        return ""

# Load manuals for all tools
MANUALS = {
    'subfinder': load_manual('subfinder_manual.txt'),
    'naabu': load_manual('naabu_manual.txt'),
    'katana': load_manual('katana_manual.txt'),
    'dirsearch': load_manual('dirsearch_manual.txt'),
    'ffuf': load_manual('ffuf_manual.txt'),
    'amass': load_manual('amass_manual.txt'),
    'arjun': load_manual('arjun_manual.txt'),
    'bxss': load_manual('bxss_manual.txt'),
    'dirbuster': load_manual('dirbuster_manual.txt'),
    'dnsx': load_manual('dnsx_manual.txt'),
    'eyewitness': load_manual('eyewitness_manual.txt'),
    'feroxbuster': load_manual('feroxbuster_manual.txt'),
    'gau': load_manual('gau_manual.txt'),
    'getjs': load_manual('getJS_manual.txt'),
    'gitgrabber': load_manual('git_grabber_manual.txt'),
    'githound': load_manual('githound_manual.txt'),
    'gitsecrets': load_manual('gitsecrets_manual.txt'),
    'gowitness': load_manual('gowitness_manual.txt'),
    'hakrawler': load_manual('hakrawler_manual.txt'),
    'httprobe': load_manual('httprobe_manual.txt'),
    'httpx': load_manual('httpx_manual.txt'),
    'loxs': load_manual('loxs_manual.txt'),
    'masscan': load_manual('masscan_manual.txt'),
    'nomore403': load_manual('nomore403_manual.txt'),
    'openredirex': load_manual('openredirex_manual.txt'),
    'oralyzer': load_manual('oralyzer_manual.txt'),
    'paramspider': load_manual('paramspider_manual.txt'),
    'puredns': load_manual('puredns_manual.txt'),
    'rustbuster': load_manual('rustbuster_manual.txt'),
    'rustscan': load_manual('rustscan_manual.txt'),
    'rustyhog': load_manual('rustyhog_manual.txt'),
    's3scanner': load_manual('s3scanner_manual.txt'),
    'secretlint': load_manual('secretlint_manual.txt'),
    'shuffledns': load_manual('shuffledns_manual.txt'),
    'sqlmap': load_manual('sqlmap_manual.txt'),
    'subjs': load_manual('subjs_manual.txt'),
    'subzy': load_manual('subzy_manual.txt'),
    'trufflehog': load_manual('trufflehog_manual.txt'),
    'waybackurls': load_manual('waybackurls_manual.txt'),
    'waymore': load_manual('waymore_manual.txt'),
    'wfuzz': load_manual('wfuzz_manual.txt'),
    'xnlinkfinder': load_manual('xnlinkfinder_manual.txt'),
    'xsser': load_manual('xsser_manual.txt'),
    'xsstrike': load_manual('xsstrike_manual.txt')
}

# Common commands for all tools (as provided or placeholders for brevity)
# Commonly used commands with descriptions
COMMON_SUBFINDER_COMMANDS = [
    {"command": "subfinder -d hackerone.com", "description": "Find subdomains for a single domain." , "Author":""},
]

COMMON_NAABU_COMMANDS = [
    {"command": "naabu -p 0-65535 -host example.com", "description": "Scan all ports for a host." , "Author":""},
    {"command": "naabu -list subdomains.txt -verify -ec -rate 9000 -retries 1 -p 80,443 -c 50 -o naabu-fast.txt", "description": "Fast scan and verify open ports 80 and 443 for subdomains from a list, output to file." , "Author":""},
    {"command": "naabu -list subdomains.txt -verify -ec -rate 9000 -retries 1 -p 0-65535 -warm-up-time 0 -c 50 -nmap-cli 'nmap -sV -oG nmap-naabu-out' -silent -o naabu-full.txt", "description": "Full port scan with service enumeration using Nmap, for subdomains from a list, output to file." , "Author":""},
]

COMMON_KATANA_COMMANDS = [
    {"command": "katana -u http://example.com", "description": "Basic crawl of a single URL." , "Author":""},
    {"command": "katana -f qurl -o qurl-output.txt -u http://example.com", "description": "Output query parameters from crawled URLs to a file." , "Author":""},
]
COMMON_DIRSEARCH_COMMANDS = [
    {"command": "dirsearch -u http://example.com", "description": "Basic directory and file discovery on a target URL.", "Author": ""},
    {"command": "dirsearch -u http://example.com -e php,html,js -o dirsearch-results.txt", "description": "Search for specific file extensions and save results.", "Author": ""},
    {"command": "dirsearch -l urls.txt -e php,asp,aspx,jsp,html,zip,jar", "description": "Scan multiple URLs from a file for various file types.", "Author": ""},
    {"command": "dirsearch -u http://example.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt", "description": "Use custom wordlist for directory discovery.", "Author": ""},
]

COMMON_FFUF_COMMANDS = [
    {"command": "ffuf -w /usr/share/wordlists/dirb/common.txt -u http://example.com/FUZZ", "description": "Basic directory fuzzing with common wordlist.", "Author": ""},
    {"command": "ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-directories.txt -u http://example.com/FUZZ -mc 200,204,301,302,307,401,403", "description": "Directory fuzzing with specific response codes.", "Author": ""},
    {"command": "ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt -u http://example.com/index.php?FUZZ=test_value", "description": "Parameter fuzzing to discover hidden parameters.", "Author": ""},
    {"command": "ffuf -w /usr/share/wordlists/seclists/Usernames/Names/names.txt -u http://example.com/FUZZ -H 'Host: FUZZ.example.com'", "description": "Virtual host discovery using Host header fuzzing.", "Author": ""},
]

COMMON_AMASS_COMMANDS = [
    {"command": "amass enum -d example.com", "description": "Basic subdomain enumeration for a domain.", "Author": ""},
    {"command": "amass enum -d example.com -o amass-results.txt", "description": "Subdomain enumeration with output to file.", "Author": ""},
    {"command": "amass enum -df domains.txt -o amass-multiple.txt", "description": "Enumerate subdomains for multiple domains from file.", "Author": ""},
    {"command": "amass enum -active -d example.com -brute", "description": "Active enumeration with brute force techniques.", "Author": ""},
    {"command": "amass intel -d example.com", "description": "Intelligence gathering on target domain.", "Author": ""},
]

COMMON_ARJUN_COMMANDS = [
    {"command": "arjun -u http://example.com", "description": "Basic parameter discovery on a URL.", "Author": ""},
    {"command": "arjun -u http://example.com -m POST", "description": "Parameter discovery using POST method.", "Author": ""},
    {"command": "arjun -i urls.txt -o arjun-results.txt", "description": "Parameter discovery on multiple URLs from file.", "Author": ""},
    {"command": "arjun -u http://example.com --headers 'Authorization: Bearer token123'", "description": "Parameter discovery with custom headers.", "Author": ""},
]

COMMON_BXSS_COMMANDS = [
    {"command": "bxss -appendMode -payload '\"><script src=https://xss.bxss.me/t/fit_ID_HERE></script>'", "description": "Basic blind XSS testing with custom payload.", "Author": ""},
    {"command": "bxss -url http://example.com/search?q=BXSS", "description": "Test specific URL for blind XSS vulnerability.", "Author": ""},
    {"command": "bxss -burpFile requests.xml", "description": "Test URLs from Burp Suite history file.", "Author": ""},
]

COMMON_DIRBUSTER_COMMANDS = [
    {"command": "dirb http://example.com", "description": "Basic directory discovery with default wordlist.", "Author": ""},
    {"command": "dirb http://example.com /usr/share/wordlists/dirb/big.txt", "description": "Directory discovery with custom wordlist.", "Author": ""},
    {"command": "dirb http://example.com -o dirb-results.txt", "description": "Directory discovery with output to file.", "Author": ""},
    {"command": "dirb http://example.com -x .php,.html,.txt", "description": "Search for files with specific extensions.", "Author": ""},
]

COMMON_DNSX_COMMANDS = [
    {"command": "dnsx -l subdomains.txt", "description": "DNS resolution for subdomains from file.", "Author": ""},
    {"command": "dnsx -l subdomains.txt -a -aaaa -cname -ns -txt -mx", "description": "Comprehensive DNS record lookup.", "Author": ""},
    {"command": "dnsx -l subdomains.txt -resp -o dns-results.txt", "description": "DNS resolution with response data output.", "Author": ""},
    {"command": "dnsx -l subdomains.txt -cdn", "description": "Check if domains are behind CDN.", "Author": ""},
]

COMMON_EYEWITNESS_COMMANDS = [
    {"command": "eyewitness --web -f urls.txt", "description": "Take screenshots of web applications from URL list.", "Author": ""},
    {"command": "eyewitness --web -x nmap-results.xml", "description": "Take screenshots from Nmap XML results.", "Author": ""},
    {"command": "eyewitness --web -f urls.txt --no-prompt", "description": "Automated screenshot capture without prompts.", "Author": ""},
    {"command": "eyewitness --web -f urls.txt --timeout 30", "description": "Screenshot capture with custom timeout.", "Author": ""},
]

COMMON_FEROXBUSTER_COMMANDS = [
    {"command": "feroxbuster -u http://example.com", "description": "Basic directory and file discovery.", "Author": ""},
    {"command": "feroxbuster -u http://example.com -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt", "description": "Directory discovery with custom wordlist.", "Author": ""},
    {"command": "feroxbuster -u http://example.com -x php,html,txt -o ferox-results.txt", "description": "File discovery with specific extensions and output.", "Author": ""},
    {"command": "feroxbuster -u http://example.com --extract-links", "description": "Extract and follow links during discovery.", "Author": ""},
]

COMMON_GAU_COMMANDS = [
    {"command": "gau example.com", "description": "Fetch URLs for domain from web archives.", "Author": ""},
    {"command": "gau example.com --subs", "description": "Include subdomains in URL fetching.", "Author": ""},
    {"command": "gau example.com -o gau-urls.txt", "description": "Save fetched URLs to output file.", "Author": ""},
    {"command": "gau example.com --blacklist png,jpg,gif,css", "description": "Exclude specific file types from results.", "Author": ""},
]

COMMON_GETJS_COMMANDS = [
    {"command": "getJS --url http://example.com", "description": "Extract JavaScript files from a single URL.", "Author": ""},
    {"command": "getJS --input urls.txt --output js-files.txt", "description": "Extract JS files from multiple URLs and save results.", "Author": ""},
    {"command": "getJS --url http://example.com --complete", "description": "Extract JS with complete source code.", "Author": ""},
    {"command": "getJS --input urls.txt --resolve", "description": "Resolve and extract JS files with full content.", "Author": ""},
]

COMMON_GITGRABBER_COMMANDS = [
    {"command": "gitGraber.py -k wordlist.txt -q example.com", "description": "Search for Git repositories using keywords.", "Author": ""},
    {"command": "gitGraber.py -k wordlist.txt -q example.com -s", "description": "Search with sorting by repository creation date.", "Author": ""},
    {"command": "gitGraber.py -k wordlist.txt -q example.com -o git-results.txt", "description": "Save Git repository search results to file.", "Author": ""},
]

COMMON_GITHOUND_COMMANDS = [
    {"command": "githound --search-query 'example.com'", "description": "Search GitHub for mentions of target domain.", "Author": ""},
    {"command": "githound --search-query 'API_KEY OR apikey' --language javascript", "description": "Search for API keys in JavaScript repositories.", "Author": ""},
    {"command": "githound --search-query 'password' --dig-files --dig-commits", "description": "Deep search in files and commits for passwords.", "Author": ""},
]

COMMON_GITSECRETS_COMMANDS = [
    {"command": "git-secrets --scan", "description": "Scan current repository for secrets.", "Author": ""},
    {"command": "git-secrets --scan-history", "description": "Scan entire Git history for secrets.", "Author": ""},
    {"command": "git-secrets --install", "description": "Install git-secrets hooks in repository.", "Author": ""},
    {"command": "git-secrets --register-aws", "description": "Register AWS secret patterns.", "Author": ""},
]

COMMON_GOWITNESS_COMMANDS = [
    {"command": "gowitness single -u http://example.com", "description": "Take screenshot of single URL.", "Author": ""},
    {"command": "gowitness file -f urls.txt", "description": "Take screenshots of URLs from file.", "Author": ""},
    {"command": "gowitness nmap -f nmap-results.xml", "description": "Take screenshots from Nmap XML results.", "Author": ""},
    {"command": "gowitness file -f urls.txt --timeout 30", "description": "Screenshot capture with custom timeout.", "Author": ""},
]

COMMON_HAKRAWLER_COMMANDS = [
    {"command": "hakrawler -url http://example.com", "description": "Basic web crawling of single URL.", "Author": ""},
    {"command": "hakrawler -url http://example.com -depth 3", "description": "Crawl with specific depth limit.", "Author": ""},
    {"command": "hakrawler -urls urls.txt -o crawled-urls.txt", "description": "Crawl multiple URLs and save results.", "Author": ""},
    {"command": "hakrawler -url http://example.com -js", "description": "Include JavaScript file URLs in crawling.", "Author": ""},
]

COMMON_HTTPROBE_COMMANDS = [
    {"command": "cat subdomains.txt | httprobe", "description": "Probe subdomains for HTTP/HTTPS services.", "Author": ""},
    {"command": "cat subdomains.txt | httprobe -c 50", "description": "Probe with 50 concurrent connections.", "Author": ""},
    {"command": "cat subdomains.txt | httprobe -p http:8080 -p https:8443", "description": "Probe specific ports for HTTP/HTTPS.", "Author": ""},
    {"command": "cat subdomains.txt | httprobe > live-urls.txt", "description": "Save live URLs to output file.", "Author": ""},
]

COMMON_HTTPX_COMMANDS = [
    {"command": "httpx -l urls.txt", "description": "Basic HTTP probing of URLs from file.", "Author": ""},
    {"command": "httpx -l subdomains.txt -ports 80,443,8080,8443", "description": "Probe specific ports on subdomains.", "Author": ""},
    {"command": "httpx -l urls.txt -title -tech-detect -status-code", "description": "Extract titles, detect technologies, and show status codes.", "Author": ""},
    {"command": "httpx -l urls.txt -o httpx-results.txt", "description": "Save probing results to output file.", "Author": ""},
]

COMMON_LOXS_COMMANDS = [
    {"command": "loxs -u http://example.com", "description": "Basic XSS scanning of single URL.", "Author": ""},
    {"command": "loxs -l urls.txt", "description": "XSS scanning of multiple URLs from file.", "Author": ""},
    {"command": "loxs -u http://example.com -p 'param1,param2'", "description": "Test specific parameters for XSS.", "Author": ""},
]

COMMON_MASSCAN_COMMANDS = [
    {"command": "masscan -p1-65535 192.168.1.0/24 --rate=1000", "description": "Scan all ports on subnet with specified rate.", "Author": ""},
    {"command": "masscan -p80,443 -iL targets.txt --rate=10000", "description": "Fast scan of web ports on targets from file.", "Author": ""},
    {"command": "masscan -p1-1000 192.168.1.1 -oG masscan-results.txt", "description": "Port scan with grepable output format.", "Author": ""},
    {"command": "masscan --top-ports 100 192.168.1.0/24", "description": "Scan top 100 most common ports.", "Author": ""},
]

COMMON_NOMORE403_COMMANDS = [
    {"command": "nomore403 -u http://example.com/admin", "description": "Bypass 403 forbidden errors on specific endpoint.", "Author": ""},
    {"command": "nomore403 -u http://example.com/admin -b", "description": "Use brute force techniques to bypass restrictions.", "Author": ""},
    {"command": "nomore403 -l forbidden-urls.txt", "description": "Test multiple forbidden URLs from file.", "Author": ""},
]

COMMON_OPENREDIREX_COMMANDS = [
    {"command": "openredirex -l urls.txt", "description": "Test URLs from file for open redirect vulnerabilities.", "Author": ""},
    {"command": "openredirex -u http://example.com", "description": "Test single URL for open redirect.", "Author": ""},
    {"command": "openredirex -l urls.txt -p payloads.txt", "description": "Use custom payloads for open redirect testing.", "Author": ""},
]

COMMON_ORALYZER_COMMANDS = [
    {"command": "oralyzer -u http://example.com", "description": "Analyze single URL for open redirect vulnerabilities.", "Author": ""},
    {"command": "oralyzer -l urls.txt", "description": "Analyze multiple URLs from file.", "Author": ""},
    {"command": "oralyzer -u http://example.com -p custom-payloads.txt", "description": "Use custom payloads for analysis.", "Author": ""},
]

COMMON_PARAMSPIDER_COMMANDS = [
    {"command": "paramspider.py -d example.com", "description": "Discover parameters for target domain.", "Author": ""},
    {"command": "paramspider.py -l domains.txt", "description": "Parameter discovery for multiple domains.", "Author": ""},
    {"command": "paramspider.py -d example.com -s", "description": "Save results and clean output.", "Author": ""},
    {"command": "paramspider.py -d example.com --exclude png,jpg,gif", "description": "Exclude specific file types from parameter discovery.", "Author": ""},
]

COMMON_PUREDNS_COMMANDS = [
    {"command": "puredns bruteforce wordlist.txt example.com", "description": "DNS brute forcing with wordlist.", "Author": ""},
    {"command": "puredns resolve subdomains.txt", "description": "Resolve subdomains and filter live ones.", "Author": ""},
    {"command": "puredns bruteforce wordlist.txt example.com -r resolvers.txt", "description": "Use custom DNS resolvers for brute forcing.", "Author": ""},
    {"command": "puredns resolve subdomains.txt -w resolved.txt", "description": "Save resolved subdomains to output file.", "Author": ""},
]

COMMON_RUSTBUSTER_COMMANDS = [
    {"command": "rustbuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt", "description": "Basic directory discovery.", "Author": ""},
    {"command": "rustbuster dir -u http://example.com -w wordlist.txt -e php,html,txt", "description": "Directory discovery with file extensions.", "Author": ""},
    {"command": "rustbuster vhost -u http://example.com -w vhost-wordlist.txt", "description": "Virtual host discovery.", "Author": ""},
]

COMMON_RUSTSCAN_COMMANDS = [
    {"command": "rustscan -a 192.168.1.1", "description": "Basic port scan of single IP.", "Author": ""},
    {"command": "rustscan -a 192.168.1.0/24 -p 1-1000", "description": "Scan port range on subnet.", "Author": ""},
    {"command": "rustscan -a 192.168.1.1 -- -sV -sC", "description": "Port scan with Nmap service detection and scripts.", "Author": ""},
    {"command": "rustscan -a targets.txt -p 80,443,22,21", "description": "Scan specific ports on targets from file.", "Author": ""},
]

COMMON_RUSTYHOG_COMMANDS = [
    {"command": "rustyhog_s3 -r us-west-2 -k secrets.txt", "description": "Search for secrets in S3 buckets.", "Author": ""},
    {"command": "rustyhog_git -u https://github.com/user/repo", "description": "Search for secrets in Git repository.", "Author": ""},
    {"command": "rustyhog_slack -t xoxb-token", "description": "Search for secrets in Slack workspace.", "Author": ""},
]

COMMON_S3SCANNER_COMMANDS = [
    {"command": "s3scanner scan -f bucket-names.txt", "description": "Scan S3 bucket names from file.", "Author": ""},
    {"command": "s3scanner dump -f found-buckets.txt", "description": "Dump contents of found S3 buckets.", "Author": ""},
    {"command": "s3scanner scan -n bucket-name", "description": "Scan specific S3 bucket name.", "Author": ""},
]

COMMON_SECRETLINT_COMMANDS = [
    {"command": "secretlint .", "description": "Scan current directory for secrets.", "Author": ""},
    {"command": "secretlint --format json file.js", "description": "Scan specific file with JSON output.", "Author": ""},
    {"command": "secretlint --secretlintrc .secretlintrc.json .", "description": "Use custom configuration file for scanning.", "Author": ""},
]

COMMON_SHUFFLEDNS_COMMANDS = [
    {"command": "shuffledns -d example.com -list subdomains.txt", "description": "DNS resolution using subdomain list.", "Author": ""},
    {"command": "shuffledns -d example.com -w wordlist.txt", "description": "DNS brute forcing with wordlist.", "Author": ""},
    {"command": "shuffledns -d example.com -list subdomains.txt -r resolvers.txt", "description": "Use custom DNS resolvers for resolution.", "Author": ""},
]

COMMON_SQLMAP_COMMANDS = [
    {"command": "sqlmap -u 'http://example.com/page.php?id=1'", "description": "Basic SQL injection testing on URL parameter.", "Author": ""},
    {"command": "sqlmap -u 'http://example.com/page.php?id=1' --dbs", "description": "Enumerate databases if injection found.", "Author": ""},
    {"command": "sqlmap -r request.txt", "description": "Test SQL injection using HTTP request file.", "Author": ""},
    {"command": "sqlmap -u 'http://example.com/page.php?id=1' --dump -D database_name -T table_name", "description": "Dump specific table from database.", "Author": ""},
]

COMMON_SUBJS_COMMANDS = [
    {"command": "subjs -i urls.txt", "description": "Extract JavaScript files from URLs.", "Author": ""},
    {"command": "subjs -i urls.txt -o js-files.txt", "description": "Save extracted JavaScript URLs to file.", "Author": ""},
    {"command": "subjs -u http://example.com", "description": "Extract JS files from single URL.", "Author": ""},
]

COMMON_SUBZY_COMMANDS = [
    {"command": "subzy -targets subdomains.txt", "description": "Check subdomains for subdomain takeover vulnerabilities.", "Author": ""},
    {"command": "subzy -target subdomain.example.com", "description": "Check single subdomain for takeover vulnerability.", "Author": ""},
    {"command": "subzy -targets subdomains.txt -concurrency 10", "description": "Check with custom concurrency level.", "Author": ""},
]

COMMON_TRUFFLEHOG_COMMANDS = [
    {"command": "trufflehog https://github.com/user/repo.git", "description": "Scan Git repository for secrets.", "Author": ""},
    {"command": "trufflehog filesystem /path/to/directory", "description": "Scan local filesystem directory for secrets.", "Author": ""},
    {"command": "trufflehog --json https://github.com/user/repo.git", "description": "Output results in JSON format.", "Author": ""},
    {"command": "trufflehog --only-verified https://github.com/user/repo.git", "description": "Show only verified secrets.", "Author": ""},
]

COMMON_WAYBACKURLS_COMMANDS = [
    {"command": "waybackurls example.com", "description": "Fetch URLs for domain from Wayback Machine.", "Author": ""},
    {"command": "waybackurls example.com | grep -E '\\.(js|php|asp|jsp)$'", "description": "Filter for specific file types from archived URLs.", "Author": ""},
    {"command": "waybackurls example.com > wayback-urls.txt", "description": "Save Wayback URLs to output file.", "Author": ""},
]

COMMON_WAYMORE_COMMANDS = [
    {"command": "waymore -i example.com", "description": "Fetch URLs and responses from web archives.", "Author": ""},
    {"command": "waymore -i example.com -mode U", "description": "Fetch only URLs (not responses).", "Author": ""},
    {"command": "waymore -i example.com -f js,php", "description": "Filter for specific file types.", "Author": ""},
    {"command": "waymore -i example.com -o waymore-results", "description": "Save results to specified directory.", "Author": ""},
]

COMMON_WFUZZ_COMMANDS = [
    {"command": "wfuzz -c -z file,/usr/share/wordlists/dirb/common.txt --hc 404 http://example.com/FUZZ", "description": "Basic directory fuzzing hiding 404 responses.", "Author": ""},
    {"command": "wfuzz -c -z file,/usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt http://example.com/index.php?FUZZ=test", "description": "Parameter name fuzzing.", "Author": ""},
    {"command": "wfuzz -c -z file,wordlist.txt -H 'Host: FUZZ.example.com' http://example.com/", "description": "Virtual host discovery using Host header.", "Author": ""},
    {"command": "wfuzz -c -z file,usernames.txt -z file,passwords.txt --hc 401 http://example.com/login.php -d 'username=FUZZ&password=FUZ2Z'", "description": "Login brute forcing with username and password lists.", "Author": ""},
]

COMMON_XNLINKFINDER_COMMANDS = [
    {"command": "xnLinkFinder -i urls.txt", "description": "Extract links from URLs in file.", "Author": ""},
    {"command": "xnLinkFinder -i urls.txt -sf subdomains.txt", "description": "Extract links and filter by subdomains.", "Author": ""},
    {"command": "xnLinkFinder -i urls.txt -o extracted-links.txt", "description": "Save extracted links to output file.", "Author": ""},
]

COMMON_XSSER_COMMANDS = [
    {"command": "xsser --url 'http://example.com/search.php?q=XSS'", "description": "Basic XSS testing on URL parameter.", "Author": ""},
    {"command": "xsser --url 'http://example.com/search.php?q=XSS' --auto", "description": "Automatic XSS testing with various payloads.", "Author": ""},
    {"command": "xsser -i targets.txt --threads=10", "description": "Test multiple targets with threading.", "Author": ""},
]

COMMON_XSSTRIKE_COMMANDS = [
    {"command": "xsstrike.py -u 'http://example.com/search.php?q=test'", "description": "Basic XSS testing on URL parameter.", "Author": ""},
    {"command": "xsstrike.py -u 'http://example.com/search.php?q=test' --crawl", "description": "Crawl target and test found parameters.", "Author":""},
]

# Load environment variables
print("Attempting to load .env file...")
success = load_dotenv()
print(f".env loading successful: {success}")

api_key = os.environ.get("GOOGLE_API_KEY")
model_name = os.environ.get("GEMINI_MODEL_NAME")
print(f"Value of GOOGLE_API_KEY: {api_key}")
print(f"Value of GEMINI_MODEL_NAME: {model_name}")

# Configuration checks
is_ready_to_configure = True
model = None

if not api_key:
    print(f"{Fore.RED}Error: GOOGLE_API_KEY environment variable not set.{Style.RESET_ALL}")
    is_ready_to_configure = False
else:
    print(f"{Fore.GREEN}API Key successfully loaded.{Style.RESET_ALL}")

if not model_name:
    print(f"{Fore.RED}Error: GEMINI_MODEL_NAME environment variable not set.{Style.RESET_ALL}")
    is_ready_to_configure = False
else:
    print(f"{Fore.GREEN}Gemini model name '{model_name}' successfully loaded.{Style.RESET_ALL}")

# Configure Gemini API
if is_ready_to_configure:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        print(f"{Fore.GREEN}Gemini model '{model_name}' configured successfully.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error configuring Gemini API: {e}{Style.RESET_ALL}")
        model = None

if model is None:
    print(f"{Fore.RED}Script cannot proceed without Gemini model configuration.{Style.RESET_ALL}")
    exit(1)

# Helper functions
def extract_command_from_markdown(text):
    match = re.search(r"```(?:\w+)?\n(.*?)\n```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def clean_assistance_output(text):
    cleaned_text = re.sub(r"```(?:\w+)?\n(.*?)\n```", r"\1", text, flags=re.DOTALL)
    cleaned_text = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned_text)
    cleaned_text = re.sub(r"\*(.*?)\*", r"\1", cleaned_text)
    cleaned_text = re.sub(r"_(.*?)_", r"\1", cleaned_text)
    cleaned_text = re.sub(r"`(.*?)`", r"\1", cleaned_text)
    return cleaned_text.strip()

def assist_with_output(command, user_question):
    prompt_text = f"""
You are a concise assistant specializing in command-line tools.
Command: {command}
User's Question: {user_question}
Provide a short answer about the command's output or flags. Use Linux commands if needed. Avoid markdown formatting.
"""
    try:
        response = model.generate_content(prompt_text)
        return clean_assistance_output(response.text.strip())
    except Exception as e:
        return f"{Fore.RED}Error communicating with Gemini API: {e}{Style.RESET_ALL}"

def generate_command(tool, user_question, manual):
    try:
        prompt_template = PROMPT_TEMPLATES.get(tool)
        if not prompt_template:
            return f"{Fore.RED}Error: No prompt template defined for {tool} in config.py{Style.RESET_ALL}", ""
        
        prompt_text = prompt_template.format(manual=manual, user_question=user_question, tool=tool)
        try:
            response = model.generate_content(prompt_text)
            raw_response_text = response.text.strip()
            command = extract_command_from_markdown(raw_response_text)
            if command.startswith(tool):
                return command, raw_response_text
            elif f"Question is not related to {tool} manual" in raw_response_text:
                return raw_response_text, raw_response_text
            else:
                return f"{Fore.RED}Error: Invalid {tool} command generated:\n{raw_response_text}{Style.RESET_ALL}", raw_response_text
        except Exception as e:
            return f"{Fore.RED}Error communicating with Gemini API: {e}{Style.RESET_ALL}", str(e)
    except KeyError:
        return f"{Fore.RED}Error: No prompt template defined for {tool} in config.py{Style.RESET_ALL}", ""

def display_common_commands(commands, tool_name):
    print(f"\n{Fore.GREEN}Commonly Used {tool_name} Commands:{Style.RESET_ALL}\n")
    for cmd_info in commands:
        print(f"Command: {cmd_info['command']}")
        print(f"Description: {cmd_info['description']}")
        print("-" * 20)
    print("-------------------------------------------\n")
    print("Press Enter to return...")
    input()

# Tool classifications
TOOL_CATEGORIES = {
    "Reconnaissance": ["subfinder", "amass", "dnsx", "shuffledns", "puredns"],
    "Port Scanning": ["naabu", "masscan", "rustscan"],
    "Web Crawling": ["katana", "hakrawler", "gau", "waybackurls", "waymore"],
    "Directory Discovery": ["dirsearch", "ffuf", "feroxbuster", "dirbuster", "rustbuster", "wfuzz"],
    "Parameter Discovery": ["arjun", "paramspider"],
    "XSS Testing": ["bxss", "loxs", "xsstrike", "xsser"],
    "HTTP Probing": ["httprobe", "httpx"],
    "Screenshots": ["eyewitness", "gowitness"],
    "JavaScript Analysis": ["getjs", "subjs", "xnlinkfinder"],
    "Secret Detection": ["trufflehog", "gitsecrets", "rustyhog", "secretlint"],
    "Git Analysis": ["gitgrabber", "githound"],
    "SQL Injection": ["sqlmap"],
    "Vulnerability Testing": ["openredirex", "oralyzer", "nomore403", "subzy"],
    "Cloud Security": ["s3scanner"],
    "Bypass Techniques": ["nomore403"]
}

# Common commands mapping
COMMON_COMMANDS = {
    'subfinder': COMMON_SUBFINDER_COMMANDS,
    'naabu': COMMON_NAABU_COMMANDS,
    'katana': COMMON_KATANA_COMMANDS,
    'dirsearch': COMMON_DIRSEARCH_COMMANDS,
    'ffuf': COMMON_FFUF_COMMANDS,
    'amass': COMMON_AMASS_COMMANDS,
    'arjun': COMMON_ARJUN_COMMANDS,
    'bxss': COMMON_BXSS_COMMANDS,
    'dirbuster': COMMON_DIRBUSTER_COMMANDS,
    'dnsx': COMMON_DNSX_COMMANDS,
    'eyewitness': COMMON_EYEWITNESS_COMMANDS,
    'feroxbuster': COMMON_FEROXBUSTER_COMMANDS,
    'gau': COMMON_GAU_COMMANDS,
    'getjs': COMMON_GETJS_COMMANDS,
    'gitgrabber': COMMON_GITGRABBER_COMMANDS,
    'githound': COMMON_GITHOUND_COMMANDS,
    'gitsecrets': COMMON_GITSECRETS_COMMANDS,
    'gowitness': COMMON_GOWITNESS_COMMANDS,
    'hakrawler': COMMON_HAKRAWLER_COMMANDS,
    'httprobe': COMMON_HTTPROBE_COMMANDS,
    'httpx': COMMON_HTTPX_COMMANDS,
    'loxs': COMMON_LOXS_COMMANDS,
    'masscan': COMMON_MASSCAN_COMMANDS,
    'nomore403': COMMON_NOMORE403_COMMANDS,
    'openredirex': COMMON_OPENREDIREX_COMMANDS,
    'oralyzer': COMMON_ORALYZER_COMMANDS,
    'paramspider': COMMON_P9RAMSPIDER_COMMANDS,
    'puredns': COMMON_PUREDNS_COMMANDS,
    'rustbuster': COMMON_RU6TBUSTER_COMMANDS,
    'rustscan': COMMON_RUSTSCAN_COMMANDS,
    'rustyhog': COMMON_RUSTYHOG_COMMANDS,
    's3scanner': COMMON_S3SCANNER_COMMANDS,
    'secretlint': COMMON_SECRETLINT_COMMANDS,
    'shuffledns': COMMON_SHUFFLEDNS_COMMANDS,
    'sqlmap': COMMON_SQLMAP_COMMANDS,
    'subjs': COMMON_SUBJS_COMMANDS,
    'subzy': COMMON_SUBZY_COMMANDS,
    'trufflehog': COMMON_TRUFFLEHOG_COMMANDS,
    'waybackurls': COMMON_WAYBACKURLS_COMMANDS,
    'waymore': COMMON_WAYMORE_COMMANDS,
    'wfuzz': COMMON_WFUZZ_COMMANDS,
    'xnlinkfinder': COMMON_XNLINKFINDER_COMMANDS,
    'xsser': COMMON_XSSER_COMMANDS,
    'xsstrike': COMMON_XSSTRIKE_COMMANDS
}

# Main menu
if __name__ == "__main__":
    while True:
        print(f"\n{Fore.CYAN}Choose a Functionality (Classification):{Style.RESET_ALL}")
        for idx, category in enumerate(TOOL_CATEGORIES.keys(), 1):
            print(f"{Fore.CYAN}{idx}. {category}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}0. Exit{Style.RESET_ALL}")

        try:
            choice = input("Enter your choice (0 or 1-15): ")
            if choice == '0':
                print("Exiting...")
                break

            category_idx = int(choice) - 1
            if category_idx < 0 or category_idx >= len(TOOL_CATEGORIES):
                print(f"{Fore.RED}Invalid choice. Please select a valid option.{Style.RESET_ALL}")
                continue

            category = list(TOOL_CATEGORIES.keys())[category_idx]
            tools = TOOL_CATEGORIES[category]

            while True:
                print(f"\n{Fore.CYAN}Tools in {category}:{Style.RESET_ALL}")
                for idx, tool in enumerate(tools, 1):
                    print(f"{Fore.CYAN}{idx}. {tool.capitalize()}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}0. Back to Classification Menu{Style.RESET_ALL}")

                tool_choice = input("Select a tool (0 or 1-{}): ".format(len(tools)))
                if tool_choice == '0':
                    break

                try:
                    tool_idx = int(tool_choice) - 1
                    if tool_idx < 0 or tool_idx >= len(tools):
                        print(f"{Fore.RED}Invalid tool choice. Please select a valid tool.{Style.RESET_ALL}")
                        continue

                    tool = tools[tool_idx]
                    while True:
                        print(f"\n{Fore.GREEN}Options for {tool.capitalize()}:{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}1. Generate {tool.capitalize()} Command{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}2. View Commonly Used {tool.capitalize()} Commands{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}0. Back to {category} Tools{Style.RESET_ALL}")

                        action_choice = input("Choose an action (0-2): ")
                        if action_choice == '0':
                            break
                        elif action_choice == '1':
                            while True:
                                user_input = input(f"Ask a question about {tool.capitalize()} command (or type 'back' to return):\n> ")
                                if user_input.lower() == 'back':
                                    break
                                command, raw_response = generate_command(tool, user_input, MANUALS[tool])
                                print(f"\n{tool.capitalize()} Command:\n{command}\n")
                                print("-------------------------------------------\n")
                                continue_choice = input(f"Generate another {tool.capitalize()} command (y), ask about output (que), or return (back)? (y/que/back): ").lower()
                                if continue_choice == 'que':
                                    output_question = input("What is your question about the command's output?\n> ")
                                    assistance = assist_with_output(command, output_question)
                                    print(f"\nAssistance:\n{assistance}\n")
                                    print("-------------------------------------------\n")
                                    continue
                                elif continue_choice == 'back':
                                    break
                                elif continue_choice == 'y':
                                    continue
                                else:
                                    print(f"{Fore.YELLOW}Invalid choice. Returning to tool options.{Style.RESET_ALL}")
                                    break
                        elif action_choice == '2':
                            display_common_commands(COMMON_COMMANDS[tool], tool.capitalize())
                        else:
                            print(f"{Fore.RED}Invalid action. Please select 0, 1, or 2.{Style.RESET_ALL}")

                except ValueError:
                    print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")

        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")

colorama.deinit()
