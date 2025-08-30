# Configuration Test Suite

Comprehensive automated testing for the Multi-Agent AI Chat System configuration management system.

## Overview

The configuration test suite (`test_config_suite.sh`) provides comprehensive automated testing of the configuration management system with detailed reporting and validation.

## Features

- **18 Comprehensive Tests** covering all configuration aspects
- **Color-coded Output** for easy visualization of test results
- **Detailed Validation** with both exit code and output pattern matching
- **Test Statistics** including success rate and detailed reporting
- **Error Handling** with graceful failure detection and reporting
- **Environment Detection** with automatic prerequisite checking

## Test Categories

### 🔧 Core Functionality Tests (5 tests)
- **Basic Configuration Loading** - Tests main configuration system
- **Development Environment Configuration** - Validates dev environment settings
- **Testing Environment Configuration** - Validates test environment settings  
- **Environment Detection Functions** - Tests automatic environment detection
- **Settings Singleton Pattern** - Validates singleton implementation

### 🔒 Configuration Validation Tests (4 tests)
- **Invalid Port Validation** - Tests port range validation
- **Invalid Database URL Validation** - Tests database URL format validation
- **Configuration Type Validation** - Tests type conversion and validation
- **Production Debug Mode Validation** - Tests production safety checks

### 🌍 Environment & Override Tests (4 tests)
- **Environment Variable Overrides** - Tests environment variable precedence
- **Nested Environment Variables** - Tests nested configuration overrides
- **Production Environment with Valid Configuration** - Tests production config loading
- **Multiple Environment Files Priority** - Tests file priority resolution

### 🛠️ Utility & Integration Tests (5 tests)
- **Configuration Utility Methods** - Tests helper methods and properties
- **CORS Configuration Generation** - Tests FastAPI CORS integration
- **Logging Configuration** - Tests logging system configuration
- **Security Configuration** - Tests security settings validation
- **Configuration Reload** - Tests dynamic configuration reloading

## Usage

### Basic Usage
```bash
# Run all tests
./test_config_suite.sh

# Make executable if needed
chmod +x test_config_suite.sh
```

### Prerequisites
- Python environment with required packages (pydantic-settings)
- Backend configuration module available
- Test files (test_config.py, .env files) present

## Test Results

### Success Output
```
============================================
🎉 ALL CONFIGURATION TESTS PASSED! 🎉
============================================
Configuration management system is working correctly.

📊 Test Execution Statistics:
   Total Tests:    18
   Passed Tests:   18
   Failed Tests:   0
   Skipped Tests:  0
   Success Rate:   100%
```

### Detailed Test Report
Each test provides detailed results:
- ✅ **PASSED** - Test completed successfully with validation
- ❌ **FAILED** - Test failed with error details and output
- ⏭️ **SKIPPED** - Test skipped due to prerequisites

## Test Validation

### Exit Code Validation
Tests validate both:
- **Expected Exit Codes** (0 for success, 1 for expected failures)
- **Output Pattern Matching** for specific validation strings

### Output Pattern Examples
```bash
# Success validation
"All configuration tests passed successfully"

# Error validation  
"Input should be less than or equal to 65535"

# Environment validation
"Environment: development"
```

## Advanced Features

### Error Handling
- Graceful handling of script interruption (Ctrl+C)
- Automatic prerequisite checking
- Detailed error reporting with context

### Test Isolation
- Each test runs in isolated environment
- Temporary file cleanup for production tests
- Environment variable restoration

### Color Coding
- 🔵 **Blue** - Headers and informational messages
- 🟢 **Green** - Successful tests and validation
- 🔴 **Red** - Failed tests and errors
- 🟡 **Yellow** - Warnings and skipped tests
- 🟣 **Purple** - Test separators and statistics

## Individual Test Details

### Core Functionality Tests

1. **Basic Configuration Loading**
   - Runs: `python test_config.py`
   - Validates: Complete configuration test suite passes
   - Expected: All tests pass with success message

2. **Development Environment Configuration** 
   - Runs: `python test_config.py development`
   - Validates: Development environment properly loaded
   - Expected: Environment detection and configuration

3. **Testing Environment Configuration**
   - Runs: `python test_config.py testing`
   - Validates: Testing environment settings applied
   - Expected: Different port, in-memory DB, minimal logging

4. **Environment Detection Functions**
   - Tests: Environment enum detection and validation
   - Validates: Proper environment type detection
   - Expected: Environment enum instances working correctly

5. **Settings Singleton Pattern**
   - Tests: Multiple get_settings() calls return same instance
   - Validates: Singleton pattern implementation
   - Expected: Same object instance across calls

### Validation Tests

6. **Invalid Port Validation**
   - Tests: Port > 65535 (invalid range)
   - Validates: Proper validation error thrown
   - Expected: Pydantic validation error with specific message

7. **Invalid Database URL Validation**
   - Tests: Invalid database URL scheme
   - Validates: URL format validation
   - Expected: Database URL scheme validation error

8. **Configuration Type Validation** 
   - Tests: Invalid type for consensus threshold
   - Validates: Type conversion and validation
   - Expected: Type validation error

9. **Production Debug Mode Validation**
   - Tests: Production environment with debug=True
   - Validates: Production safety checks
   - Expected: Production validation prevents debug mode

### Environment & Override Tests

10. **Environment Variable Overrides**
    - Tests: Custom database URL, LLM provider, agent settings
    - Validates: Environment variables override config files
    - Expected: Settings reflect environment variable values

11. **Nested Environment Variables**
    - Tests: `LLM__OLLAMA__BASE_URL` and `AGENTS__RESPONSE_TIMEOUT`
    - Validates: Double underscore nested variable parsing
    - Expected: Nested configuration properly applied

12. **Production Environment with Valid Configuration**
    - Tests: Full production configuration loading
    - Validates: Production settings without validation errors
    - Expected: Successful production environment loading

13. **Multiple Environment Files Priority**
    - Tests: Environment-specific file detection
    - Validates: File resolution and priority system
    - Expected: Both development and testing files exist

### Utility & Integration Tests

14. **Configuration Utility Methods**
    - Tests: `is_development`, `get_database_url()`, CORS config
    - Validates: Utility methods return expected values
    - Expected: Development mode detection and URL formatting

15. **CORS Configuration Generation**
    - Tests: `get_cors_config()` method for FastAPI
    - Validates: CORS dictionary structure
    - Expected: Proper credentials and origins configuration

16. **Logging Configuration**
    - Tests: Log level, console output, file path settings
    - Validates: Logging system configuration
    - Expected: Logging settings properly structured

17. **Security Configuration**
    - Tests: Rate limiting, secret key configuration
    - Validates: Security settings validation
    - Expected: Security features properly configured

18. **Configuration Reload**
    - Tests: `reload_settings()` function
    - Validates: Dynamic configuration reloading
    - Expected: Successfully reload configuration

## Script Architecture

### Functions
- `run_test()` - Core test execution wrapper with validation
- `print_*()` - Formatted output functions with color coding
- `test_*()` - Individual test implementations
- `generate_test_report()` - Comprehensive results reporting

### Variables
- `TOTAL_TESTS`, `PASSED_TESTS`, `FAILED_TESTS`, `SKIPPED_TESTS` - Counters
- `TEST_RESULTS[]` - Array storing detailed results
- Color constants for terminal formatting

### Error Handling
- `set -e` - Exit on any error in main script
- `trap` - Handle script interruption gracefully
- Validation of prerequisites before test execution

## Troubleshooting

### Common Issues

1. **Script not executable**
   ```bash
   chmod +x test_config_suite.sh
   ```

2. **Missing dependencies**
   ```bash
   conda install -c conda-forge pydantic-settings
   ```

3. **Wrong directory**
   ```bash
   # Run from project root where test_config.py exists
   cd /path/to/chatbot/project
   ./test_config_suite.sh
   ```

4. **Backend module not found**
   ```bash
   # Ensure backend module is in Python path
   export PYTHONPATH=/path/to/project:$PYTHONPATH
   ```

### Test Debugging
- Individual tests can be debugged by running their commands manually
- Output is captured and displayed for failed tests
- Validation patterns can be adjusted for different environments

## Integration

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run Configuration Tests
  run: |
    chmod +x test_config_suite.sh
    ./test_config_suite.sh
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
./test_config_suite.sh
```

## Extending Tests

### Adding New Tests
```bash
test_my_new_feature() {
    run_test \
        "My New Feature Test" \
        "python -c 'test command here'" \
        0 \
        "expected output pattern"
}

# Add to main() function test execution
test_my_new_feature
```

### Custom Validation
```bash
# Custom test with manual validation
test_custom_feature() {
    print_test "Custom Feature Test"
    increment_test
    
    if custom_validation_logic; then
        print_success "Custom Feature Test"
    else
        print_failure "Custom Feature Test - Custom validation failed"
    fi
}
```

This comprehensive test suite ensures the configuration management system is robust, secure, and ready for production deployment across all supported environments.
