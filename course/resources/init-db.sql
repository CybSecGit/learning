-- Initialize database for Web Scraping Course
-- This script sets up the initial schema and sample data

-- Create schema
CREATE SCHEMA IF NOT EXISTS scraping;

-- Set search path
SET search_path TO scraping, public;

-- Tools table for tracking scraped tools
CREATE TABLE IF NOT EXISTS tools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100),
    url VARCHAR(500),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scraping runs table
CREATE TABLE IF NOT EXISTS scraping_runs (
    id SERIAL PRIMARY KEY,
    tool_id INTEGER REFERENCES tools(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    error_message TEXT,
    scraped_data JSONB
);

-- Changelog entries table
CREATE TABLE IF NOT EXISTS changelog_entries (
    id SERIAL PRIMARY KEY,
    tool_id INTEGER REFERENCES tools(id),
    version VARCHAR(50),
    release_date DATE,
    title VARCHAR(500),
    content TEXT,
    url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance metrics table
CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES scraping_runs(id),
    metric_name VARCHAR(100),
    metric_value DECIMAL(10, 2),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_tools_name ON tools(name);
CREATE INDEX idx_scraping_runs_tool_id ON scraping_runs(tool_id);
CREATE INDEX idx_scraping_runs_status ON scraping_runs(status);
CREATE INDEX idx_changelog_entries_tool_id ON changelog_entries(tool_id);
CREATE INDEX idx_changelog_entries_release_date ON changelog_entries(release_date);

-- Create update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tools_updated_at BEFORE UPDATE ON tools
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO tools (name, category, url, description) VALUES
    ('React', 'Frontend Framework', 'https://react.dev', 'A JavaScript library for building user interfaces'),
    ('Django', 'Web Framework', 'https://www.djangoproject.com', 'The web framework for perfectionists with deadlines'),
    ('PostgreSQL', 'Database', 'https://www.postgresql.org', 'The world''s most advanced open source database'),
    ('Docker', 'DevOps', 'https://www.docker.com', 'Develop faster. Run anywhere.'),
    ('Kubernetes', 'DevOps', 'https://kubernetes.io', 'Production-Grade Container Orchestration')
ON CONFLICT (name) DO NOTHING;

-- Create views for common queries
CREATE OR REPLACE VIEW v_recent_scraping_runs AS
SELECT 
    sr.id,
    t.name as tool_name,
    sr.started_at,
    sr.completed_at,
    sr.status,
    sr.error_message,
    EXTRACT(EPOCH FROM (sr.completed_at - sr.started_at)) as duration_seconds
FROM scraping_runs sr
JOIN tools t ON sr.tool_id = t.id
ORDER BY sr.started_at DESC
LIMIT 100;

CREATE OR REPLACE VIEW v_tool_scraping_stats AS
SELECT 
    t.id,
    t.name,
    COUNT(sr.id) as total_runs,
    COUNT(CASE WHEN sr.status = 'success' THEN 1 END) as successful_runs,
    COUNT(CASE WHEN sr.status = 'failed' THEN 1 END) as failed_runs,
    AVG(EXTRACT(EPOCH FROM (sr.completed_at - sr.started_at))) as avg_duration_seconds,
    MAX(sr.completed_at) as last_scraped
FROM tools t
LEFT JOIN scraping_runs sr ON t.id = sr.tool_id
GROUP BY t.id, t.name;

-- Grant permissions (adjust as needed)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA scraping TO scraper;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA scraping TO scraper;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA scraping TO scraper;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully!';
END $$;