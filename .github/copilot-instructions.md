<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# E-commerce Digital Product Platform - Copilot Instructions

## Project Overview
This is a full-stack e-commerce platform for digital products with:
- **Backend**: FastAPI (Python) with SQLAlchemy ORM
- **Frontend**: React 18 with TypeScript
- **Database**: PostgreSQL with Redis for caching
- **Authentication**: JWT-based system
- **Payment**: Stripe integration

## Code Style & Standards

### Backend (Python/FastAPI)
- Follow PEP 8 standards
- Use type hints for all functions and variables
- Use Pydantic models for request/response schemas
- Follow FastAPI best practices for dependency injection
- Use async/await for database operations
- Implement proper error handling with custom exceptions
- Use SQLAlchemy 2.0 syntax
- Follow the repository pattern for data access

### Frontend (React/TypeScript)
- Use functional components with hooks
- Follow React best practices and hooks rules
- Use TypeScript strict mode
- Implement proper error boundaries
- Use Redux Toolkit for state management
- Follow atomic design principles for components
- Use React Hook Form for form handling
- Implement proper loading states and error handling

### Database
- Use snake_case for table and column names
- Create proper indexes for performance
- Use foreign key constraints
- Follow normalization principles
- Use Alembic for migrations

## Architecture Patterns

### Backend Architecture
- **Controllers**: Handle HTTP requests in `api/` directory
- **Services**: Business logic in `services/` directory  
- **Models**: SQLAlchemy models in `models/` directory
- **Schemas**: Pydantic schemas in `schemas/` directory
- **Repositories**: Data access layer abstraction
- **Dependencies**: FastAPI dependencies for reusable logic

### Frontend Architecture
- **Components**: Reusable UI components in `components/`
- **Pages**: Route-level components in `pages/`
- **Services**: API integration in `services/`
- **Hooks**: Custom React hooks in `hooks/`
- **Utils**: Helper functions in `utils/`
- **Types**: TypeScript definitions in `types/`

## Security Considerations
- Always validate and sanitize user input
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Hash passwords using bcrypt
- Use HTTPS in production
- Implement rate limiting
- Validate file uploads thoroughly
- Use CORS properly

## API Design
- Follow RESTful conventions
- Use proper HTTP status codes
- Implement pagination for list endpoints
- Use consistent error response format
- Version APIs with `/api/v1/` prefix
- Document all endpoints with OpenAPI

## Testing Guidelines
- Write unit tests for all business logic
- Use pytest for backend testing
- Use Jest and React Testing Library for frontend
- Implement integration tests for API endpoints
- Test error scenarios and edge cases
- Maintain high test coverage

## Performance Optimization
- Use database indexes appropriately
- Implement caching with Redis
- Use lazy loading for large datasets
- Optimize database queries
- Implement code splitting in React
- Use proper image optimization

## File Organization
- Group related files together
- Use descriptive file and directory names
- Separate concerns properly
- Follow the established folder structure
- Keep components small and focused

## Environment Configuration
- Use environment variables for configuration
- Never commit sensitive data
- Use different configs for dev/staging/prod
- Document all required environment variables

## Error Handling
- Use custom exception classes
- Implement global error handlers
- Provide meaningful error messages
- Log errors appropriately
- Handle async errors properly

## Code Generation Preferences
- Generate complete, working code examples
- Include proper error handling
- Add appropriate comments for complex logic
- Follow the established patterns in the codebase
- Include necessary imports and dependencies
- Consider scalability and maintainability
