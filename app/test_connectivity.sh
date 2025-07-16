#!/bin/bash

echo "=== Supply Chain Tracker API Connectivity Test ==="
echo ""

# Test if containers are running
echo "1. Checking if containers are running..."
docker-compose ps

echo ""
echo "2. Testing direct backend connectivity..."

# Test direct backend access
echo "   - Testing backend health (direct): http://localhost:8002/health"
curl -s http://localhost:8002/health | jq . 2>/dev/null || echo "Failed or no JSON response"

echo "   - Testing backend docs (direct): http://localhost:8002/docs"
curl -s -I http://localhost:8002/docs | head -n 1

echo "   - Testing backend OpenAPI (direct): http://localhost:8002/openapi.json"
curl -s http://localhost:8002/openapi.json | jq '.info.title' 2>/dev/null || echo "Failed or no JSON response"

echo ""
echo "3. Testing through nginx proxy..."

# Test through nginx
echo "   - Testing via staging domain: https://staging-sctracker.aimingmed.local/api/health"
curl -k -s https://staging-sctracker.aimingmed.local/api/health | jq . 2>/dev/null || echo "Failed or no JSON response"

echo "   - Testing docs via staging domain: https://staging-sctracker.aimingmed.local/docs"
curl -k -s -I https://staging-sctracker.aimingmed.local/docs | head -n 1

echo "   - Testing via localhost: https://localhost/api/health"
curl -k -s https://localhost/api/health | jq . 2>/dev/null || echo "Failed or no JSON response"

echo ""
echo "4. Testing productlog endpoints..."
echo "   - Testing product-details: https://staging-sctracker.aimingmed.local/api/productlog/product-details"
curl -k -s https://staging-sctracker.aimingmed.local/api/productlog/product-details | jq . 2>/dev/null || echo "Failed or no JSON response"

echo ""
echo "5. Network connectivity..."
echo "   - Checking if staging domain resolves..."
nslookup staging-sctracker.aimingmed.local 2>/dev/null || echo "Domain does not resolve"

echo ""
echo "=== Test Complete ==="
echo ""
echo "If you see 404 errors, the routing is incorrect."
echo "If you see connection errors, check if containers are running."
echo "If you see SSL errors, check certificate configuration."
