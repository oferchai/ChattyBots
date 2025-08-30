#!/bin/bash
# Configuration Test Suite for Multi-Agent AI Chat System
# Automated testing script with result validation and reporting
#
# Usage: ./test_config_suite.sh
# 
# This script runs comprehensive configuration tests including:
# - Environment detection and switching
# - Configuration validation and loading  
# - Environment variable overrides
# - Production validation and security checks
# - Error handling and validation testing

set -e  # Exit on any error

# Colors for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

# Test results array
declare -a TEST_RESULTS

# Utility functions
print_header() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${WHITE}$1${NC}"
    echo -e "${BLUE}============================================${NC}"
}

print_test() {
    echo -e "\n${CYAN}🧪 $1${NC}"
    echo -e "${PURPLE}-------------------------------------------${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
    TEST_RESULTS+=("PASS: $1")
}

print_failure() {
    echo -e "${RED}❌ $1${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    TEST_RESULTS+=("FAIL: $1")
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_skip() {
    echo -e "${YELLOW}⏭️  $1${NC}"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
    TEST_RESULTS+=("SKIP: $1")
}

increment_test() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

# Test execution wrapper
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit_code="${3:-0}"  # Default to 0 if not specified
    local validation_pattern="$4"
    
    increment_test
    print_test "$test_name"
    
    # Run the test command and capture output
    local output
    local exit_code
    
    if output=$(eval "$test_command" 2>&1); then
        exit_code=0
    else
        exit_code=$?
    fi
    
    # Validate exit code
    if [ "$exit_code" -eq "$expected_exit_code" ]; then
        # If validation pattern is provided, check output
        if [ -n "$validation_pattern" ]; then
            if echo "$output" | grep -q "$validation_pattern"; then
                print_success "$test_name - Output validation passed"
                return 0
            else
                print_failure "$test_name - Output validation failed (missing: $validation_pattern)"
                echo -e "${YELLOW}Output:${NC} $output"
                return 1
            fi
        else
            print_success "$test_name - Exit code validation passed"
            return 0
        fi
    else
        print_failure "$test_name - Expected exit code $expected_exit_code, got $exit_code"
        echo -e "${YELLOW}Output:${NC} $output"
        return 1
    fi
}

# Individual test functions
test_basic_config_loading() {
    run_test \
        "Basic Configuration Loading" \
        "python test_config.py" \
        0 \
        "All configuration tests passed successfully"
}

test_development_environment() {
    run_test \
        "Development Environment Configuration" \
        "python test_config.py development" \
        0 \
        "Environment: development"
}

test_testing_environment() {
    run_test \
        "Testing Environment Configuration" \
        "python test_config.py testing" \
        0 \
        "Environment: testing"
}

test_environment_variable_overrides() {
    run_test \
        "Environment Variable Overrides" \
        "DATABASE__URL='sqlite:///./custom.db' LLM__PROVIDER='openrouter' AGENTS__MAX_CONVERSATION_ROUNDS=50 python test_config.py" \
        0 \
        "Max rounds: 50"
}

test_invalid_port_validation() {
    run_test \
        "Invalid Port Validation" \
        "SERVER__PORT=99999 python -c 'from backend.config import get_settings; get_settings()'" \
        1 \
        "Input should be less than or equal to 65535"
}

test_invalid_database_url_validation() {
    run_test \
        "Invalid Database URL Validation" \
        "DATABASE__URL='invalid://protocol' python -c 'from backend.config import get_settings; get_settings()'" \
        1 \
        "Database URL must use sqlite://, postgresql://, or mysql:// scheme"
}

test_production_debug_validation() {
    run_test \
        "Production Debug Mode Validation" \
        "ENVIRONMENT=production python -c 'from backend.config import get_settings; get_settings()'" \
        1 \
        "Debug mode must be disabled in production"
}

test_production_with_valid_config() {
    print_test "Production Environment with Valid Configuration"
    increment_test
    
    # Create temporary production config
    if cp .env.production.template .env.production 2>/dev/null; then
        if ENVIRONMENT=production python test_config.py >/dev/null 2>&1; then
            print_success "Production Environment with Valid Configuration"
            rm -f .env.production  # Cleanup
        else
            print_failure "Production Environment with Valid Configuration - Failed to load"
            rm -f .env.production  # Cleanup
        fi
    else
        print_skip "Production Environment with Valid Configuration - Template not found"
    fi
}

test_nested_environment_variables() {
    run_test \
        "Nested Environment Variables" \
        "LLM__OLLAMA__BASE_URL='http://custom:11434' AGENTS__RESPONSE_TIMEOUT=45 python -c 'from backend.config import get_settings; s=get_settings(); print(f\"Ollama URL: {s.llm.ollama.base_url}\"); print(f\"Timeout: {s.agents.response_timeout}\")'" \
        0 \
        "Ollama URL: http://custom:11434"
}

test_configuration_utility_methods() {
    run_test \
        "Configuration Utility Methods" \
        "python -c 'from backend.config import get_settings; s=get_settings(); print(\"Is dev:\", s.is_development); print(\"DB URL:\", s.get_database_url()); cors=s.get_cors_config(); print(\"CORS origins:\", len(cors[\"allow_origins\"]))'" \
        0 \
        "Is dev: True"
}

test_settings_singleton_pattern() {
    run_test \
        "Settings Singleton Pattern" \
        "python -c 'from backend.config import get_settings; s1=get_settings(); s2=get_settings(); print(f\"Same instance: {s1 is s2}\"); print(f\"App name: {s1.app_name}\")'" \
        0 \
        "Same instance: True"
}

test_environment_detection() {
    run_test \
        "Environment Detection Functions" \
        "python -c 'from backend.config import get_environment, Environment; env=get_environment(); print(f\"Current env: {env.value}\"); print(f\"Is enum: {isinstance(env, Environment)}\")'" \
        0 \
        "Current env: development"
}

test_configuration_validation_types() {
    run_test \
        "Configuration Type Validation" \
        "AGENTS__CONSENSUS_THRESHOLD=invalid python -c 'from backend.config import get_settings; get_settings()'" \
        1 \
        "validation error"
}

test_cors_configuration_generation() {
    run_test \
        "CORS Configuration Generation" \
        "python -c 'from backend.config import get_settings; s=get_settings(); cors=s.get_cors_config(); print(\"Origins:\", len(cors[\"allow_origins\"])); print(\"Credentials:\", cors[\"allow_credentials\"])'" \
        0 \
        "Credentials: True"
}

test_logging_configuration() {
    run_test \
        "Logging Configuration" \
        "python -c 'from backend.config import get_settings; s=get_settings(); print(f\"Log level: {s.logging.level.value}\"); print(f\"Console: {s.logging.console_output}\"); print(f\"File: {s.logging.file_path}\")'" \
        0 \
        "Log level:"
}

test_security_configuration() {
    run_test \
        "Security Configuration" \
        "python -c 'from backend.config import get_settings; s=get_settings(); print(f\"Rate limit: {s.security.rate_limit_per_minute}\"); print(f\"Secret key set: {bool(s.security.secret_key)}\")'" \
        0 \
        "Secret key set: True"
}

# Performance and edge case tests
test_configuration_reload() {
    run_test \
        "Configuration Reload" \
        "python -c 'from backend.config import get_settings, reload_settings; s1=get_settings(); s2=reload_settings(); print(f\"Reloaded successfully: {s2.app_name == s1.app_name}\")'" \
        0 \
        "Reloaded successfully: True"
}

test_multiple_environment_files() {
    print_test "Multiple Environment Files Priority"
    increment_test
    
    # Test environment file priority
    local test_output
    if test_output=$(python -c "
from backend.config import get_env_file_path, Environment
import os
dev_path = get_env_file_path(Environment.DEVELOPMENT)
test_path = get_env_file_path(Environment.TESTING)
print(f'Dev file: {os.path.basename(dev_path)}')
print(f'Test file: {os.path.basename(test_path)}')
print(f'Files exist: {os.path.exists(dev_path) and os.path.exists(test_path)}')
" 2>&1); then
        if echo "$test_output" | grep -q "Files exist: True"; then
            print_success "Multiple Environment Files Priority"
        else
            print_failure "Multiple Environment Files Priority - Environment files not found"
        fi
    else
        print_failure "Multiple Environment Files Priority - Test execution failed"
    fi
}

# Main test execution
main() {
    print_header "Multi-Agent AI Chat System - Configuration Test Suite"
    echo -e "${WHITE}Automated testing of configuration management system${NC}"
    echo -e "${BLUE}Running comprehensive validation tests...${NC}\n"
    
    # Check if we're in the right directory
    if [ ! -f "test_config.py" ]; then
        echo -e "${RED}❌ Error: test_config.py not found. Please run from project root directory.${NC}"
        exit 1
    fi
    
    # Check if backend.config module is available
    if ! python -c "import backend.config" 2>/dev/null; then
        echo -e "${RED}❌ Error: backend.config module not found. Please ensure the project is properly set up.${NC}"
        exit 1
    fi
    
    print_info "Starting test execution..."
    
    # Core functionality tests
    print_header "Core Functionality Tests"
    test_basic_config_loading
    test_development_environment
    test_testing_environment
    test_environment_detection
    test_settings_singleton_pattern
    
    # Configuration validation tests
    print_header "Configuration Validation Tests"
    test_invalid_port_validation
    test_invalid_database_url_validation
    test_configuration_validation_types
    test_production_debug_validation
    
    # Environment and override tests
    print_header "Environment & Override Tests"
    test_environment_variable_overrides
    test_nested_environment_variables
    test_production_with_valid_config
    test_multiple_environment_files
    
    # Utility and integration tests
    print_header "Utility & Integration Tests"
    test_configuration_utility_methods
    test_cors_configuration_generation
    test_logging_configuration
    test_security_configuration
    test_configuration_reload
    
    # Generate test report
    generate_test_report
}

generate_test_report() {
    print_header "Test Results Summary"
    
    echo -e "${WHITE}📊 Test Execution Statistics:${NC}"
    echo -e "${BLUE}   Total Tests:    ${WHITE}$TOTAL_TESTS${NC}"
    echo -e "${GREEN}   Passed Tests:   ${WHITE}$PASSED_TESTS${NC}"
    echo -e "${RED}   Failed Tests:   ${WHITE}$FAILED_TESTS${NC}"
    echo -e "${YELLOW}   Skipped Tests:  ${WHITE}$SKIPPED_TESTS${NC}"
    
    # Calculate success rate
    if [ $TOTAL_TESTS -gt 0 ]; then
        local success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
        echo -e "${PURPLE}   Success Rate:   ${WHITE}${success_rate}%${NC}"
    fi
    
    echo -e "\n${WHITE}📋 Detailed Test Results:${NC}"
    echo -e "${BLUE}----------------------------------------${NC}"
    
    for result in "${TEST_RESULTS[@]}"; do
        if [[ $result == PASS:* ]]; then
            echo -e "${GREEN}✅ ${result#PASS: }${NC}"
        elif [[ $result == FAIL:* ]]; then
            echo -e "${RED}❌ ${result#FAIL: }${NC}"
        elif [[ $result == SKIP:* ]]; then
            echo -e "${YELLOW}⏭️  ${result#SKIP: }${NC}"
        fi
    done
    
    # Final result
    echo -e "\n${BLUE}============================================${NC}"
    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${GREEN}🎉 ALL CONFIGURATION TESTS PASSED! 🎉${NC}"
        echo -e "${WHITE}Configuration management system is working correctly.${NC}"
        exit 0
    else
        echo -e "${RED}💥 SOME TESTS FAILED! 💥${NC}"
        echo -e "${YELLOW}Please review the failed tests above and fix any issues.${NC}"
        exit 1
    fi
}

# Handle script interruption
trap 'echo -e "\n${YELLOW}⚠️  Test suite interrupted by user${NC}"; exit 130' INT TERM

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
