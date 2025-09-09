Overall Project Summary

Project Name: Multi-Role User Portal

Technology Stack:

Backend: FastAPI (Python), MySQL

Frontend: Angular (TypeScript)

Email Integration: SMTP (automated credential delivery)

Architecture: RESTful API, role-based access, modular service layers

 Objective

To design and implement a secure, scalable, and user-friendly web application that supports multiple user roles with distinct login patterns, automated account creation, and profile management — mimicking a production-like environment for enterprise use cases.

Core Features

Automated User Account Creation

Role-based login ID generation (e.g., std12345, emp12345, mgr12345, ent12345, job71965).

Random password assignment sent directly to the user via email.

Credentials stored in the database (plain text for prototype as requested — could be hashed in production).

User Authentication & Role Handling

Sign-up and Sign-in endpoints built with FastAPI.

Distinct user roles (Student, Employee, Manager, Entrepreneur, Jobseeker).

Scalable design for future permissions and role-based dashboards.

Student Profile Module

Add/Edit student profile information (personal, academic, contact details).

Upload and store profile photos and resumes.

Real-time profile viewing and editing in the Angular frontend.

Email Notifications

SMTP-based email service for automated delivery of credentials.

Responsive Angular UI

Modern interface with clear navigation.

Built for desktop and mobile responsiveness.

 Technical Highlights

RESTful API with clear route organization.

MySQL database schema supporting relational mapping between users and student profiles.

Environment-based configuration for secure DB and email credentials.

Separation of concerns: Independent backend and frontend for cleaner development and deployment.

Ready for scaling — password hashing, JWT-based sessions, and cloud deployment can be added with minimal refactoring.

 Outcome

This project successfully demonstrated:

End-to-end full-stack development capabilities.

Integration of authentication, database, and email services.

Real-world problem-solving in an internship setting — from requirement analysis to deployment-ready architecture.

 Impact / Learning

Learned production-level backend development (FastAPI, REST design, DB modeling).

Built a dynamic, responsive frontend (Angular).

Implemented secure (and configurable) communication between services.

Gained hands-on experience in debugging, data flow design, and deployment preparation.



# Web

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 20.2.2.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.

