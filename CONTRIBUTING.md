# 🤝 Contributing to MCP DJEN Server

Thank you for your interest in contributing to the MCP DJEN Server! This document provides guidelines for contributing to this project.

## 🎯 Project Goals

Our mission is to standardize access to Brazilian court data for LLM agents and AI applications, making legal automation accessible to developers worldwide.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- Docker (optional)

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/mcp-djen-server.git
cd mcp-djen-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python3 test_server.py

# Start development server
python3 start_server.py
```

## 📋 Contribution Guidelines

### Code Standards
- **Type Hints**: Required for all functions
- **Docstrings**: Google style documentation
- **Tests**: 90%+ coverage required
- **Linting**: Zero warnings (flake8, black)
- **Commits**: Conventional commits format

### Pull Request Process
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python3 test_server.py

# Run specific test
python3 -m pytest tests/test_adapter.py

# Run with coverage
python3 -m pytest --cov=app tests/
```

### Test Structure
```
tests/
├── test_adapter.py      # API integration tests
├── test_main.py         # Endpoint tests
├── test_validation.py   # Data validation tests
└── test_performance.py  # Performance benchmarks
```

## 📚 Documentation

### Adding Documentation
- **README.md**: Project overview and quick start
- **API docs**: OpenAPI specification
- **Code comments**: Inline documentation
- **Examples**: Usage examples in `/examples`

### Documentation Standards
- Clear and concise language
- Code examples for all endpoints
- Error handling documentation
- Performance considerations

## 🔧 Development Workflow

### 1. Issue Discussion
- Open an issue to discuss proposed changes
- Provide context and use cases
- Link related issues or pull requests

### 2. Implementation
- Follow the established code style
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Review Process
- Self-review your changes
- Request review from maintainers
- Address feedback promptly
- Ensure CI/CD passes

## 🏗️ Architecture Guidelines

### Adding New Endpoints
1. **Define** the endpoint in `app/main.py`
2. **Add** Pydantic models for request/response
3. **Implement** error handling
4. **Add** rate limiting
5. **Write** comprehensive tests
6. **Update** OpenAPI specification

### Error Handling
- Use structured error responses
- Include appropriate HTTP status codes
- Provide helpful error messages
- Log errors for debugging

### Performance Considerations
- Implement caching where appropriate
- Use async/await for I/O operations
- Monitor response times
- Consider rate limiting

## 🌍 Internationalization

### Adding Support for New Countries
1. **Research** the country's legal API structure
2. **Create** adapter for the new API
3. **Add** country-specific error handling
4. **Update** documentation with examples
5. **Add** tests for the new integration

### Current Supported Countries
- **Brazil**: DJEN API (Production)
- **Mexico**: AMLO API (Planned)
- **Portugal**: STJ API (Planned)
- **Argentina**: PJF API (Planned)

## 📊 Performance Benchmarks

### Current Metrics
- **Response Time**: < 4 seconds average
- **Throughput**: 100 requests/minute
- **Uptime**: 99.9% availability
- **Error Rate**: 0.5%

### Adding Benchmarks
1. **Define** the benchmark scenario
2. **Implement** performance tests
3. **Document** the methodology
4. **Update** BENCHMARKS.md

## 🐛 Bug Reports

### Reporting Bugs
1. **Check** existing issues
2. **Provide** detailed reproduction steps
3. **Include** error logs and stack traces
4. **Specify** environment details
5. **Add** screenshots if applicable

### Bug Report Template
```markdown
**Description**
Brief description of the issue

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.11.6]
- Version: [e.g., 1.0.0]

**Additional Information**
Any other context or logs
```

## 💡 Feature Requests

### Suggesting Features
1. **Describe** the feature clearly
2. **Explain** the use case
3. **Provide** examples if possible
4. **Consider** implementation complexity
5. **Discuss** with maintainers

## 📞 Getting Help

### Communication Channels
- **Issues**: GitHub Issues for bugs and features
- **Discussions**: GitHub Discussions for questions
- **Email**: hi@pdrobrandao.com for private matters

### Code of Conduct
- Be respectful and inclusive
- Focus on technical discussions
- Help others learn and grow
- Follow the project's coding standards

## 🎉 Recognition

### Contributors
- Your name will be added to the contributors list
- Significant contributions get special recognition
- We appreciate all forms of contribution

### Types of Contributions
- **Code**: Bug fixes, new features, improvements
- **Documentation**: Guides, examples, API docs
- **Testing**: Test cases, bug reports
- **Design**: UI/UX improvements, diagrams
- **Community**: Helping others, answering questions

---

**Thank you for contributing to the future of legal automation!** 🚀 