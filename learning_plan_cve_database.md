# Learning Plan: Building Your Own CVE Database Empire
## *Or: How to Become the Paranoid Security Oracle Your Company Needs*

> "Why rely on other people's vulnerability databases when you can build your own and add features like 'CVE Horoscope' and 'Vulnerability Speed Dating'?" - Developer who got tired of API rate limits

Welcome to the world where you become the master of all vulnerabilities, the keeper of CVEs, the one who knows when Log4j is about to ruin everyone's weekend. By the end of this journey, you'll have built a personal CVE database that makes security vendors nervous and your DevOps team actually grateful.

## The Problem We're Solving
### *Why Build Your Own When NIST Exists?*

**The Current Reality** (aka "The Pain"):
- NIST NVD rate limits: 5 requests per 30 seconds (or 10 if you beg for an API key)
- Different databases have different data: Snyk knows npm, GitHub knows Go, nobody knows everything
- Enrichment data scattered across 47 different sources
- Your security tools cost more than your car
- Half the CVE descriptions read like they were written by lawyers having a bad day

**Your Future Reality** (aka "The Gain"):
- Unlimited queries against YOUR database
- All sources unified in one beautiful schema
- Custom enrichment with whatever matters to YOU
- Build tools that would cost $10k/month from vendors
- CVE descriptions rewritten by your personal AI to actually make sense

**Real Talk**: When the next Log4Shell drops, you'll know about it from 7 different sources, have the full exploitation timeline, affected version ranges, and a pre-written email to your boss explaining why the weekend is cancelled.

## Feasibility Analysis
### *Can One Person Really Do This? (Spoiler: Yes, But...)*

Let's do some **real math** instead of hand-waving:

### Storage Requirements (The Truth Edition)

```python
# Let's calculate this properly
import json

class CVEStorageCalculator:
    """
    Calculates real storage requirements.
    No marketing BS, just facts.
    """
    
    def __init__(self):
        # Current CVE statistics (as of 2024)
        self.total_cves = 220000  # Approximate total CVEs
        self.new_cves_per_year = 25000  # Growing every year
        
        # Average sizes (from actual data)
        self.base_cve_size = 2048  # 2KB for basic CVE data
        self.enrichment_multiplier = 10  # Enriched data is ~10x larger
        
    def calculate_storage(self, years=5):
        """Calculate storage for X years of operation."""
        
        # Initial load
        initial_size = self.total_cves * self.base_cve_size
        initial_enriched = self.total_cves * self.base_cve_size * self.enrichment_multiplier
        
        # Growth over time
        growth_size = 0
        growth_enriched = 0
        
        for year in range(years):
            yearly_cves = self.new_cves_per_year * (1.1 ** year)  # 10% growth
            growth_size += yearly_cves * self.base_cve_size
            growth_enriched += yearly_cves * self.base_cve_size * self.enrichment_multiplier
        
        # Add indexes, metadata, etc (30% overhead)
        overhead = 1.3
        
        total_basic = (initial_size + growth_size) * overhead
        total_enriched = (initial_enriched + growth_enriched) * overhead
        
        return {
            'initial_basic_gb': initial_size / (1024**3),
            'initial_enriched_gb': initial_enriched / (1024**3),
            'total_basic_gb': total_basic / (1024**3),
            'total_enriched_gb': total_enriched / (1024**3),
            'daily_update_mb': (self.new_cves_per_year / 365) * self.base_cve_size * self.enrichment_multiplier / (1024**2)
        }

calc = CVEStorageCalculator()
storage = calc.calculate_storage(5)

print(f"Initial load (basic): {storage['initial_basic_gb']:.1f} GB")
print(f"Initial load (enriched): {storage['initial_enriched_gb']:.1f} GB")
print(f"After 5 years (basic): {storage['total_basic_gb']:.1f} GB")
print(f"After 5 years (enriched): {storage['total_enriched_gb']:.1f} GB")
print(f"Daily update size: {storage['daily_update_mb']:.1f} MB")
```

**The Reality Check**:
- Initial load: ~4.3 GB (enriched)
- After 5 years: ~11 GB (enriched)
- Daily updates: ~1.7 MB
- **Verdict**: Your laptop's SSD laughs at these numbers

### Resource Requirements (The "Will It Run on a Potato?" Test)

```yaml
# Minimum viable infrastructure
development:
  cpu: 2 cores
  ram: 4 GB
  disk: 50 GB SSD
  cost: $0 (your laptop)
  
production:
  cpu: 4 cores
  ram: 8 GB
  disk: 100 GB SSD
  bandwidth: 100 GB/month
  cost: $20-40/month (Hetzner/DigitalOcean)
  
enterprise_flex:
  cpu: 8 cores
  ram: 32 GB
  disk: 500 GB NVMe
  cost: $100/month
  capabilities: "Can handle your entire company's paranoia"
```

### Legal Considerations (The "Will I Get Sued?" Section)

**Good News**: All these sources provide public data meant to be consumed!

**Fine Print That Matters**:
- NIST NVD: Public domain, but respect rate limits
- OSV: Apache 2.0 license, free to use
- Snyk: Free tier available, respect API limits
- Wiz.io: Public access, no API required
- VulDB: Free tier with attribution
- CISA KEV: US Government work = public domain
- GitHub vulnrichment: Open source, MIT license

**The One Rule**: Don't be a jerk. Respect rate limits, attribute sources, and don't resell public data as your own.

## Architecture Design
### *Building Something That Won't Embarrass You in 6 Months*

```mermaid
graph TB
    subgraph "Data Sources"
        NIST[NIST NVD API]
        OSV[OSV.dev API]
        SNYK[Snyk API]
        WIZ[Wiz.io Scraper]
        VULDB[VulDB API]
        CISA[CISA KEV API]
        GITHUB[GitHub Vulnrichment]
    end
    
    subgraph "Ingestion Layer"
        SCHEDULER[Celery Beat Scheduler]
        WORKERS[Celery Workers]
        QUEUE[Redis Queue]
    end
    
    subgraph "Processing Layer"
        NORM[Data Normalizer]
        ENRICH[Enrichment Engine]
        DEDUP[Deduplication Service]
    end
    
    subgraph "Storage Layer"
        PG[(PostgreSQL)]
        REDIS[(Redis Cache)]
        S3[S3/MinIO]
    end
    
    subgraph "API Layer"
        FASTAPI[FastAPI]
        GRAPHQL[GraphQL]
        WEBHOOK[Webhook Service]
    end
    
    subgraph "Frontend"
        DASH[Dashboard]
        CLI[CLI Tool]
        SLACK[Slack Bot]
    end
    
    NIST --> WORKERS
    OSV --> WORKERS
    SNYK --> WORKERS
    WIZ --> WORKERS
    VULDB --> WORKERS
    CISA --> WORKERS
    GITHUB --> WORKERS
    
    SCHEDULER --> QUEUE
    QUEUE --> WORKERS
    WORKERS --> NORM
    NORM --> ENRICH
    ENRICH --> DEDUP
    DEDUP --> PG
    DEDUP --> REDIS
    
    PG --> FASTAPI
    REDIS --> FASTAPI
    FASTAPI --> DASH
    FASTAPI --> CLI
    FASTAPI --> SLACK
    FASTAPI --> WEBHOOK
```

### The Secret Sauce: Smart Synchronization

```python
class SmartCVEScheduler:
    """
    Staggers updates across sources to avoid thundering herd.
    Because we're not barbarians.
    """
    
    def __init__(self):
        self.sources = [
            {
                'name': 'NIST_NVD',
                'interval': '0 */4 * * *',  # Every 4 hours
                'priority': 1,
                'rate_limit': '10/minute'
            },
            {
                'name': 'OSV',
                'interval': '30 */4 * * *',  # Every 4 hours, offset by 30 min
                'priority': 2,
                'rate_limit': '100/minute'
            },
            {
                'name': 'SNYK',
                'interval': '0 */6 * * *',  # Every 6 hours
                'priority': 3,
                'rate_limit': '60/minute'
            },
            {
                'name': 'CISA_KEV',
                'interval': '0 8,20 * * *',  # Twice daily
                'priority': 1,
                'rate_limit': None  # No limit on government data
            },
            {
                'name': 'WIZ_IO',
                'interval': '0 2 * * *',  # Daily at 2 AM
                'priority': 4,
                'rate_limit': '5/minute'  # Be nice to their servers
            }
        ]
```

## Implementation Guide
### *From "pip install hope" to "Holy Crap, It Works!"*

### Phase 1: Database Schema That Doesn't Suck

```python
# schema.py - The foundation of your empire
from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, Text, Float, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
import uuid
from datetime import datetime

Base = declarative_base()

class CVE(Base):
    """
    The master CVE record.
    Like a Pokemon card, but for vulnerabilities.
    """
    __tablename__ = 'cves'
    
    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cve_id = Column(String(20), unique=True, nullable=False, index=True)  # CVE-2021-44228
    
    # Basic metadata
    published_date = Column(DateTime, nullable=False)
    last_modified = Column(DateTime, nullable=False)
    
    # Descriptions (because one is never enough)
    description = Column(Text)  # Original description
    description_enhanced = Column(Text)  # AI-improved description
    title = Column(String(500))  # Human-friendly title
    
    # Scoring (the numbers that make managers panic)
    cvss_v2_score = Column(Float)
    cvss_v3_score = Column(Float)
    cvss_v3_vector = Column(String(100))
    epss_score = Column(Float)  # Exploit Prediction Scoring System
    severity = Column(String(20))  # LOW, MEDIUM, HIGH, CRITICAL
    
    # Classification
    cwe_ids = Column(ARRAY(String))  # Weakness types
    attack_vector = Column(String(20))  # NETWORK, LOCAL, etc
    
    # Affected products (the actual useful part)
    affected_products = Column(JSONB)  # CPE strings and version ranges
    
    # Sources and references
    sources = Column(JSONB)  # Which databases have this CVE
    references = Column(JSONB)  # URLs, advisories, etc
    
    # Enrichment data
    exploits = Column(JSONB)  # Known exploits
    patches = Column(JSONB)  # Available patches
    mitigations = Column(JSONB)  # Temporary fixes
    
    # Status flags
    is_disputed = Column(Boolean, default=False)
    is_rejected = Column(Boolean, default=False)
    is_kev = Column(Boolean, default=False)  # Is in CISA KEV?
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Performance indexes
    __table_args__ = (
        Index('idx_cvss_v3_score', 'cvss_v3_score'),
        Index('idx_published_date', 'published_date'),
        Index('idx_severity', 'severity'),
        Index('idx_is_kev', 'is_kev'),
        Index('idx_affected_products', 'affected_products', postgresql_using='gin'),
    )

class CVESource(Base):
    """
    Track where each piece of data came from.
    For when you need to blame someone.
    """
    __tablename__ = 'cve_sources'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cve_id = Column(String(20), nullable=False, index=True)
    source = Column(String(50), nullable=False)  # NIST, OSV, SNYK, etc
    
    # Source-specific data
    source_data = Column(JSONB)  # Original data from source
    source_url = Column(Text)
    
    # Tracking
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)
    update_count = Column(Integer, default=1)
    
    # Quality metrics
    data_quality_score = Column(Float)  # How complete/accurate is this source?
    
    __table_args__ = (
        Index('idx_cve_source', 'cve_id', 'source', unique=True),
    )

class ExploitInfo(Base):
    """
    The scary stuff that keeps CISOs awake.
    """
    __tablename__ = 'exploits'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cve_id = Column(String(20), nullable=False, index=True)
    
    # Exploit details
    exploit_type = Column(String(50))  # RCE, DOS, INFO_DISCLOSURE, etc
    exploit_name = Column(String(200))
    exploit_url = Column(Text)
    
    # Availability
    is_public = Column(Boolean, default=False)
    is_weaponized = Column(Boolean, default=False)
    is_in_the_wild = Column(Boolean, default=False)
    
    # Metadata
    discovered_date = Column(DateTime)
    disclosure_date = Column(DateTime)
    
    # PoC information
    poc_available = Column(Boolean, default=False)
    poc_url = Column(Text)
    poc_language = Column(String(50))  # Python, Metasploit, etc
    
    # Threat intelligence
    threat_actors = Column(ARRAY(String))
    campaigns = Column(ARRAY(String))
    
    created_at = Column(DateTime, default=datetime.utcnow)

# Create the tables
engine = create_engine('postgresql://cve_user:secure_password@localhost/cve_db')
Base.metadata.create_all(engine)

print("Database schema created! Your empire begins...")
```

### Phase 2: Data Ingestion Pipeline (The Fun Part)

```python
# ingestors/base.py - The foundation for all data sources
import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import logging
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

class BaseIngestor(ABC):
    """
    Base class for all CVE data ingestors.
    Like a vacuum cleaner, but for vulnerabilities.
    """
    
    def __init__(self, source_name: str, rate_limit: int = 10):
        self.source_name = source_name
        self.rate_limit = rate_limit
        self.logger = logging.getLogger(f"ingestor.{source_name}")
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(rate_limit)
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch(self, url: str, **kwargs) -> Dict:
        """
        Fetch data with retries and rate limiting.
        Because the internet is unreliable.
        """
        async with self.semaphore:
            self.logger.debug(f"Fetching: {url}")
            async with self.session.get(url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
    
    @abstractmethod
    async def get_cve_list(self, since: datetime) -> List[str]:
        """Get list of CVEs updated since given date."""
        pass
    
    @abstractmethod
    async def get_cve_details(self, cve_id: str) -> Dict:
        """Get detailed information for a specific CVE."""
        pass
    
    def normalize_cve_data(self, raw_data: Dict) -> Dict:
        """
        Convert source-specific format to our standard.
        Like Google Translate, but for vulnerabilities.
        """
        # Override in subclasses
        return raw_data

# ingestors/nist.py - NIST NVD Ingestor
class NISTIngestor(BaseIngestor):
    """
    Ingest from NIST NVD - The OG of CVE databases.
    Slow but authoritative, like a government website.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("NIST_NVD", rate_limit=10 if api_key else 5)
        self.api_key = api_key
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        
    async def get_cve_list(self, since: datetime) -> List[str]:
        """
        Get CVEs modified since date.
        Warning: This might take a while. Get coffee.
        """
        cve_ids = []
        start_index = 0
        results_per_page = 2000  # Max allowed
        
        while True:
            params = {
                'lastModStartDate': since.isoformat(),
                'lastModEndDate': datetime.utcnow().isoformat(),
                'startIndex': start_index,
                'resultsPerPage': results_per_page
            }
            
            if self.api_key:
                params['apiKey'] = self.api_key
            
            data = await self.fetch(self.base_url, params=params)
            
            vulnerabilities = data.get('vulnerabilities', [])
            if not vulnerabilities:
                break
                
            for vuln in vulnerabilities:
                cve_ids.append(vuln['cve']['id'])
            
            start_index += results_per_page
            
            # Check if we've got all results
            if start_index >= data.get('totalResults', 0):
                break
            
            # Be nice to NIST servers
            await asyncio.sleep(6 if not self.api_key else 0.6)
        
        return cve_ids
    
    async def get_cve_details(self, cve_id: str) -> Dict:
        """Get the full CVE details from NIST."""
        params = {'cveId': cve_id}
        if self.api_key:
            params['apiKey'] = self.api_key
            
        data = await self.fetch(self.base_url, params=params)
        
        if data.get('vulnerabilities'):
            return self.normalize_cve_data(data['vulnerabilities'][0])
        
        return {}
    
    def normalize_cve_data(self, raw_data: Dict) -> Dict:
        """Convert NIST format to our schema."""
        cve = raw_data.get('cve', {})
        
        # Extract CVSS scores
        metrics = cve.get('metrics', {})
        cvss_v3 = metrics.get('cvssMetricV31', [{}])[0].get('cvssData', {})
        cvss_v2 = metrics.get('cvssMetricV2', [{}])[0].get('cvssData', {})
        
        # Extract affected products (CPEs)
        affected_products = []
        for config in cve.get('configurations', []):
            for node in config.get('nodes', []):
                for cpe_match in node.get('cpeMatch', []):
                    if cpe_match.get('vulnerable'):
                        affected_products.append({
                            'cpe': cpe_match.get('criteria'),
                            'versionStart': cpe_match.get('versionStartIncluding'),
                            'versionEnd': cpe_match.get('versionEndIncluding')
                        })
        
        return {
            'cve_id': cve.get('id'),
            'published_date': cve.get('published'),
            'last_modified': cve.get('lastModified'),
            'description': cve.get('descriptions', [{}])[0].get('value', ''),
            'cvss_v3_score': cvss_v3.get('baseScore'),
            'cvss_v3_vector': cvss_v3.get('vectorString'),
            'cvss_v2_score': cvss_v2.get('baseScore'),
            'severity': cvss_v3.get('baseSeverity', 'UNKNOWN'),
            'affected_products': affected_products,
            'references': [ref.get('url') for ref in cve.get('references', [])],
            'cwe_ids': [w.get('value') for w in cve.get('weaknesses', [])]
        }

# ingestors/osv.py - OSV.dev Ingestor
class OSVIngestor(BaseIngestor):
    """
    OSV.dev - Google's gift to the security world.
    Fast, comprehensive, and actually has a good API.
    """
    
    def __init__(self):
        super().__init__("OSV", rate_limit=100)  # They're generous
        self.base_url = "https://api.osv.dev/v1"
        
    async def get_cve_list(self, since: datetime) -> List[str]:
        """
        OSV doesn't have a great "list by date" API,
        so we'll be creative.
        """
        # For OSV, we'll query by ecosystem and filter
        ecosystems = ['PyPI', 'npm', 'Go', 'crates.io', 'RubyGems', 'Maven']
        cve_ids = set()
        
        for ecosystem in ecosystems:
            try:
                # Query recent vulnerabilities
                data = await self.fetch(
                    f"{self.base_url}/query",
                    json={'package': {'ecosystem': ecosystem}}
                )
                
                for vuln in data.get('vulns', []):
                    # Extract CVE IDs from aliases
                    for alias in vuln.get('aliases', []):
                        if alias.startswith('CVE-'):
                            cve_ids.add(alias)
                            
            except Exception as e:
                self.logger.error(f"Error querying {ecosystem}: {e}")
                
        return list(cve_ids)
    
    async def get_cve_details(self, cve_id: str) -> Dict:
        """Get CVE details from OSV."""
        try:
            data = await self.fetch(
                f"{self.base_url}/vulns/{cve_id}"
            )
            return self.normalize_cve_data(data)
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                # OSV might not have this CVE
                return {}
            raise
    
    def normalize_cve_data(self, raw_data: Dict) -> Dict:
        """Convert OSV format to our schema."""
        # Extract affected packages
        affected_products = []
        for affected in raw_data.get('affected', []):
            package = affected.get('package', {})
            affected_products.append({
                'ecosystem': package.get('ecosystem'),
                'name': package.get('name'),
                'versions': affected.get('versions', []),
                'ranges': affected.get('ranges', [])
            })
        
        # Find CVE ID in aliases
        cve_id = None
        for alias in raw_data.get('aliases', []):
            if alias.startswith('CVE-'):
                cve_id = alias
                break
                
        return {
            'cve_id': cve_id or raw_data.get('id'),
            'published_date': raw_data.get('published'),
            'last_modified': raw_data.get('modified'),
            'description': raw_data.get('summary', ''),
            'severity': raw_data.get('database_specific', {}).get('severity', 'UNKNOWN'),
            'affected_products': affected_products,
            'references': [ref.get('url') for ref in raw_data.get('references', [])],
            'source_specific': {
                'osv_id': raw_data.get('id'),
                'ecosystem_specific': raw_data.get('ecosystem_specific', {})
            }
        }

# orchestrator.py - The conductor of this symphony
import asyncio
from typing import List, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from celery import Celery

app = Celery('cve_collector', broker='redis://localhost:6379')

class CVEOrchestrator:
    """
    Coordinates all the ingestors like a maestro.
    Except instead of music, it's vulnerabilities.
    """
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.ingestors = {
            'NIST': NISTIngestor(api_key=os.environ.get('NIST_API_KEY')),
            'OSV': OSVIngestor(),
            # Add more ingestors here
        }
        
    async def sync_all_sources(self, since: datetime = None):
        """
        Sync from all sources.
        Like a vulnerability buffet.
        """
        if since is None:
            # Default to last 24 hours
            since = datetime.utcnow() - timedelta(days=1)
            
        results = {
            'total_cves': 0,
            'new_cves': 0,
            'updated_cves': 0,
            'errors': []
        }
        
        for source_name, ingestor in self.ingestors.items():
            try:
                async with ingestor:
                    self.logger.info(f"Starting sync from {source_name}")
                    
                    # Get list of CVEs
                    cve_ids = await ingestor.get_cve_list(since)
                    self.logger.info(f"Found {len(cve_ids)} CVEs from {source_name}")
                    
                    # Process in batches
                    batch_size = 50
                    for i in range(0, len(cve_ids), batch_size):
                        batch = cve_ids[i:i + batch_size]
                        await self.process_cve_batch(batch, source_name, ingestor)
                        
                    results['total_cves'] += len(cve_ids)
                    
            except Exception as e:
                self.logger.error(f"Error syncing {source_name}: {e}")
                results['errors'].append({
                    'source': source_name,
                    'error': str(e)
                })
                
        return results
    
    async def process_cve_batch(self, cve_ids: List[str], source: str, ingestor: BaseIngestor):
        """Process a batch of CVEs concurrently."""
        tasks = []
        for cve_id in cve_ids:
            task = self.process_single_cve(cve_id, source, ingestor)
            tasks.append(task)
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle results
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Error processing CVE: {result}")

@app.task
def sync_source(source_name: str):
    """Celery task to sync a single source."""
    asyncio.run(_sync_source_async(source_name))

async def _sync_source_async(source_name: str):
    """Async implementation of source sync."""
    orchestrator = CVEOrchestrator(get_db_session())
    await orchestrator.sync_single_source(source_name)

# Schedule periodic syncs
from celery.schedules import crontab

app.conf.beat_schedule = {
    'sync-nist': {
        'task': 'sync_source',
        'schedule': crontab(minute='0', hour='*/4'),  # Every 4 hours
        'args': ('NIST',)
    },
    'sync-osv': {
        'task': 'sync_source',
        'schedule': crontab(minute='30', hour='*/4'),  # Every 4 hours, offset
        'args': ('OSV',)
    },
    # Add more scheduled tasks
}
```

### Phase 3: The API Layer (Where the Magic Happens)

```python
# api/main.py - FastAPI application
from fastapi import FastAPI, Query, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import redis
from pydantic import BaseModel, Field
import json

app = FastAPI(
    title="Personal CVE Database API",
    description="Your own vulnerability intelligence platform. Like MITRE, but with personality.",
    version="1.0.0"
)

# Redis for caching and rate limiting
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Pydantic models
class CVEResponse(BaseModel):
    cve_id: str
    title: Optional[str]
    description: str
    severity: str
    cvss_v3_score: Optional[float]
    published_date: datetime
    affected_products: List[Dict]
    is_kev: bool = False
    exploit_available: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "cve_id": "CVE-2021-44228",
                "title": "Log4Shell - Apache Log4j RCE",
                "description": "The one that ruined everyone's December",
                "severity": "CRITICAL",
                "cvss_v3_score": 10.0,
                "published_date": "2021-12-10T00:00:00",
                "affected_products": [{"name": "log4j", "versions": ["2.0-2.14.1"]}],
                "is_kev": True,
                "exploit_available": True
            }
        }

class CVESearchRequest(BaseModel):
    keyword: Optional[str] = Field(None, description="Search in description and products")
    severity: Optional[List[str]] = Field(None, description="Filter by severity levels")
    min_cvss: Optional[float] = Field(None, ge=0, le=10)
    published_after: Optional[datetime] = None
    published_before: Optional[datetime] = None
    has_exploit: Optional[bool] = None
    is_kev: Optional[bool] = None
    affected_product: Optional[str] = None
    limit: int = Field(100, ge=1, le=1000)
    offset: int = Field(0, ge=0)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=JSONResponse)
async def root():
    """Welcome to your personal CVE empire."""
    return {
        "message": "Welcome to your Personal CVE Database",
        "stats": await get_database_stats(),
        "endpoints": {
            "search": "/api/v1/cves/search",
            "get_cve": "/api/v1/cves/{cve_id}",
            "stream": "/api/v1/stream",
            "webhook": "/api/v1/webhooks",
            "stats": "/api/v1/stats"
        }
    }

@app.get("/api/v1/cves/{cve_id}", response_model=CVEResponse)
async def get_cve(cve_id: str, db: Session = Depends(get_db)):
    """
    Get details for a specific CVE.
    Cached because we're not savages.
    """
    # Check cache first
    cached = redis_client.get(f"cve:{cve_id}")
    if cached:
        return json.loads(cached)
    
    # Query database
    cve = db.query(CVE).filter(CVE.cve_id == cve_id).first()
    if not cve:
        raise HTTPException(status_code=404, detail=f"CVE {cve_id} not found")
    
    # Convert to response model
    response = CVEResponse(
        cve_id=cve.cve_id,
        title=cve.title,
        description=cve.description_enhanced or cve.description,
        severity=cve.severity,
        cvss_v3_score=cve.cvss_v3_score,
        published_date=cve.published_date,
        affected_products=cve.affected_products or [],
        is_kev=cve.is_kev,
        exploit_available=bool(cve.exploits)
    )
    
    # Cache for 1 hour
    redis_client.setex(
        f"cve:{cve_id}", 
        3600, 
        response.json()
    )
    
    return response

@app.post("/api/v1/cves/search", response_model=List[CVEResponse])
async def search_cves(
    request: CVESearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search CVEs with multiple filters.
    More powerful than a regex in a haystack.
    """
    query = db.query(CVE)
    
    # Apply filters
    if request.keyword:
        search_term = f"%{request.keyword}%"
        query = query.filter(
            (CVE.description.ilike(search_term)) |
            (CVE.title.ilike(search_term)) |
            (CVE.cve_id.ilike(search_term))
        )
    
    if request.severity:
        query = query.filter(CVE.severity.in_(request.severity))
    
    if request.min_cvss is not None:
        query = query.filter(CVE.cvss_v3_score >= request.min_cvss)
    
    if request.published_after:
        query = query.filter(CVE.published_date >= request.published_after)
    
    if request.published_before:
        query = query.filter(CVE.published_date <= request.published_before)
    
    if request.has_exploit is not None:
        if request.has_exploit:
            query = query.filter(CVE.exploits.isnot(None))
        else:
            query = query.filter(CVE.exploits.is_(None))
    
    if request.is_kev is not None:
        query = query.filter(CVE.is_kev == request.is_kev)
    
    if request.affected_product:
        # JSONB query for affected products
        query = query.filter(
            CVE.affected_products.contains([{
                'name': request.affected_product
            }])
        )
    
    # Order by severity and date
    query = query.order_by(CVE.published_date.desc())
    
    # Pagination
    total = query.count()
    results = query.offset(request.offset).limit(request.limit).all()
    
    # Convert to response models
    return [
        CVEResponse(
            cve_id=cve.cve_id,
            title=cve.title,
            description=cve.description_enhanced or cve.description,
            severity=cve.severity,
            cvss_v3_score=cve.cvss_v3_score,
            published_date=cve.published_date,
            affected_products=cve.affected_products or [],
            is_kev=cve.is_kev,
            exploit_available=bool(cve.exploits)
        )
        for cve in results
    ]

@app.get("/api/v1/stream")
async def stream_cves():
    """
    Real-time CVE stream via Server-Sent Events.
    Like Twitter, but for vulnerabilities.
    """
    async def event_generator():
        # Subscribe to Redis pub/sub
        pubsub = redis_client.pubsub()
        pubsub.subscribe('cve_updates')
        
        try:
            while True:
                message = pubsub.get_message(timeout=1.0)
                if message and message['type'] == 'message':
                    yield f"data: {message['data']}\n\n"
                else:
                    # Send heartbeat
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
                
                await asyncio.sleep(0.1)
                
        except asyncio.CancelledError:
            pubsub.unsubscribe('cve_updates')
            pubsub.close()
            raise
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/api/v1/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Database statistics and insights.
    Numbers to impress your boss.
    """
    stats = {
        'total_cves': db.query(CVE).count(),
        'critical_cves': db.query(CVE).filter(CVE.severity == 'CRITICAL').count(),
        'cves_with_exploits': db.query(CVE).filter(CVE.exploits.isnot(None)).count(),
        'kev_cves': db.query(CVE).filter(CVE.is_kev == True).count(),
        'last_update': db.query(CVE).order_by(CVE.updated_at.desc()).first().updated_at,
        'top_cwe': db.query(CVE.cwe_ids, func.count(CVE.id)).group_by(CVE.cwe_ids).order_by(func.count(CVE.id).desc()).limit(10).all(),
        'severity_breakdown': {
            'CRITICAL': db.query(CVE).filter(CVE.severity == 'CRITICAL').count(),
            'HIGH': db.query(CVE).filter(CVE.severity == 'HIGH').count(),
            'MEDIUM': db.query(CVE).filter(CVE.severity == 'MEDIUM').count(),
            'LOW': db.query(CVE).filter(CVE.severity == 'LOW').count(),
        }
    }
    
    return stats

# Webhook support for integrations
class WebhookConfig(BaseModel):
    url: str
    events: List[str] = ['new_cve', 'exploit_available', 'kev_addition']
    severity_filter: Optional[List[str]] = None
    product_filter: Optional[List[str]] = None

@app.post("/api/v1/webhooks")
async def create_webhook(config: WebhookConfig, background_tasks: BackgroundTasks):
    """
    Register a webhook for CVE notifications.
    Because manually checking for vulnerabilities is so 2010.
    """
    webhook_id = str(uuid.uuid4())
    
    # Store webhook config
    redis_client.hset(
        'webhooks',
        webhook_id,
        json.dumps(config.dict())
    )
    
    return {
        'webhook_id': webhook_id,
        'status': 'active',
        'config': config
    }
```

## Creative Tool Ideas
### *The Fun Part Where We Get Weird*

### Tool 1: CVE Horoscope 🔮
*"What vulnerabilities does the universe have in store for you today?"*

```python
# tools/cve_horoscope.py
import random
from datetime import datetime, timedelta
from typing import List, Dict

class CVEHoroscope:
    """
    Predicts your vulnerability future based on your tech stack.
    100% accurate 0% of the time.
    """
    
    def __init__(self, db_session):
        self.db = db_session
        self.zodiac_stacks = {
            'Aries': ['Spring', 'React', 'MongoDB'],  # Likes to move fast and break things
            'Taurus': ['Django', 'PostgreSQL', 'nginx'],  # Stable and reliable
            'Gemini': ['Node.js', 'GraphQL', 'Redis'],  # Can't decide on one technology
            'Cancer': ['PHP', 'MySQL', 'Apache'],  # Nostalgic for the old days
            'Leo': ['Kubernetes', 'Istio', 'Prometheus'],  # Loves complexity
            'Virgo': ['Rust', 'SQLite', 'HAProxy'],  # Perfectionist
            'Libra': ['Rails', 'Vue.js', 'Elasticsearch'],  # Seeks balance
            'Scorpio': ['Go', 'Kafka', 'Cassandra'],  # Intense and powerful
            'Sagittarius': ['Elixir', 'Phoenix', 'CockroachDB'],  # Adventurous
            'Capricorn': ['Java', 'Oracle', 'WebLogic'],  # Enterprise minded
            'Aquarius': ['Deno', 'SurrealDB', 'Fly.io'],  # Ahead of their time
            'Pisces': ['Python', 'Docker', 'anything'],  # Goes with the flow
        }
        
        self.fortune_templates = [
            "A critical vulnerability in {product} will test your patience today. Deploy patches wisely.",
            "The stars align for a zero-day in {product}. Your logs will reveal the truth.",
            "Mercury in retrograde suggests avoiding {product} updates until next week.",
            "Your {product} installation attracts positive energy. And also CVE-{year}-{number}.",
            "Today's cosmic energy favors penetration testing your {product} deployment.",
            "Venus enters your security sector. Romance is in the air, but so is CVE-{year}-{number}.",
            "Your ruling planet suggests implementing WAF rules for {product} immediately.",
            "The universe whispers: 'Check your {product} version.' Trust the universe.",
            "Abundance flows to those who patch {product} before the weekend.",
            "Your security karma improves by helping others understand CVE-{year}-{number}."
        ]
    
    def get_sign_for_stack(self, tech_stack: List[str]) -> str:
        """Determine zodiac sign based on tech stack."""
        # This is definitely how astrology works
        stack_hash = sum(ord(c) for tech in tech_stack for c in tech)
        signs = list(self.zodiac_stacks.keys())
        return signs[stack_hash % len(signs)]
    
    def generate_horoscope(self, user_stack: List[str]) -> Dict:
        """
        Generate a personalized vulnerability horoscope.
        May contain traces of actual vulnerabilities.
        """
        sign = self.get_sign_for_stack(user_stack)
        
        # Get recent CVEs for user's stack
        relevant_cves = []
        for product in user_stack:
            cves = self.db.query(CVE).filter(
                CVE.affected_products.contains([{'name': product.lower()}])
            ).order_by(CVE.published_date.desc()).limit(5).all()
            relevant_cves.extend(cves)
        
        # Pick a fortune template
        fortune = random.choice(self.fortune_templates)
        
        # Fill in the fortune
        if relevant_cves:
            cve = random.choice(relevant_cves)
            fortune = fortune.format(
                product=random.choice(user_stack),
                year=cve.cve_id.split('-')[1],
                number=cve.cve_id.split('-')[2]
            )
        else:
            # Make up a plausible CVE number
            fortune = fortune.format(
                product=random.choice(user_stack),
                year=datetime.now().year,
                number=random.randint(10000, 30000)
            )
        
        # Generate lucky numbers (CVSS scores to watch for)
        lucky_scores = sorted([round(random.uniform(4.0, 9.9), 1) for _ in range(3)])
        
        # Generate daily advice
        advice = self._generate_advice(sign, user_stack, relevant_cves)
        
        return {
            'date': datetime.now().date().isoformat(),
            'sign': sign,
            'fortune': fortune,
            'lucky_cvss_scores': lucky_scores,
            'advice': advice,
            'compatibility': self._get_compatibility(sign),
            'mood': random.choice(['Paranoid', 'Cautiously Optimistic', 'Patch Happy', 'Zero Trust']),
            'color_of_the_day': random.choice(['Red Team Red', 'Blue Team Blue', 'Patch Tuesday Purple'])
        }
    
    def _generate_advice(self, sign: str, stack: List[str], cves: List[CVE]) -> str:
        """Generate sign-specific security advice."""
        advice_templates = {
            'Aries': "Your impulsive nature may lead to skipping security headers. Slow down.",
            'Taurus': "Your resistance to change is admirable, but those dependencies need updating.",
            'Gemini': "Your dual nature sees both the feature and the vulnerability. Choose wisely.",
            'Cancer': "Your emotional attachment to legacy code creates vulnerabilities. Let go.",
            'Leo': "Your confidence is great, but even kings need Web Application Firewalls.",
            'Virgo': "Your attention to detail will catch that SQL injection others missed.",
            'Libra': "Seeking balance between features and security? Today, security wins.",
            'Scorpio': "Your suspicious nature serves you well. That third-party library IS sketchy.",
            'Sagittarius': "Your adventurous deployments need more testing. Try staging first.",
            'Capricorn': "Your conservative approach pays off. That rushed patch has issues.",
            'Aquarius': "Your innovative solutions are great, but please document them.",
            'Pisces': "Your intuition says something's wrong with production. Trust it."
        }
        
        return advice_templates.get(sign, "The stars are unclear. Try sudo rm -rf /var/log/*")
    
    def _get_compatibility(self, sign: str) -> Dict:
        """Which tech stacks are you compatible with today?"""
        compatible = random.sample(list(self.zodiac_stacks.keys()), 3)
        return {
            'most_compatible': compatible[0],
            'their_stack': self.zodiac_stacks[compatible[0]],
            'compatibility_score': random.randint(70, 95),
            'warning': f"Avoid pair programming with {compatible[-1]} today"
        }

# API endpoint for horoscope
@app.get("/api/v1/horoscope")
async def get_cve_horoscope(
    tech_stack: List[str] = Query(..., description="Your technology stack"),
    db: Session = Depends(get_db)
):
    """
    Get your daily CVE horoscope.
    More accurate than your actual horoscope.
    """
    horoscope = CVEHoroscope(db)
    return horoscope.generate_horoscope(tech_stack)
```

### Tool 2: Vulnerability Genealogy 🌳
*"Track the family tree of vulnerabilities"*

```python
# tools/vuln_genealogy.py
from typing import Dict, List, Set
import networkx as nx
from collections import defaultdict

class VulnerabilityGenealogy:
    """
    Traces the ancestry and descendants of vulnerabilities.
    Like 23andMe, but for security flaws.
    """
    
    def __init__(self, db_session):
        self.db = db_session
        self.family_patterns = {
            'SQL Injection Dynasty': ['CWE-89', 'CWE-564', 'CWE-20'],
            'Buffer Overflow Bloodline': ['CWE-120', 'CWE-121', 'CWE-122'],
            'XSS Clan': ['CWE-79', 'CWE-80', 'CWE-81'],
            'Deserialization Dynasty': ['CWE-502', 'CWE-915'],
            'Authentication Aristocracy': ['CWE-287', 'CWE-306', 'CWE-307']
        }
        
    def build_family_tree(self, cve_id: str) -> Dict:
        """
        Build the complete family tree for a CVE.
        Warning: Some families have issues.
        """
        # Get the CVE
        root_cve = self.db.query(CVE).filter(CVE.cve_id == cve_id).first()
        if not root_cve:
            return {'error': 'CVE not found. Perhaps it was adopted?'}
        
        # Create the family tree
        tree = nx.DiGraph()
        tree.add_node(cve_id, data=self._get_cve_personality(root_cve))
        
        # Find ancestors (older similar vulnerabilities)
        ancestors = self._find_ancestors(root_cve)
        for ancestor in ancestors:
            tree.add_node(ancestor['cve_id'], data=ancestor)
            tree.add_edge(ancestor['cve_id'], cve_id, relation='parent')
        
        # Find siblings (same CWE, similar time)
        siblings = self._find_siblings(root_cve)
        for sibling in siblings:
            tree.add_node(sibling['cve_id'], data=sibling)
            tree.add_edge(cve_id, sibling['cve_id'], relation='sibling')
        
        # Find descendants (newer similar vulnerabilities)
        descendants = self._find_descendants(root_cve)
        for desc in descendants:
            tree.add_node(desc['cve_id'], data=desc)
            tree.add_edge(cve_id, desc['cve_id'], relation='child')
        
        # Find cousins (related through shared techniques)
        cousins = self._find_cousins(root_cve)
        for cousin in cousins:
            tree.add_node(cousin['cve_id'], data=cousin)
            tree.add_edge(cve_id, cousin['cve_id'], relation='cousin')
        
        # Generate family analysis
        analysis = self._analyze_family(tree, root_cve)
        
        return {
            'cve_id': cve_id,
            'family_name': self._get_family_name(root_cve),
            'family_motto': self._generate_family_motto(root_cve),
            'family_tree': self._tree_to_dict(tree),
            'family_traits': self._get_family_traits(tree),
            'black_sheep': self._find_black_sheep(tree),
            'family_reunion_risk': analysis['reunion_risk'],
            'inheritance': analysis['inheritance'],
            'family_drama': self._generate_drama(tree)
        }
    
    def _get_cve_personality(self, cve: CVE) -> Dict:
        """Assign personality traits to a CVE."""
        personalities = {
            'CRITICAL': {
                'temperament': 'Explosive',
                'hobby': 'Ruining weekends',
                'favorite_food': 'RAM',
                'life_goal': 'Make it to CNN'
            },
            'HIGH': {
                'temperament': 'Aggressive',
                'hobby': 'Keeping security teams busy',
                'favorite_food': 'CPU cycles',
                'life_goal': 'Get a logo and catchy name'
            },
            'MEDIUM': {
                'temperament': 'Passive-aggressive',
                'hobby': 'Being ignored until audit time',
                'favorite_food': 'Log files',
                'life_goal': 'Maybe get patched someday'
            },
            'LOW': {
                'temperament': 'Laid back',
                'hobby': 'Collecting dust in backlogs',
                'favorite_food': 'Disk space',
                'life_goal': 'Just happy to be included'
            }
        }
        
        return personalities.get(cve.severity, personalities['LOW'])
    
    def _find_ancestors(self, cve: CVE) -> List[Dict]:
        """Find older vulnerabilities that led to this one."""
        ancestors = []
        
        # Look for same CWE, older CVEs
        if cve.cwe_ids:
            older_cves = self.db.query(CVE).filter(
                CVE.cwe_ids.overlap(cve.cwe_ids),
                CVE.published_date < cve.published_date
            ).order_by(CVE.published_date.desc()).limit(5).all()
            
            for ancestor in older_cves:
                ancestors.append({
                    'cve_id': ancestor.cve_id,
                    'age': (cve.published_date - ancestor.published_date).days,
                    'relation_strength': self._calculate_similarity(cve, ancestor)
                })
        
        return ancestors
    
    def _find_siblings(self, cve: CVE) -> List[Dict]:
        """Find vulnerabilities from the same batch/family."""
        siblings = []
        
        # Same product, similar time window
        time_window = timedelta(days=30)
        similar_cves = self.db.query(CVE).filter(
            CVE.cve_id != cve.cve_id,
            CVE.published_date.between(
                cve.published_date - time_window,
                cve.published_date + time_window
            ),
            CVE.affected_products.overlap(cve.affected_products)
        ).limit(10).all()
        
        for sibling in similar_cves:
            siblings.append({
                'cve_id': sibling.cve_id,
                'rivalry_score': abs(sibling.cvss_v3_score - cve.cvss_v3_score) if sibling.cvss_v3_score else 0,
                'favorite_child': sibling.cvss_v3_score > cve.cvss_v3_score if sibling.cvss_v3_score else False
            })
        
        return siblings
    
    def _generate_family_motto(self, cve: CVE) -> str:
        """Generate a family motto based on vulnerability type."""
        mottos = {
            'CWE-89': "'; DROP TABLE security;--",
            'CWE-79': "<script>alert('Family Pride')</script>",
            'CWE-120': "Buffer overflow, stack overflow, family overflow",
            'CWE-287': "Authentication is optional in this family",
            'CWE-502': "We put the 'serial' in 'serial killer'",
            'CWE-22': "../../../etc/passwd is home",
            'CWE-78': "; rm -rf /",
            'CWE-94': "eval() is just family bonding time"
        }
        
        if cve.cwe_ids:
            return mottos.get(cve.cwe_ids[0], "Vulnerabilities run in the family")
        return "We put the 'fun' in 'fundamental design flaw'"
    
    def _generate_drama(self, tree: nx.DiGraph) -> List[str]:
        """Generate family drama narratives."""
        drama_templates = [
            "{cve1} never forgave {cve2} for getting more media attention",
            "{cve1} claims {cve2} stole their exploitation technique",
            "The family doesn't talk about {cve1} anymore after the incident",
            "{cve1} and {cve2} compete for who can crash systems faster",
            "Rumor has it {cve1} isn't actually related - just similar looking",
            "{cve1} was disowned after getting a CVE score downgrade"
        ]
        
        nodes = list(tree.nodes())
        if len(nodes) < 2:
            return ["This CVE is an only child. How sad."]
        
        drama = []
        for _ in range(min(3, len(nodes) // 2)):
            template = random.choice(drama_templates)
            cve1, cve2 = random.sample(nodes, 2)
            drama.append(template.format(cve1=cve1, cve2=cve2))
        
        return drama
```

### Tool 3: Patch Roulette 🎰
*"Gamify your patch management decisions"*

```python
# tools/patch_roulette.py
import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class PatchRoulette:
    """
    Turn patch decisions into a game of chance.
    DISCLAIMER: Don't actually use this for real decisions.
    Or do. I'm not your compliance officer.
    """
    
    def __init__(self, db_session):
        self.db = db_session
        self.wheel_sections = {
            'PATCH_NOW': {'color': 'red', 'multiplier': 0, 'sound': '🚨'},
            'PATCH_TONIGHT': {'color': 'orange', 'multiplier': 0.5, 'sound': '⏰'},
            'PATCH_THIS_WEEK': {'color': 'yellow', 'multiplier': 1, 'sound': '📅'},
            'PATCH_NEXT_SPRINT': {'color': 'green', 'multiplier': 2, 'sound': '🏃'},
            'RISK_ACCEPTED': {'color': 'blue', 'multiplier': 5, 'sound': '🎲'},
            'YOLO': {'color': 'purple', 'multiplier': 10, 'sound': '🚀'},
            'BANKRUPTCY': {'color': 'black', 'multiplier': -100, 'sound': '💀'}
        }
        
    def spin_the_wheel(self, cve_list: List[str]) -> Dict:
        """
        Spin the wheel of patch fortune.
        May the odds be ever in your favor.
        """
        results = {
            'timestamp': datetime.utcnow(),
            'total_cves': len(cve_list),
            'decisions': [],
            'risk_score': 0,
            'estimated_downtime': 0,
            'excitement_level': 0,
            'recommended_coffee_cups': 0
        }
        
        for cve_id in cve_list:
            cve = self.db.query(CVE).filter(CVE.cve_id == cve_id).first()
            if not cve:
                continue
            
            # Calculate spin probability based on severity
            spin_result = self._calculate_spin(cve)
            
            # Calculate consequences
            consequences = self._calculate_consequences(cve, spin_result['section'])
            
            decision = {
                'cve_id': cve_id,
                'severity': cve.severity,
                'spin_result': spin_result,
                'consequences': consequences,
                'fortune_cookie': self._generate_fortune(cve, spin_result['section'])
            }
            
            results['decisions'].append(decision)
            results['risk_score'] += consequences['risk_points']
            results['estimated_downtime'] += consequences['downtime_minutes']
            results['excitement_level'] += consequences['adrenaline_rush']
        
        # Calculate final scores
        results['recommended_coffee_cups'] = math.ceil(results['excitement_level'] / 10)
        results['survival_probability'] = self._calculate_survival_probability(results)
        results['achievement_unlocked'] = self._check_achievements(results)
        results['leaderboard_position'] = self._calculate_leaderboard_position(results)
        
        return results
    
    def _calculate_spin(self, cve: CVE) -> Dict:
        """
        Calculate where the wheel lands based on CVE properties.
        Totally not rigged. *wink*
        """
        # Base probabilities
        if cve.severity == 'CRITICAL':
            weights = {
                'PATCH_NOW': 60,
                'PATCH_TONIGHT': 25,
                'PATCH_THIS_WEEK': 10,
                'PATCH_NEXT_SPRINT': 3,
                'RISK_ACCEPTED': 1,
                'YOLO': 0.5,
                'BANKRUPTCY': 0.5
            }
        elif cve.severity == 'HIGH':
            weights = {
                'PATCH_NOW': 30,
                'PATCH_TONIGHT': 35,
                'PATCH_THIS_WEEK': 20,
                'PATCH_NEXT_SPRINT': 10,
                'RISK_ACCEPTED': 3,
                'YOLO': 1,
                'BANKRUPTCY': 1
            }
        elif cve.severity == 'MEDIUM':
            weights = {
                'PATCH_NOW': 10,
                'PATCH_TONIGHT': 20,
                'PATCH_THIS_WEEK': 35,
                'PATCH_NEXT_SPRINT': 25,
                'RISK_ACCEPTED': 7,
                'YOLO': 2,
                'BANKRUPTCY': 1
            }
        else:  # LOW
            weights = {
                'PATCH_NOW': 2,
                'PATCH_TONIGHT': 8,
                'PATCH_THIS_WEEK': 20,
                'PATCH_NEXT_SPRINT': 40,
                'RISK_ACCEPTED': 20,
                'YOLO': 8,
                'BANKRUPTCY': 2
            }
        
        # Modify weights based on additional factors
        if cve.is_kev:
            weights['PATCH_NOW'] *= 2
            weights['BANKRUPTCY'] *= 3
        
        if cve.exploits:
            weights['PATCH_NOW'] *= 1.5
            weights['YOLO'] *= 0.5
        
        # Normalize weights
        total = sum(weights.values())
        probabilities = {k: v/total for k, v in weights.items()}
        
        # Spin!
        spin_value = random.random()
        cumulative = 0
        
        for section, prob in probabilities.items():
            cumulative += prob
            if spin_value <= cumulative:
                return {
                    'section': section,
                    'details': self.wheel_sections[section],
                    'spin_value': spin_value,
                    'dramatic_pause': random.uniform(2, 5)  # Seconds to build suspense
                }
        
        # Fallback (shouldn't happen)
        return {
            'section': 'BANKRUPTCY',
            'details': self.wheel_sections['BANKRUPTCY'],
            'spin_value': spin_value,
            'dramatic_pause': 10
        }
    
    def _calculate_consequences(self, cve: CVE, decision: str) -> Dict:
        """Calculate the consequences of your patching decision."""
        base_risk = {
            'CRITICAL': 1000,
            'HIGH': 500,
            'MEDIUM': 100,
            'LOW': 10
        }.get(cve.severity, 10)
        
        multiplier = self.wheel_sections[decision]['multiplier']
        
        consequences = {
            'risk_points': base_risk * abs(multiplier) if multiplier > 0 else base_risk * 100,
            'downtime_minutes': 0,
            'adrenaline_rush': 0,
            'karma_points': 0
        }
        
        # Calculate based on decision
        if decision == 'PATCH_NOW':
            consequences['downtime_minutes'] = random.randint(30, 120)
            consequences['adrenaline_rush'] = 50
            consequences['karma_points'] = 100
        elif decision == 'PATCH_TONIGHT':
            consequences['downtime_minutes'] = random.randint(20, 60)
            consequences['adrenaline_rush'] = 30
            consequences['karma_points'] = 75
        elif decision == 'PATCH_THIS_WEEK':
            consequences['downtime_minutes'] = random.randint(15, 45)
            consequences['adrenaline_rush'] = 20
            consequences['karma_points'] = 50
        elif decision == 'PATCH_NEXT_SPRINT':
            consequences['downtime_minutes'] = random.randint(10, 30)
            consequences['adrenaline_rush'] = 10
            consequences['karma_points'] = 25
        elif decision == 'RISK_ACCEPTED':
            consequences['downtime_minutes'] = 0
            consequences['adrenaline_rush'] = 60
            consequences['karma_points'] = -25
        elif decision == 'YOLO':
            consequences['downtime_minutes'] = 0
            consequences['adrenaline_rush'] = 100
            consequences['karma_points'] = -50
        elif decision == 'BANKRUPTCY':
            consequences['downtime_minutes'] = 9999
            consequences['adrenaline_rush'] = 200
            consequences['karma_points'] = -1000
        
        return consequences
    
    def _generate_fortune(self, cve: CVE, decision: str) -> str:
        """Generate a fortune cookie message for the decision."""
        fortunes = {
            'PATCH_NOW': [
                "Your future holds many grateful users and peaceful nights.",
                "A patched server is a happy server.",
                "The security gods smile upon your swift action."
            ],
            'PATCH_TONIGHT': [
                "Midnight oil burns brightest when patching critical flaws.",
                "Your dedication will be remembered... by the logs.",
                "Coffee is your friend, sleep is overrated."
            ],
            'PATCH_THIS_WEEK': [
                "Procrastination today, penetration tomorrow.",
                "A journey of a thousand patches begins with a single ticket.",
                "Your faith in weekday patching will be tested."
            ],
            'PATCH_NEXT_SPRINT': [
                "The sprint that never ends provides patches that never land.",
                "Your backlog grows heavy with the weight of decisions.",
                "Agile methodology meets immovable vulnerabilities."
            ],
            'RISK_ACCEPTED': [
                "You have chosen... poorly. But confidently!",
                "Risk acceptance forms must be signed in triplicate.",
                "Your risk register gains another distinguished entry."
            ],
            'YOLO': [
                "You only live once, but your servers die frequently.",
                "Fortune favors the bold. Attackers favor the unpatched.",
                "Your name will echo through incident reports."
            ],
            'BANKRUPTCY': [
                "Press F to pay respects to your infrastructure.",
                "Your resume update begins now.",
                "Sometimes the house wins. This is that time."
            ]
        }
        
        return random.choice(fortunes.get(decision, ["The wheel has spoken."]))
    
    def _check_achievements(self, results: Dict) -> List[Dict]:
        """Check if any achievements were unlocked."""
        achievements = []
        
        # Check various achievement conditions
        if results['risk_score'] > 10000:
            achievements.append({
                'name': 'Living Dangerously',
                'description': 'Accumulated over 10,000 risk points',
                'emoji': '🔥'
            })
        
        if results['recommended_coffee_cups'] > 20:
            achievements.append({
                'name': 'Caffeine Immunity',
                'description': 'Required more than 20 cups of coffee',
                'emoji': '☕'
            })
        
        bankruptcy_count = sum(1 for d in results['decisions'] if d['spin_result']['section'] == 'BANKRUPTCY')
        if bankruptcy_count > 0:
            achievements.append({
                'name': 'Bankruptcy Speedrun',
                'description': 'Hit bankruptcy on the wheel',
                'emoji': '📉'
            })
        
        yolo_count = sum(1 for d in results['decisions'] if d['spin_result']['section'] == 'YOLO')
        if yolo_count >= 3:
            achievements.append({
                'name': 'YOLO Master',
                'description': 'Chose YOLO 3 or more times',
                'emoji': '🚀'
            })
        
        if all(d['spin_result']['section'] == 'PATCH_NOW' for d in results['decisions']):
            achievements.append({
                'name': 'Security Saint',
                'description': 'Patched everything immediately',
                'emoji': '😇'
            })
        
        return achievements

# API endpoint
@app.post("/api/v1/patch-roulette")
async def play_patch_roulette(
    cve_ids: List[str],
    db: Session = Depends(get_db)
):
    """
    Play Patch Roulette with your CVEs.
    Not financial advice. Or security advice. Or any kind of advice.
    """
    roulette = PatchRoulette(db)
    return roulette.spin_the_wheel(cve_ids)
```

### Tool 4: CVE Dating App 💕
*"Match vulnerabilities with their perfect exploits"*

```python
# tools/cve_dating.py
class CVEDatingApp:
    """
    Swipe right on vulnerabilities.
    Finally, a dating app for security researchers.
    """
    
    def __init__(self, db_session):
        self.db = db_session
        self.personality_types = {
            'RCE': {
                'bio': "Loves long walks through memory and executing arbitrary code",
                'looking_for': "Someone who appreciates unrestricted access",
                'turn_ons': ["No input validation", "Unsafe deserialization", "eval()"],
                'turn_offs': ["Sandboxing", "DEP", "ASLR"]
            },
            'SQLi': {
                'bio': "'; DROP TABLE inhibitions;--",
                'looking_for': "A database that doesn't ask too many questions",
                'turn_ons': ["String concatenation", "Dynamic queries", "Trust"],
                'turn_offs': ["Prepared statements", "Input sanitization", "ORMs"]
            },
            'XSS': {
                'bio': "<script>alert('Looking for love')</script>",
                'looking_for': "Someone who renders me without judgment",
                'turn_ons': ["innerHTML", "document.write", "No CSP"],
                'turn_offs': ["HTML encoding", "Content Security Policy", "React"]
            }
        }
    
    def create_dating_profile(self, cve_id: str) -> Dict:
        """Create a dating profile for a CVE."""
        cve = self.db.query(CVE).filter(CVE.cve_id == cve_id).first()
        if not cve:
            return {'error': 'CVE not found. Maybe they deleted their profile?'}
        
        profile = {
            'name': cve.cve_id,
            'age': (datetime.now() - cve.published_date).days,
            'severity': cve.severity,
            'bio': self._generate_bio(cve),
            'interests': cve.cwe_ids or ['Causing chaos'],
            'ideal_first_date': self._generate_date_idea(cve),
            'red_flags': self._identify_red_flags(cve),
            'anthem': self._pick_anthem(cve),
            'looking_for': self._what_theyre_looking_for(cve),
            'photos': self._generate_photos(cve)  # ASCII art representations
        }
        
        return profile
    
    def find_matches(self, cve_id: str) -> List[Dict]:
        """Find compatible exploits for a CVE."""
        cve = self.db.query(CVE).filter(CVE.cve_id == cve_id).first()
        if not cve:
            return []
        
        # Find exploits that match
        exploits = self.db.query(ExploitInfo).filter(
            ExploitInfo.cve_id == cve_id
        ).all()
        
        matches = []
        for exploit in exploits:
            compatibility = self._calculate_compatibility(cve, exploit)
            matches.append({
                'exploit_name': exploit.exploit_name or 'Mystery Exploit',
                'compatibility_score': compatibility,
                'conversation_starter': self._generate_pickup_line(cve, exploit),
                'warning_signs': self._check_warning_signs(exploit),
                'first_message': self._generate_first_message(cve, exploit)
            })
        
        return sorted(matches, key=lambda x: x['compatibility_score'], reverse=True)
```

## Data Enrichment Strategies
### *Making Your CVE Data Thicc*

```python
# enrichment/enricher.py
class CVEEnricher:
    """
    Adds context, meaning, and sass to raw CVE data.
    Like makeup, but for vulnerabilities.
    """
    
    def __init__(self):
        self.enrichment_sources = {
            'exploit_availability': self._check_exploit_sources,
            'affected_versions': self._parse_version_ranges,
            'threat_intelligence': self._gather_threat_intel,
            'patch_information': self._find_patches,
            'real_world_impact': self._assess_impact,
            'ai_description': self._enhance_description,
            'meme_potential': self._calculate_meme_score
        }
    
    async def enrich_cve(self, cve: CVE) -> Dict:
        """Enrich a CVE with additional context."""
        enrichments = {}
        
        for enrichment_type, enrichment_func in self.enrichment_sources.items():
            try:
                result = await enrichment_func(cve)
                enrichments[enrichment_type] = result
            except Exception as e:
                self.logger.error(f"Enrichment {enrichment_type} failed: {e}")
                enrichments[enrichment_type] = None
        
        return enrichments
    
    async def _enhance_description(self, cve: CVE) -> str:
        """
        Use AI to rewrite CVE descriptions in plain English.
        Because "The product does not properly..." gets old.
        """
        # This would integrate with OpenAI/Claude API
        prompt = f"""
        Rewrite this CVE description to be clear and understandable:
        {cve.description}
        
        Include:
        1. What the vulnerability is (in plain English)
        2. How it can be exploited
        3. What the impact is
        4. Who should care
        
        Keep it under 200 words and maybe add a tiny bit of personality.
        """
        
        # Placeholder for AI integration
        enhanced = f"TL;DR: {cve.cve_id} lets bad guys do bad things to your {cve.affected_products[0] if cve.affected_products else 'systems'}. Patch it before someone discovers your server's deepest secrets."
        
        return enhanced
    
    def _calculate_meme_score(self, cve: CVE) -> Dict:
        """
        Calculate how memeable a vulnerability is.
        For research purposes only.
        """
        score = 0
        factors = []
        
        # Check for meme potential
        if 'log4j' in str(cve.affected_products).lower():
            score += 100
            factors.append("Log4j automatically equals memes")
        
        if cve.cvss_v3_score == 10.0:
            score += 50
            factors.append("Perfect 10 score")
        
        if 'wordpress' in str(cve.affected_products).lower():
            score += 30
            factors.append("WordPress gonna WordPress")
        
        if any(word in cve.description.lower() for word in ['trivial', 'easily', 'simple']):
            score += 40
            factors.append("Embarrassingly simple exploit")
        
        # Check if it has a cool name
        if cve.title and len(cve.title.split()) <= 2:
            score += 25
            factors.append("Has a catchy name")
        
        return {
            'meme_score': min(score, 100),
            'factors': factors,
            'suggested_meme_template': self._suggest_meme_template(score)
        }
```

## Running Your Empire
### *From Zero to CVE Hero*

### Development Setup

```bash
# Clone and setup
git clone https://github.com/you/cve-empire.git
cd cve-empire

# Environment setup
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Setup databases
docker-compose up -d postgres redis

# Initialize database
python scripts/init_db.py

# Run initial sync (grab coffee, this takes a while)
python scripts/initial_sync.py

# Start the API
uvicorn api.main:app --reload

# Start the task worker
celery -A orchestrator worker --loglevel=info

# Start the scheduler
celery -A orchestrator beat --loglevel=info
```

### Production Deployment

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: cve_db
      POSTGRES_USER: cve_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  redis:
    image: redis:7-alpine
    restart: always

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://cve_user:${DB_PASSWORD}@postgres/cve_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: always

  worker:
    build: .
    command: celery -A orchestrator worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://cve_user:${DB_PASSWORD}@postgres/cve_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: always

  scheduler:
    build: .
    command: celery -A orchestrator beat --loglevel=info
    environment:
      DATABASE_URL: postgresql://cve_user:${DB_PASSWORD}@postgres/cve_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - api
    restart: always

volumes:
  postgres_data:
```

## Maintenance and Operations
### *Keeping Your Empire Running*

```python
# scripts/health_check.py
class CVESystemHealth:
    """
    Monitor the health of your CVE empire.
    Because even empires need checkups.
    """
    
    def __init__(self):
        self.checks = {
            'database': self._check_database,
            'api': self._check_api,
            'workers': self._check_workers,
            'data_freshness': self._check_data_freshness,
            'storage': self._check_storage,
            'source_apis': self._check_source_apis
        }
        
    async def run_health_check(self) -> Dict:
        """Run all health checks."""
        results = {
            'timestamp': datetime.utcnow(),
            'overall_health': 'HEALTHY',
            'checks': {}
        }
        
        for check_name, check_func in self.checks.items():
            try:
                result = await check_func()
                results['checks'][check_name] = result
                
                if result['status'] != 'HEALTHY':
                    results['overall_health'] = 'DEGRADED'
                    
            except Exception as e:
                results['checks'][check_name] = {
                    'status': 'ERROR',
                    'message': str(e)
                }
                results['overall_health'] = 'UNHEALTHY'
        
        # Send alerts if needed
        if results['overall_health'] != 'HEALTHY':
            await self._send_alerts(results)
        
        return results
```

## Cost Analysis
### *The Real Talk About Money*

```python
def calculate_monthly_costs():
    """
    Calculate real operational costs.
    Spoiler: It's less than your Netflix subscription.
    """
    costs = {
        'infrastructure': {
            'vps_hosting': 40,  # DigitalOcean/Hetzner
            'backup_storage': 5,  # S3/Backblaze
            'domain_name': 1,  # Amortized yearly cost
            'ssl_certificate': 0,  # Let's Encrypt FTW
        },
        'api_costs': {
            'nist_nvd': 0,  # Free tier
            'osv': 0,  # Free
            'snyk': 0,  # Free tier (200 tests/month)
            'other_sources': 0,  # Most are free
        },
        'time_investment': {
            'initial_setup_hours': 20,
            'monthly_maintenance_hours': 2,
            'hourly_rate': 'priceless',  # Your time
        }
    }
    
    total_monthly = sum(costs['infrastructure'].values()) + sum(costs['api_costs'].values())
    
    return {
        'total_monthly_usd': total_monthly,
        'total_yearly_usd': total_monthly * 12,
        'comparison': {
            'vs_commercial_solution': 'Save $1000-5000/month',
            'vs_doing_nothing': 'Avoid one breach = pays for itself forever',
            'vs_netflix': f"Costs {total_monthly/15:.1f} Netflix subscriptions"
        }
    }
```

## Lessons Learned
### *From Someone Who Built This*

1. **Start Small**: Don't try to ingest all sources at once. Start with NIST, add others gradually.

2. **Cache Everything**: API rate limits are real. Cache aggressively.

3. **Normalize Early**: Different sources use different formats. Normalize during ingestion, not during queries.

4. **Index Wisely**: Your queries will mostly be by date, severity, and product. Index accordingly.

5. **Monitor Everything**: You'll discover source API changes when your ingestion breaks at 3 AM.

6. **Have Fun With It**: If you're going to stare at vulnerabilities all day, might as well make it entertaining.

## Next Steps
### *Your Journey Continues*

Now that you have your own CVE database empire:

1. **Add More Sources**: Integrate GitHub Security Advisories, vendor-specific databases
2. **Build Integrations**: Slack bots, email alerts, JIRA tickets
3. **Add ML/AI**: Predict future vulnerabilities, auto-generate patches (just kidding on that last one)
4. **Share With Others**: Open source your tools, help the community
5. **Stay Paranoid**: New vulnerabilities are published every day. Your database should know about them.

## Final Thoughts
### *You Did It!*

Congratulations! You've built your own CVE database that:
- Aggregates data from 7+ sources
- Provides unlimited API access
- Includes creative tools that don't exist anywhere else
- Costs less than a nice dinner
- Makes you the vulnerability oracle of your organization

Remember: With great vulnerability data comes great responsibility. Use your powers for good, patch your systems, and maybe don't actually use the Patch Roulette in production.

---

*"The only thing we have to fear is fear itself. And also unpatched vulnerabilities. Lots of unpatched vulnerabilities."* - Your Security Team, Probably